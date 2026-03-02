# 🚀 FindMy MQTT Bridge

Questo Add-on ti permette di tracciare i tuoi Apple AirTag, iPhone, iPad e Mac direttamente su Home Assistant!

## ⚙️ Configurazione
1. Compila l'Apple ID e la Password.
2. Inserisci l'URL del tuo server Anisette locale (es. `http://IP:6969`).
3. Carica i file `.plist` dei tuoi dispositivi nella cartella condivisa `/share/findmy/keys`.

## ⚠️ Primo Avvio (Codice 2FA)
Se Apple ti chiede il codice a due fattori, l'Add-on si metterà in pausa. Crea un file di testo in `/share/findmy/2fa_code.txt`, scrivici dentro le 6 cifre e salvalo. L'Add-on lo leggerà automaticamente!

---
Sviluppato da **Salvatore Lentini - DomHouse.it**
