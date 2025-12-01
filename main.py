from flask import Flask, request, render_template_string
import time

app = Flask(__name__)

# Hier speichern wir die HWIDs: { "HWID": TIMESTAMP }
authorized_hwids = {}

# Wie lange soll der Key halten? (24 Stunden in Sekunden)
DURATION = 86400 

def cleanup_old_keys():
    """Löscht abgelaufene HWIDs um Speicher zu sparen"""
    current_time = time.time()
    to_remove = [hwid for hwid, timestamp in authorized_hwids.items() if current_time - timestamp > DURATION]
    for k in to_remove:
        del authorized_hwids[k]

# --- HTML DESIGN FÜR DIE VERIFY SEITE ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Script Verification</title>
    <style>
        body { background-color: #1a1a1a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background-color: #2b2b2b; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.5); text-align: center; }
        h2 { color: #00ff88; }
        .btn { background-color: #008cff; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 5px; cursor: pointer; transition: 0.3s; }
        .btn:hover { background-color: #006bbd; }
        .info { margin-top: 15px; font-size: 12px; color: #888; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Antibot Verification</h2>
        <p>Bitte bestätige, dass du ein Mensch bist.</p>
        <br>
        <form method="POST" action="/verify_action">
            <input type="hidden" name="hwid" value="{{ hwid }}">
            <button type="submit" class="btn">Ich bin kein Roboter (VERIFY)</button>
        </form>
        <p class="info">Deine HWID: {{ hwid }}</p>
    </div>
</body>
</html>
"""

HTML_SUCCESS = """
<!DOCTYPE html>
<html>
<body style="background-color: #1a1a1a; color: #00ff88; text-align: center; padding-top: 100px; font-family: sans-serif;">
    <h1>Erfolgreich verifiziert!</h1>
    <p style="color: white;">Du hast nun für 24 Stunden Zugriff.</p>
    <p>Geh zurück in das Spiel und drücke "Check Key".</p>
</body>
</html>
"""

@app.route('/')
def home():
    return "Server is online."

# Das ist die Seite, auf die der User nach Linkvertise kommt
@app.route('/auth')
def auth_page():
    hwid = request.args.get('hwid')
    if not hwid:
        return "Fehler: Keine HWID gefunden. Bitte starte das Script neu."
    return render_template_string(HTML_PAGE, hwid=hwid)

# Das passiert, wenn man den Knopf drückt
@app.route('/verify_action', methods=['POST'])
def verify_action():
    hwid = request.form.get('hwid')
    if hwid:
        cleanup_old_keys() # Alte Keys löschen
        authorized_hwids[hwid] = time.time() # HWID whitelisten
        return render_template_string(HTML_SUCCESS)
    return "Fehler."

# Das Roblox Script fragt hier an
@app.route('/check_status')
def check_status():
    hwid = request.args.get('hwid')
    cleanup_old_keys()
    
    if hwid in authorized_hwids:
        # Prüfen ob 24h vorbei sind
        if time.time() - authorized_hwids[hwid] < DURATION:
            return "true"
    
    return "false"

# Hier kommt dein eigentliches Script rein (Raw Text)
@app.route('/get_script')
def get_script():
    hwid = request.args.get('hwid')
    if hwid in authorized_hwids:
         # HIER DEIN SCRIPT EINFÜGEN:
        return """
        print("Hello World! Das Script wurde geladen.")
        game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = 50
        """
    return "print('Zugriff verweigert!')"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)