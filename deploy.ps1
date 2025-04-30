# === Konfiguration ===
$NAO_IP = "169.254.14.127"
$NAO_USER = "nao"
$LOCAL_SCRIPT_PATH = "scripts\hello.py"
$REMOTE_SCRIPT_NAME = [System.IO.Path]::GetFileName($LOCAL_SCRIPT_PATH)

# === Übertragung ===
Write-Host "📤 Übertrage $LOCAL_SCRIPT_PATH → $NAO_USER@$NAO_IP:/home/nao/$REMOTE_SCRIPT_NAME"
scp $LOCAL_SCRIPT_PATH "$NAO_USER@$NAO_IP:/home/nao/$REMOTE_SCRIPT_NAME"

# === Ausführung (mit Loganzeige) ===
Write-Host "🚀 Starte /home/nao/$REMOTE_SCRIPT_NAME auf dem NAO"
ssh $NAO_USER@$NAO_IP "/home/nao/.local/share/PackageManager/apps/python3-nao/bin/python3 /home/nao/$REMOTE_SCRIPT_NAME"