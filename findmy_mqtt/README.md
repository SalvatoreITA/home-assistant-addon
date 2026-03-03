# 🚀 FindMy MQTT Bridge

Questo Add-on ti permette di tracciare i tuoi Apple AirTag, iPhone, iPad e Mac direttamente su Home Assistant!

## ⚙️ Configurazione
1. Compila l'Apple ID e la Password.
2. Inserisci l'URL del tuo server Anisette locale (es. `http://IP:6969`). 
**GUIDA Anisette:** https://github.com/SalvatoreITA/home-assistant-addon/tree/main/anisette_server
3. Carica i file `.plist` dei tuoi dispositivi nella cartella condivisa `/share/findmy/keys`.
**GUIDA Estrazione Plist:** https://github.com/SalvatoreITA/AirTag-Key-Extractor

## ⚠️ Primo Avvio (Codice 2FA)
Se Apple ti chiede il codice a due fattori, l'Add-on si metterà in pausa. Crea un file di testo in `/share/findmy/2fa_code.txt`, scrivici dentro le 6 cifre e salvalo. L'Add-on lo leggerà automaticamente!

> [!IMPORTANT]
> ### ⏱️ Intervallo di Aggiornamento e Sicurezza
> Per impostazione predefinita, l'intervallo di polling è fissato a **15 minuti**. 
> 
> **Si sconsiglia vivamente di scendere al di sotto di questa soglia.** >
> Effettuare richieste troppo frequenti ai server Apple (es. ogni 1 o 5 minuti) può essere interpretato come un comportamento anomalo o un attacco di tipo bot. Questo espone il tuo profilo al rischio concreto di **ban temporaneo o permanente dell'Apple ID**. Mantieni l'intervallo a 15+ minuti per garantire la massima stabilità e sicurezza del tuo account.

### 📡 Topic MQTT

Il bridge pubblica costantemente i dati (in base all'intervallo di polling scelto) sui seguenti topic:

| Dato | Topic | Contenuto (Esempio) |
| :--- | :--- | :--- |
| **Attributi** | `findmy/airtag/{ID}/attributes` | `{"latitude": 45.46, "longitude": 9.19, "timestamp": 1709395200}` |
| **Stato** | `findmy/airtag/{ID}/state` | `02/03/2026 16:45` (Data leggibile) |

> [!TIP]
> L'**`{ID}`** corrisponde al nome del file `.plist` (senza estensione) che hai caricato nella cartella `keys`. Ad esempio, se il file si chiama `zaino.plist`, il topic sarà `findmy/airtag/zaino/attributes`.

### 🏠 Esempio Integrazione Home Assistant

Aggiungi questo codice al tuo file `configuration.yaml` per creare un tracker basato sui dati MQTT:

```yaml
mqtt:
  device_tracker:
    - name: "Airtag Chiavi"
      state_topic: "findmy/airtag/chiavi_casa/state"
      json_attributes_topic: "findmy/airtag/chiavi_casa/attributes"
      source_type: gps
```

Aggiungi questo codice al tuo file `configuration.yaml` per creare un sensore ultimo aggiornamento AirTag:

```yaml
  sensor:
    - name: "Ultimo Aggiornamento Airtag Chiavi"
      state_topic: "findmy/airtag/chiavi_casa/attributes"
      device_class: timestamp
      value_template: >
        {% set ts = value_json.timestamp | float(0) %}
        {% set ts_sec = ts / 1000 if ts > 9999999999 else ts %}
        {{ (ts_sec | as_datetime | as_local).isoformat() }}
```

## ⚖️ Disclaimer & Limitazione di Responsabilità

**ATTENZIONE:** Questo progetto è rilasciato esclusivamente a **scopo didattico, di test e di ricerca personale**. 

1. **Nessuna Affiliazione:** Questo progetto **NON è** in alcun modo affiliato, autorizzato, mantenuto, sponsorizzato o approvato da **Apple Inc.** o da una delle sue sussidiarie o affiliate. 
2. **Uso a proprio rischio:** L'utilizzo della rete "Find My" al di fuori dei client ufficiali Apple può violare i Termini di Servizio di Apple. L'utente si assume la piena responsabilità per qualsiasi conseguenza derivante dall'uso di questo software, inclusi (ma non limitati a) il blocco temporaneo o permanente dell'ID Apple o limitazioni sull'account.
3. **Proprietà Intellettuale:** Tutti i marchi registrati (Apple, FindMy, AirTag, iPhone, ecc.) appartengono ai rispettivi proprietari. Questo software non contiene codice proprietario di Apple, ma utilizza librerie open-source per interagire con API pubbliche a scopo di interoperabilità domotica.
4. **Nessuna Garanzia:** Il software viene fornito "così com'è", senza garanzie di alcun tipo, espresse o implicite, riguardo alla sua funzionalità o sicurezza.

*Questo repository è destinato alla conservazione di prove di concetto (PoC) per l'interoperabilità tra sistemi IoT e non ha scopi di lucro.*

## ❤️ Crediti

Questo progetto non sarebbe stato possibile senza il lavoro della community open-source e dei seguenti progetti:

* **[Salvatore Lentini](https://domhouse.it)**: Autore dell' Addon
* **[FindMy.py](https://github.com/malmeloo/FindMy.py)**: La libreria core che permette l'interazione con i server Apple FindMy.
* **[Paho MQTT](https://eclipse.dev/paho/index.php?page=clients/python/index.php)**: Per la gestione affidabile dei messaggi verso il broker.
