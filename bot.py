import json
import telebot
import os
from flask import Flask, request

# --- CONFIGURATION DU BOT ---
TOKEN = os.environ.get('BOT_TOKEN')
# L'URL de ton application Render (ex: https://mon-bot.onrender.com)
RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- LOGIQUE DE CHARGEMENT ---
def charger_confession():
    try:
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'confession.json')
        if not os.path.exists(path):
            print("Erreur : confession.json introuvable !")
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur chargement JSON : {e}")
        return {}

confession_data = charger_confession()

# --- ROUTES FLASK ---
@app.route('/')
def home():
    return "Le bot de la Confession 1689 est opérationnel via Webhook !", 200

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# --- HANDLERS DU BOT ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    try:
        me = bot.get_me()
        bot_username = f"@{me.username}"
    except:
        bot_username = ""
    
    is_group = message.chat.type in ['group', 'supergroup']
    
    if is_group:
        if bot_username in text:
            clean_text = text.replace(bot_username, "").strip()
        else:
            return
    else:
        clean_text = text

    if '.' in clean_text:
        parts = clean_text.split('.')
        if len(parts) == 2:
            c_id = parts[0].strip()
            p_id = parts[1].strip()
            if c_id in confession_data and p_id in confession_data[c_id]:
                rep = f"« {confession_data[c_id][p_id]} »\n\n— Confession de foi baptiste de Londres de 1689, {c_id}.{p_id}."
                bot.reply_to(message, rep)

# --- DÉMARRAGE ---
if __name__ == "__main__":
    # On retire le webhook existant au cas où
    bot.remove_webhook()
    
    # On définit le nouveau webhook
    # Render fournit l'URL via RENDER_EXTERNAL_URL si configuré
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    
    # On lance Flask (Render gère le port via la variable d'environnement)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
