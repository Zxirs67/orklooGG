import discord
from flask import Flask, request, jsonify
from threading import Thread

# --- CONFIGURATION ---
# Mets ICI ton token principal (celui qui a créé le bot/application Discord)
# Sans ça, le bot plantera au démarrage car il essaiera de se connecter avec un faux token.
MAIN_TOKEN = "TON_TOKEN_PRINCIPAL_ICI"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Variable globale : le token qui est actuellement "attaché" au bot
current_active_token = None

# --- SERVEUR FLASK ---
app = Flask(__name__)

@app.route('/assign', methods=['POST'])
def assign_token():
    global current_active_token
    
    data = request.get_json()
    
    if not data or 'token' not in data:
        return jsonify({"error": "Token manquant"}), 400

    new_token = data['token']
    current_active_token = new_token

    print(f"▶️ Token reçu et assigné ! Ancien token déconnecté.")

    # Lancer la connexion en arrière-plan
    def connect_new_token():
        try:
            # On crée un nouveau client Discord avec le token fourni par le site
            new_client = discord.Client(intents=intents, bot=False)
            
            @new_client.event
            async def on_ready():
                print(f'✅ Selfbot actif ! Connecté en tant que : {new_client.user}')
                # NOTE: Le bot va rester connecté tant que le token est valide.
                # Pour tester, il va rester "en vie". Si tu veux qu'il se déconnecte après,
                # il faudrait ajouter une logique de logout après un certain temps,
                # mais pour un selfbot "assigné", on le laisse tourner.
                
            import asyncio
            # On lance la boucle asynchrone pour ce nouveau client
            asyncio.run(run_bot_task(new_client, new_token))
        except Exception as e:
            print(f"Erreur de connexion avec le nouveau token : {e}")

    t = Thread(target=connect_new_token)
    t.start()
    
    return jsonify({"status": "assigné", "message": "Selfbot connecté avec le token fourni"}), 200

async def run_bot_task(bot_client, token):
    try:
        await bot_client.login(token)
        await bot_client.connect()
    except Exception as e:
        print(f"Impossible de rester connecté : {e}")

# --- POUR LANCER LE SERVEUR ---
if __name__ == "__main__":
    print("▶️ Démarrage du gestionnaire de selfbot en local...")
    print("🌐 Serveur d'écoute sur http://127.0.0.1:8080")
    print("En attente d'un token venant de ton site Netlify...")
    
    # On lance le serveur Flask
    app.run(host='127.0.0.1', port=8080)