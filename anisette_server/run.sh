#!/bin/sh
set -e

echo "==============================================================="
echo "  🍏 AVVIO APPLE ANISETTE SERVER (Home Assistant Edition) 🍏  "
echo "               Salvatore Lentini - DomHouse.it                 "
echo "==============================================================="

echo "📁 Configurazione volumi e permessi permanenti..."
mkdir -p /data/anisette-v3
chmod -R 777 /data/anisette-v3

echo "🔗 Creazione ponte per l'identità del Mac Virtuale..."
# 1. Creiamo la cartella padre altrimenti Linux si arrabbia!
mkdir -p /root/.config

# 2. Rimuoviamo eventuali vecchi file
rm -rf /root/.config/anisette-v3

# 3. Creiamo il ponte con l'intera cartella (Device ID + Framework)
ln -sf /data/anisette-v3 /root/.config/anisette-v3

echo "🚀 Avvio server Anisette in ascolto sulla porta 6969..."
exec /opt/anisette-v3-server -n 0.0.0.0 -p 6969
