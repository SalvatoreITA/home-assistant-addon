# 🍏 Apple Anisette Server (Local for Home Assistant)

Questo Add-on esegue un server **Anisette v3** completamente in locale sul tuo Home Assistant. 
È il motore fondamentale che permette di generare i token di autenticazione necessari per fare il login sui server Apple, simulando l'identità di un Mac virtuale.

Lavorando interamente in locale, i tuoi dati (e le tue credenziali) non passeranno **mai** attraverso server di terze parti o servizi cloud esterni!

## ⚙️ Come funziona e Configurazione

A differenza di altri Add-on, **non è necessaria alcuna configurazione manuale**. 

1. Installa l'Add-on dalla repository.
2. Clicca su **Avvia**.
3. Controlla la scheda **Log**. 

> [!NOTE]  
> **Il Primo Avvio:** Durante la primissima esecuzione, l'Add-on impiegherà circa 30-40 secondi per scaricare i framework ufficiali dai server Apple e generare l'identità del Mac virtuale (`Provisioning done!`). Ai riavvii successivi, l'avvio sarà istantaneo.

### 🔌 Come collegarlo al FindMy MQTT Bridge

Una volta avviato, il server Anisette rimarrà in ascolto sulla porta `6969`.
Per farlo comunicare con il tuo *FindMy MQTT Bridge*, vai nella configurazione di quest'ultimo e inserisci l'indirizzo IP del tuo Home Assistant seguito dalla porta. 

**GUIDA  FindMy MQTT Bridge**: https://github.com/SalvatoreITA/home-assistant-addon/tree/main/findmy_mqtt

Esempio di URL da inserire nel FindMy Bridge:
`http://192.168.1.100:6969` *(Sostituisci l'IP con quello reale del tuo Home Assistant).*

> [!IMPORTANT]  
> **Identità Mac Persistente (Anti-Ban)** > Questo porting per Home Assistant è stato ottimizzato per salvare il *Device ID* generato in una memoria permanente (`/data`). Questo significa che, anche riavviando o aggiornando l'Add-on, Apple vedrà sempre lo stesso "Mac". Questo evita la moltiplicazione di dispositivi fantasma sul tuo account iCloud e riduce drasticamente il rischio di blocchi!

## ⚖️ Disclaimer & Limitazione di Responsabilità

**ATTENZIONE:** Questo progetto è rilasciato esclusivamente a **scopo didattico, di test e di ricerca personale**.

1. **Nessuna Affiliazione:** Questo progetto **NON è** in alcun modo affiliato, autorizzato, mantenuto, sponsorizzato o approvato da **Apple Inc.** o da una delle sue sussidiarie.
2. **Uso a proprio rischio:** L'interazione con i server Apple tramite sistemi non ufficiali costituisce una violazione dei Termini di Servizio (ToS) di Apple. L'utente si assume la piena responsabilità per l'utilizzo di questo software, inclusi potenziali blocchi temporanei o permanenti del proprio ID Apple. Si consiglia vivamente l'uso di un account iCloud dedicato ai test.
3. **Nessuna Garanzia:** Il software viene fornito "così com'è" (*As Is*), senza garanzie esplicite o implicite.

*Questo repository è destinato alla conservazione di prove di concetto (PoC) per l'interoperabilità tra sistemi IoT.*

## ❤️ Crediti

Questo porting per Home Assistant si basa su un lavoro eccezionale della community open-source:

* **[Salvatore Lentini](https://domhouse.it)**: Creazione della struttura, script di avvio e ottimizzazione Add-on per Home Assistant.
* **[Dadoum](https://github.com/Dadoum/anisette-v3-server)**: Autore originale dell'incredibile `anisette-v3-server`, cuore pulsante di questo progetto.
