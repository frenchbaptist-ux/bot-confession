import json
import telebot

# Ton Token
TOKEN = '8762074916:AAFJYcaJx3vVOgP7PicJNLzfESWVFBbzgMo'

bot = telebot.TeleBot(TOKEN)

def charger_confession():
    try:
        with open('confession.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur de lecture du fichier JSON : {e}")
        return {}

confession_data = charger_confession()

@bot.message_handler(func=lambda message: True)
def send_paragraph(message):
    text = message.text
    bot_username = f"@{bot.get_me().username}"
    
    # ÉTAPE 1 : Est-ce qu'on est en groupe ou en privé ?
    is_group = message.chat.type in ['group', 'supergroup']
    
    # ÉTAPE 2 : On vérifie si on doit répondre
    if is_group:
        # En groupe : seulement si le message contient le nom du bot
        if bot_username in text:
            # On nettoie le texte pour ne garder que le chiffre (ex: "1.1")
            clean_text = text.replace(bot_username, "").strip()
        else:
            return # On ignore le message s'il n'y a pas le nom du bot
    else:
        # En privé : on prend le texte tel quel
        clean_text = text.strip()

    # ÉTAPE 3 : Analyse du chiffre (ex: 1.1)
    parts = clean_text.split('.')
    
    if len(parts) == 2:
        chapter_id = parts[0].strip()
        paragraph_id = parts[1].strip()
        
        if chapter_id in confession_data and paragraph_id in confession_data[chapter_id]:
            # ICI : Modification du tiret pour le tiret cadratin (—)
            text_to_send = f"« {confession_data[chapter_id][paragraph_id]} »\n\n— Confession de foi baptiste de Londres de 1689, {chapter_id}.{paragraph_id}."
            bot.reply_to(message, text_to_send)
        else:
            # Optionnel : envoyer une erreur seulement en privé pour ne pas polluer le groupe
            if not is_group:
                bot.reply_to(message, "Désolé, je ne trouve pas ce paragraphe. Veuillez user de la bonne syntaxe chapitre.paragraphe (ex : 1.1).")

print("Le bot est allumé... Tu peux lui parler sur Telegram !")
bot.infinity_polling()