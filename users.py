import telebot
from telebot import types
import uuid
import utils
import io
from utils import get_count
import os


users = {}

class Toggler:

    def __init__(self, options: dict[str, str]) -> None:
        self.options = options



class UserToggler:
    LIST: dict[str, 'UserToggler'] = {}

    def __init__(self,
                 toggler: Toggler,
                 user: 'User') -> None:
        self.toggler = toggler
        self.user = user
        self.id = str(uuid.uuid4())

        self.LIST[self.id] = self
        self.user.toggler = self

        self.markup: types.InlineKeyboardMarkup | None = None
        self.message: types.Message | None = None

        self.states: dict[str, bool] = {
            option: False
            for option in toggler.options
        }


    def __getitem__(self, option: str) -> bool:
        return self.states[option]
    

    @property
    def choices(self) -> list[str]:
        return [option for option, isset in self.states.items() if isset]


    def get_markup(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 2
        buttons = []

        for option, isset in self.states.items():
            callback_data = f'toggle:{self.id}:{option}'
            logo = '[' + ('✅' if isset else '❌') + ']'
            name = self.toggler.options[option]

            buttons.append(
                types.InlineKeyboardButton(
                    f'{name} {logo}', callback_data=callback_data
                )
            )

        markup.add(*buttons)
        markup.keyboard.extend(self.markup.keyboard)
        return markup


    def set_message(self, msg: types.Message) -> None:
        self.message = msg


    def set_markup(self, markup: types.InlineKeyboardMarkup) -> None:
        self.markup = markup



class Togglers:
    CHECK = Toggler({
        'amazon': ' Amazon (NL/ML)',
        'netflix': 'Netflix (NL)'
        #'disney': 'Disney (ML)'
    }) 

    GEN = Toggler({
    'fr': 'France 🇫🇷',
    'en': 'Angleterre 🏴󠁧󠁢󠁥󠁮󠁧󠁿',
    'it': 'Italie 🇮🇹',
    'ch': 'Suisse 🇨🇭',
    'be': 'Belgique 🇧🇪',
    'de': 'Allemagne 🇩🇪',
    'lu': 'Luxembourg 🇱🇺',
    'es': 'Espagne 🇪🇸',
    'ae': 'United Arab Emirates 🇦🇪',
    'sa': 'Saudi Arabia 🇸🇦',
    'qa': 'Qatar 🇶🇦',
    'bh': 'Bahrain 🇧🇭',
    'my': 'Malaysia 🇲🇾',
    'sg': 'Singapore 🇸🇬',
    'am': 'Armenia 🇦🇲',
    'ge': 'Georgia 🇬🇪',
    'co': 'Colombia 🇨🇴',
    'no': 'Norway 🇳🇴',
    'il': 'Israel 🇮🇱',
    'cy': 'Cyprus 🇨🇾',
    'dk': 'Denmark 🇩🇰',
    'is': 'Iceland 🇮🇸',
    'nl': 'Netherlands 🇳🇱',
    'lu': 'Luxembourg 🇱🇺',
    'mc': 'Monaco 🇲🇨',
    'fi': 'Finland 🇫🇮',
    'hu': 'Hungary 🇭🇺',
    'za': 'South Africa 🇿🇦',
    'se': 'Sweden 🇸🇪',
    'uk': 'United Kingdom 🇬🇧',
    'cz': 'Czech Republic 🇨🇿',
    'kw': 'Kuwait 🇰🇼',
    'lv': 'Lettonie 🇱🇻',
    'pt': 'Portugal 🇵🇹',
    'au': 'Australia 🇦🇺',
    'at': 'Autriche 🇦🇹'
})



class User:
    

    LIST: dict[int, 'User'] = {}

    def __init__(self,
                 tlg: types.User,
                 bot: telebot.TeleBot) -> None:
        self.tlg = tlg
        self.bot = bot
        self.id = tlg.id

        self.end = False

        self.panel: types.Message | None = None
        self.toggler: UserToggler | None = None
        self.export = False

        self.LIST[self.id] = self
        self.checker: utils.Checker | None = None
        self.to_delete: list[types.Message] = []

        self.new = False
        self.finish = False


    def wait_for_msg(self, last_msg: types.Message) -> types.Message:

        self.end = False
        message = None
        def get_msg(msg: types.Message):
            nonlocal message
            message = msg
            self.end = True

        self.bot.register_next_step_handler(last_msg, get_msg)

        while not self.end:
            pass

        # self.bot.clear_step_handler_by_chat_id(last_msg.chat.id)

        # self.bot.delete_message(last_msg.chat.id, last_msg.id)
        return message
    


    def send(self,
             text: str,
             markup: types.InlineKeyboardMarkup | None = None) -> types.Message:
        
        self.bot.edit_message_text(
            text,
            self.panel.chat.id,
            self.panel.id,
            reply_markup=markup,
            parse_mode='markdown'
        )
        return self.panel


    def send_fr(self,
             text: str,
             markup: types.InlineKeyboardMarkup | None = None) -> types.Message:
        self.panel = self.bot.send_message(
            self.id,
            text,
            reply_markup=markup,
            parse_mode='markdown'
        )
        return self.panel
    
    
    def delete_panel(self) -> None:
        self.bot.delete_message(self.id, self.panel.id)


    def export_checked(self) -> None:
     export_folder = 'exportNL'
     if not os.path.exists(export_folder):
         os.makedirs(export_folder)

     for service, result in self.checker.result.items():
         valids = [num for num, valid in result.items() if valid]
         if not valids:
             continue

         nb = str(round(len(valids)/1000, 2)).removesuffix('.0').removesuffix('.00')
         file_name = f"{nb}K {service}.txt"
         file_path = os.path.join(export_folder, file_name)

         with open(file_path, 'w') as file:
             file.write('\n'.join(valids))

         message = self.bot.send_document(self.id, types.InputFile(file_path))
         self.checker.export_messages.append(message)