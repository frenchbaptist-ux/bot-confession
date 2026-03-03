import json
import telebot
import os
from flask import Flask
from threading import Thread

# --- SERVEUR DE MAINTIEN POUR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Le bot est en ligne !"

def run():
    # Utilise le port 8080 par défaut si non spécifié par Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """Lance le serveur web en arrière-plan"""
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- LOGIQUE DU BOT ---
# Récupération du Token (BOT_TOKEN)
TOKEN = os.environ.get('BOT_TOKEN', '8762074916:AAFJYcaJx3vVOgP7PicJNLzfESWVFBbzgMo')
bot = telebot.TeleBot(TOKEN)

def charger_confession():
    try:
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'confession.json')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur : {e}")
        return {}

confession_data = charger_confession()

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
            chap = parts[0].strip()
            para = parts[1].strip()
            if chap in confession_data and para in confession_data[chap]:
                res = f"« {confession_data[chap][para]} »\n\n— Confession de 1689, {chap}.{para}."
                bot.reply_to(message, res)

if __name__ == "__main__":
    print("Démarrage du serveur...")
    keep_alive()
    print("Bot en ligne !")
    bot.infinity_polling()
                bot.reply_to(message, "Désolé, je ne trouve pas ce paragraphe. Veuillez user de la bonne syntaxe chapitre.paragraphe (ex : 1.1).")

print("Le bot est allumé... Tu peux lui parler sur Telegram !")
bot.infinity_polling()
