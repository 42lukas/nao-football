#!/bin/bash

# Konfiguration – IP-Adresse deines NAO
NAO_IP="169.254.210.161"
NAO_USER="nao"

# Skript, das übertragen werden soll
SCRIPT="$1"

# Prüfen, ob ein Skript angegeben wurde
if [ -z "$SCRIPT" ]; then
  echo "❌ Bitte gib den Pfad zu deinem Python-Skript an."
  echo "➡ Beispiel: ./deploy.sh scripts/hello.py"
  exit 1
fi

# Pfad auf dem NAO, wohin das Skript kopiert wird
REMOTE_PATH="/home/nao/$(basename $SCRIPT)"

# Skript übertragen
echo "📤 Kopiere $SCRIPT nach $NAO_IP ..."
scp "$SCRIPT" $NAO_USER@$NAO_IP:"$REMOTE_PATH"

# Skript auf dem NAO ausführen
echo "🚀 Führe $SCRIPT auf dem NAO aus ..."
ssh $NAO_USER@$NAO_IP "python3 $REMOTE_PATH"