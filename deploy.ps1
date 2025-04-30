# === Konfiguration ===
$NAO_IP = "169.254.14.127"
$NAO_USER = "nao"
$LOCAL_SCRIPT_PATH = "scripts\hello.py"
$REMOTE_SCRIPT_NAME = [System.IO.Path]::GetFileName($LOCAL_SCRIPT_PATH)
$REMOTE_PATH = "/home/nao/$REMOTE_SCRIPT_NAME"
$REMOTE_COMMAND = "/home/nao/.local/share/PackageManager/apps/python3-nao/bin/python3 $REMOTE_PATH"

# === Übertragung ===
Write-Host ">> Übertrage $LOCAL_SCRIPT_PATH -> ${NAO_USER}@${NAO_IP}:${REMOTE_PATH}"
scp $LOCAL_SCRIPT_PATH "${NAO_USER}@${NAO_IP}:${REMOTE_PATH}"

# === Ausführung (mit Loganzeige) ===
Write-Host ">> Starte ${REMOTE_PATH} auf dem NAO"
& ssh "${NAO_USER}@${NAO_IP}" $REMOTE_COMMAND
