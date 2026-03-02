import os, time, glob, json, logging, sys, datetime
import urllib.request
import paho.mqtt.client as mqtt
from findmy import FindMyAccessory
from findmy.reports import AppleAccount, RemoteAnisetteProvider, LoginState

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("FindMy-Bridge-HA")

# Percorsi in ambiente Home Assistant
OPTIONS_FILE = "/data/options.json"
KEYS_DIR = "/share/findmy/keys"
STATE_FILE = "/data/account.json"
MFA_FILE = "/share/findmy/2fa_code.txt"

# Lettura configurazione da Home Assistant
try:
    with open(OPTIONS_FILE) as f:
        options = json.load(f)
except Exception as e:
    logger.error(f"Errore lettura configurazione Add-on: {e}"); sys.exit(1)

APPLE_ID = options.get("apple_id")
APPLE_PASS = options.get("apple_pass")
ANISETTE_URL = options.get("anisette_url", "http://127.0.0.1:6969")
MQTT_BROKER = options.get("mqtt_broker", "core-mosquitto")
MQTT_PORT = int(options.get("mqtt_port", 1883))
MQTT_USER = options.get("mqtt_user", "")
MQTT_PASS = options.get("mqtt_pass", "")
INTERVAL = int(options.get("interval", 15)) * 60

def wait_for_anisette():
    logger.info(f"⏳ Verifico lo stato di Anisette su {ANISETTE_URL} ...")
    while True:
        try:
            req = urllib.request.Request(ANISETTE_URL, headers={'User-Agent': 'Mozilla/5.0'})
            urllib.request.urlopen(req, timeout=3)
            logger.info("✅ Anisette è ONLINE e pronto!")
            break
        except Exception:
            logger.warning("⏳ Anisette sta ancora caricando. Riprovo tra 5 secondi...")
            time.sleep(5)

def setup_mqtt():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="FindMyBridgeHA")
    except AttributeError:
        client = mqtt.Client(client_id="FindMyBridgeHA")

    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    return client

def load_accessories():
    os.makedirs(KEYS_DIR, exist_ok=True)
    accs = {}
    for file in glob.glob(f"{KEYS_DIR}/*.plist"):
        try:
            with open(file, "rb") as f:
                name = os.path.splitext(os.path.basename(file))[0]
                accs[name] = FindMyAccessory.from_plist(f)
        except Exception as e:
            logger.error(f"Errore lettura {file}: {e}")
    return accs

def main():
    if not APPLE_ID or APPLE_ID == "tua@email.com" or not APPLE_PASS:
        logger.error("❌ Compila ID Apple e Password nella tab Configurazione dell'Add-on."); sys.exit(1)

    accs_map = load_accessories()
    if not accs_map:
        logger.error(f"❌ Nessun file .plist trovato in {KEYS_DIR}. Aggiungili e riavvia l'Add-on."); sys.exit(1)
    accs_list = list(accs_map.values())

    wait_for_anisette()
    mqtt_client = setup_mqtt()
    anisette = RemoteAnisetteProvider(ANISETTE_URL)

    acc = None
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                saved_data = json.load(f)
                try:
                    acc = AppleAccount.from_json(saved_data)
                except TypeError:
                    acc = AppleAccount.from_json(json.dumps(saved_data))
                acc.anisette_provider = anisette
            logger.info("♻️ Sessione Apple ricaricata con successo.")
        except Exception as e:
            logger.error(f"Errore caricamento sessione: {e}")

    if not acc:
        acc = AppleAccount(anisette)
        logger.info("🔐 Primo avvio: Tentativo di login sui server Apple...")
        state = acc.login(APPLE_ID, APPLE_PASS)

        if state == LoginState.REQUIRE_2FA:
            logger.warning("⚠️ Apple richiede l'autenticazione a due fattori (2FA).")
            methods = acc.get_2fa_methods()
            methods[0].request()

            logger.error(f"🚨 AZIONE RICHIESTA: Crea un file di testo in '{MFA_FILE}' e scrivici dentro il codice a 6 cifre ricevuto sui tuoi dispositivi Apple.")

            while not os.path.exists(MFA_FILE):
                time.sleep(5)

            with open(MFA_FILE, "r") as f:
                code = f.read().strip()

            logger.info("📩 Codice letto dal file, tentativo di invio...")
            methods[0].submit(code)

            try:
                os.remove(MFA_FILE) # Pulisce il file
            except:
                pass

        with open(STATE_FILE, "w") as f:
            data_to_save = acc.to_json()
            if isinstance(data_to_save, dict):
                json.dump(data_to_save, f)
            else:
                f.write(data_to_save)
        logger.info("✅ Login salvato con successo!")

    while True:
        logger.info("📡 Interrogo i server Apple per le posizioni...")
        try:
            reports_dict = acc.fetch_location(accs_list)

            for acc_obj, reports in reports_dict.items():
                if not reports: continue

                latest = max(reports, key=lambda r: r.timestamp) if isinstance(reports, list) else reports
                device_id = next((name for name, obj in accs_map.items() if obj == acc_obj), "tracker")

                raw_ts = getattr(latest, "timestamp", 0)
                try:
                    if isinstance(raw_ts, datetime.datetime):
                        ts_sec = raw_ts.timestamp()
                    else:
                        val_num = float(raw_ts)
                        ts_sec = val_num / 1000.0 if val_num > 9999999999 else val_num

                    stato_ora = datetime.datetime.fromtimestamp(ts_sec).strftime('%d/%m/%Y %H:%M')
                    json_ts = int(ts_sec * 1000)
                except Exception as e:
                    logger.error(f"Errore conversione data: {raw_ts} - {e}")
                    stato_ora, json_ts = "Errore Data", 0

                payload = json.dumps({
                    "latitude": getattr(latest, "latitude", None),
                    "longitude": getattr(latest, "longitude", None),
                    "timestamp": json_ts
                })

                mqtt_client.publish(f"findmy/airtag/{device_id}/attributes", payload, retain=True)
                mqtt_client.publish(f"findmy/airtag/{device_id}/state", stato_ora, retain=True)

                logger.info(f"📍 {device_id} TRACCIATO! Lat: {getattr(latest, 'latitude', 'N/A')}, Lon: {getattr(latest, 'longitude', 'N/A')} - Orario: {stato_ora}")

        except Exception as e:
            logger.error(f"Nessuna risposta valida: {e}")

        logger.info(f"⏳ Prossimo controllo tra {INTERVAL // 60} minuti...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
