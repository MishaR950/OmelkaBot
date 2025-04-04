# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging
import random
from datetime import time, datetime
import json
import os
import pytz  # Добавляем pytz для работы с часовыми поясами

# Токен от BotFather
TOKEN = '7498049015:AAFZSUpoomwEqY6uLOPPy-e6BL36taRVj3E'
CHANNEL_USERNAME = '@omellkas'

# Настройка логирования с кодировкой UTF-8
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Доступные колоды
DECKS = ["🌌 Космос подсознания", "🌟 Мне сейчас важно"]

# Карты для каждой колоды (file_id)
CARDS = {
    "Космос подсознания": [
        "AgACAgIAAxkBAAICXWftnX3lEGCM6i2rD1g7UDag-y2uAAKt6TEbaaBRS1DyWhzfB_MAAQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAICXGftnX015Au7c7e8xNUVqsxqZ-SAAAKs6TEbaaBRS7YBRftA1IlMAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICW2ftnX2qJAVHVZXYtpn8snn9jHOWAAKr6TEbaaBRS0AO5Ii3gyV5AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICWmftnX1PVSx2j94jOTe_0QvcBOr4AAKq6TEbaaBRS8mPjBvOVlynAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICWWftnX1dPhrwiQ9euY79mnNd9XMHAAKp6TEbaaBRS84VmBGuAvwAAQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAICWGftnX3Rp0UIMt6gzEvoCtGKk5WoAAKo6TEbaaBRS3cwJt9hMdN8AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICV2ftnX3XbGnf3r_CxOa5TLhyWK9PAAKn6TEbaaBRS0h8WLgLSrBvAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICVmftnX0WCuXym64OmTD8EOmKKwMqAAKl6TEbaaBRS49kZH_vp43gAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICVWftnX007LKt8-_9X4rHgmsI72ZcAAKg6TEbaaBRSyiNZC0-w58oAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICVGftnX3EtXazwjN18ReJ63OtocA8AAKX6TEbaaBRSxczKDByJRVfAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICU2ftnX1GUjhQvco87nVcIER2m8QXAAKm6TEbaaBRSyK3rJ6eCUOAAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICUmftnX0D216DavjlptbKSn8R-6wkAAKk6TEbaaBRSyj7Jme34TBYAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICUWftnX2f_xwHDGvQcs63Ke04M6qLAAKj6TEbaaBRS5vWuT9_gjCjAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICUGftnX3-eDofzFxtbko5YLlCC3PAAAKi6TEbaaBRS9FYMB3f45g2AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICT2ftnX0ERj5IF3SMh5C6wVgDd3PVAAKh6TEbaaBRS4OlCzwZR406AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICTmftnX0-iYTZ7iCI_x5YusURBXRNAAKf6TEbaaBRSy7Q2p7QzsJzAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICTWftnX0GWPLpO_Ac_qqcSyv3VPdEAAKe6TEbaaBRS0Sw3ioYvT8XAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICTGftnX1oqz9k7WabAAFeXR2glxqVRQACm-kxG2mgUUv-4h9UtpKDGAEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAICS2ftnX3sqqCYfYG2HoFvSdsJG78mAAKV6TEbaaBRS7nZOAIufV17AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICSmftnX3fCgVPU1VlXRWwhZDrjFNlAAKQ6TEbaaBRSyc4t9_jqljvAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICSWftnX2NC2dLNEKfiA1kv2EnQrrGAAKd6TEbaaBRS3PF6107JCMAAQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAICSGftnX2Uw6M36ZYW2K2loFNn8QJ6AAKc6TEbaaBRS8ZAZH_X31PjAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICR2ftnX1PqKCpD3yOLt04Nb7G_T23AAKa6TEbaaBRS_umwKeXNfdAAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICRmftnX1fQZrSK5PGJuXMMqaHfy49AAKZ6TEbaaBRS8n-rrh7NQswAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICRWftnX3sSWuKT8M4LiwxWSMNO_zjAAKY6TEbaaBRS9Xm6RrsYlRnAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICRGftnX2hVJOHFJMeTRuLD5294gQFAAKW6TEbaaBRSwb89sKKgOg7AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICQ2ftnX30ey6CO_zx6pOQq6dFmS1uAAKU6TEbaaBRS4zYUP2eC3_wAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICQmftnX1kcqL2qzWua6qiboIZg74hAAKT6TEbaaBRSx60GsmbBui5AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICQWftnX2X8OAXIHAyCVW9KkqxxhZPAAKR6TEbaaBRS0VtO0LT6A31AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICQGftnX3OiBxe9JKnkAuu-a11UtACAAKP6TEbaaBRS_i0yktBbR8dAQADAgADeQADNgQ"
    ],
    "Мне сейчас важно": [
        "AgACAgIAAxkBAAICGmftmV67VAlISVmTF8Tc9299u47bAAJI6jEbaaBRS_cAATx-Q9JL-wEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAICGWftmV6WHifKEpi7VA6AWOAp8gsPAAJH6jEbaaBRS2D2mrvgdkIvAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICGGftmV5ypUQ1IoK_F-pUvV3nPD2RAAJG6jEbaaBRS5ORTennfFnQAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICF2ftmV7L14l0xjL6Mikq040tXKRdAAJF6jEbaaBRS3hcly13DCVJAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICFmftmV6F_7fwXcpjdJJOSVJ4MiElAAJE6jEbaaBRSy6fnLa6myFtAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICFWftmV579FDd0_bfibaHr25SzO93AAJD6jEbaaBRS8SYXG1lNr7aAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICFGftmV4ClmOOauhzsjs0GmFXyydzAAJB6jEbaaBRSy9EoZcMeohYAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICE2ftmV57C2sTqukTD0MtAlyBh_lDAAJA6jEbaaBRS5l9BOLLQsbNAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICEmftmV4sNteie_D_9_trNq4oG4jAAAI_6jEbaaBRS_Ie2p6-ykwnAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICEWftmV4eApe6WdOYD3qcEInIauhHAAI-6jEbaaBRS48RVprcLux_AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICEGftmV54MgLX1FUFqdoWuRiBJNHoAAI96jEbaaBRS9OuMaYbacx3AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICD2ftmV4M2BpvK9g0aWVbvdnZK7UcAAI86jEbaaBRS6Ner3UCY23lAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICDmftmV7W8tU8HyMSpWcOsrnLs218AAI76jEbaaBRS44riTGmK6qcAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICDWftmV4-8SF2DT-69Z3aEp6wiQ2CAAI66jEbaaBRS_nwLhbW2eb8AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICDGftmV4qYTgsfhxHn2hc_wAB2lHMwQACOeoxG2mgUUutwVna_3sJwgEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAICC2ftmV6LdIz5ub1dLayZqZEHPGbpAAI46jEbaaBRS-YxzV2Dg7cEAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICCmftmV6iofNBTH4qfTkqeQ6C40KHAAI36jEbaaBRSz8JKdZsq6nyAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICCWftmV4LXFgWsv9lvraD2RzOIav2AAI26jEbaaBRS1uhxFkQwKpLAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICCGftmV53RBnaKDlMcuLMW9gBnvGCAAI16jEbaaBRS0gJAlhEqiH_AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICB2ftmV410swqesuQ_aTW7wqmjgk2AAI06jEbaaBRS-XQDBQNrNRBAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICBmftmV67nAh7rItlIShWzswAATZFIAACM-oxG2mgUUsjRvZkiHh1MAEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAICBWftmV49uiPYYqHfH7k_tgWE6R-oAAIy6jEbaaBRSyynEED_Yhj9AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICBGftmV4SPAkNpcUGCQ7fGFEOFKsoAAIx6jEbaaBRS9MRF0hSK3GkAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICA2ftmV7QnpWtw6Zkztu64HNtudMRAAIw6jEbaaBRS8zguIIB4u-pAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICAmftmV5kZxSAhitcEOmaT4zAmbICAAIv6jEbaaBRS60lKsvj8AOoAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICAWftmV4YZ6T-zb3mcH_G9QH8HDUNAAIu6jEbaaBRS-h8ozQ1dvb5AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAICAAFn7ZleL6kLm9n8u_mpDXyPMvvJGQACLeoxG2mgUUvlbZRWLMm2JgEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIB_2ftmV5z5Va7emoPsRGUKoY8xTdjAAIs6jEbaaBRS2WzQfMoqt_-AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB_mftmV72oE2M0y_V_4oS3Ar_glWsAAIr6jEbaaBRS3a9wx3_VxkrAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB_WftmV4LOilZy7V9qeQPkCmn0QMTAAIq6jEbaaBRS7cQQqytsgolAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB_GftmV5xsw6ofMLSCJ6hTsOuk8aLAAIo6jEbaaBRS5IGUJMQU8d3AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB-2ftmV4oULhBbeZsksDqxFn_OXfQAAIn6jEbaaBRS20f1HjCtHD8AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB-mftmV4kOn7A2dxJIFhx70DD7IxLAAIm6jEbaaBRS4pvWUmGXe0HAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB-WftmV6SQWreXO0dc3wCqB_572RcAAIl6jEbaaBRSzKGYeYk1CI6AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB-GftmV5ght2Vap68JpsZfEXHkPwJAAIk6jEbaaBRS68AAdRr6duyVwEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIB92ftmV7VgQvL2cl7KtfeMFfq2OnfAAIj6jEbaaBRSy9fSdcVm_ZiAQADAgADeQADNgQ"
    ]
}

# Функции для сохранения и загрузки bot_data
def save_bot_data(bot_data):
    users = bot_data.get('users', {})
    logging.info(f"Saving bot_data: {users}")
    # Используем путь для Render (если деплой на Render)
    file_path = '/app/data/users.json' if os.path.exists('/app/data') else 'users.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False)

def load_bot_data():
    file_path = '/app/data/users.json' if os.path.exists('/app/data') else 'users.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logging.info(f"Loaded bot_data: {data}")
            return data
    logging.info("No users.json found, starting with empty data")
    return {}

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="😔 Произошла ошибка. Попробуй снова!"
        )

# Инициализация: отправка кнопки "Старт" при запуске бота
async def init_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_chat or update.effective_chat.type != "private":
        logging.info("Ignoring non-private chat update in init_start")
        return

    user_id = str(update.effective_user.id)
    if 'users' in context.bot_data and user_id in context.bot_data['users']:
        del context.bot_data['users'][user_id]
        save_bot_data(context.bot_data)
        logging.info(f"User {user_id} removed from bot_data to start anew")

    await update.message.reply_text(
        "Удаляем старую клавиатуру...",
        reply_markup=ReplyKeyboardRemove()
    )

    reply_keyboard = [[KeyboardButton("🌟 Старт")]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Привет! Я бот Оли Евглевской. Нажми 'Старт', чтобы начать! 🌸",
        reply_markup=reply_markup
    )
    logging.info(f"Sent init message with Start button to user {user_id}")

# Старт (вызывается после нажатия кнопки "Старт")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and (not update.effective_chat or update.effective_chat.type != "private"):
        logging.info("Ignoring non-private chat update in start")
        return

    user_id = str(update.effective_user.id)
    if 'users' in context.bot_data and user_id in context.bot_data['users']:
        await menu(update, context)
        return

    context.user_data['deck'] = None
    context.user_data['subscribed'] = context.user_data.get('subscribed', False)

    welcome_text = (
        "🌸 *Привет, я Оля Евглевская!* 🌸\n"
        "Рада видеть тебя здесь! Чтобы начать волшебство, подпишись на мой канал:\n"
        "👉 https://t.me/omellkas\n"
        "---\n"
        "Готов? Нажми кнопку ниже!"
    )
    reply_keyboard = [[KeyboardButton("🚀 Проверить подписку")]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
    if update.message:
        await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
    elif update.callback_query:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    logging.info(f"User {user_id} started bot")

# Проверка подписки
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_chat or update.effective_chat.type != "private":
        logging.info("Ignoring non-private chat update in check_subscription")
        return

    user_id = str(update.effective_user.id)
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            context.user_data['subscribed'] = True
            context.user_data['deck'] = None
            if 'users' not in context.bot_data:
                context.bot_data['users'] = {}
            context.bot_data['users'][user_id] = {'deck': None, 'last_card_date': None}
            save_bot_data(context.bot_data)
            reply_keyboard = [
                [KeyboardButton("🌌 Космос подсознания"), KeyboardButton("🌟 Мне сейчас важно")],
                [KeyboardButton("📜 Меню")]
            ]
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
            await update.message.reply_text(
                "🎉 *Ура, ты с нами!* 🎉\n"
                "Теперь каждый день я буду присылать тебе 'Карту дня'.\n"
                "✨ Выбери колоду:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "🌟 Пока не вижу тебя среди подписчиков!\n"
                "Подпишись сюда: https://t.me/omellkas"
            )
    except Exception as e:
        logging.error(f"Error checking subscription for {user_id}: {str(e)}")
        await update.message.reply_text("😔 Что-то пошло не так. Попробуй ещё раз!")

# Функция отправки карты одному пользователю
async def send_card_to_user(user_id: str, deck: str, context: ContextTypes.DEFAULT_TYPE):
    if deck and deck in CARDS:
        card_url = random.choice(CARDS[deck])
        card_text = (
            "🃏 *Карта дня от Оли Евглевской* 🃏\n"
            f"Колода: {deck}\n"
            "✨ Подумай, что она тебе говорит!"
        )
        try:
            logging.info(f"Sending card to user {user_id}: {card_url}")
            await context.bot.send_photo(user_id, photo=card_url, caption=card_text, parse_mode='Markdown')
            logging.info(f"Successfully sent card to user {user_id}")
        except Exception as e:
            logging.error(f"Error sending card to {user_id}: {str(e)}")
            await context.bot.send_message(user_id, "😔 Не удалось отправить карту. Попробую завтра!")

# Обработка выбора колоды через reply-кнопки
async def handle_deck_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, deck: str):
    if not update.message or not update.effective_chat or update.effective_chat.type != "private":
        logging.info("Ignoring non-private chat update in handle_deck_selection")
        return

    user_id = str(update.effective_user.id)
    context.user_data['deck'] = deck
    if 'users' in context.bot_data and user_id in context.bot_data['users']:
        context.bot_data['users'][user_id]['deck'] = deck
        context.bot_data['users'][user_id]['last_card_date'] = datetime.now().strftime('%Y-%m-%d')
    else:
        context.bot_data['users'][user_id] = {'deck': deck, 'last_card_date': datetime.now().strftime('%Y-%m-%d')}
    save_bot_data(context.bot_data)

    await send_card_to_user(user_id, deck, context)
    logging.info(f"Sent first card to new user {user_id} after deck selection")

    reply_keyboard = [[KeyboardButton("📜 Меню")]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text(
        f"🌈 *Ты выбрал колоду: {deck}!*\n"
        "Я только что отправила тебе первую карту. Теперь каждый день жди новую карту в 9:00 утра. Открой меню, чтобы продолжить!",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    logging.info(f"User {user_id} selected deck: {deck}")

# Меню
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and (not update.effective_chat or update.effective_chat.type != "private"):
        logging.info("Ignoring non-private chat update in menu")
        return

    user_id = str(update.effective_user.id)
    if 'users' in context.bot_data and user_id in context.bot_data['users']:
        context.user_data['deck'] = context.bot_data['users'][user_id]['deck']
    else:
        context.user_data['deck'] = None

    message = update.message if update.message else update
    if not context.user_data.get('subscribed', False):
        await message.reply_text("🌟 Подпишись на канал: https://t.me/omellkas")
        return
    if not context.user_data.get('deck'):
        reply_keyboard = [
            [KeyboardButton("🌌 Космос подсознания"), KeyboardButton("🌟 Мне сейчас важно")],
            [KeyboardButton("📜 Меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
        await message.reply_text(
            "🌟 Ты ещё не выбрал колоду! Давай выберем:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        return
    keyboard = [
        [InlineKeyboardButton("🔄 Сменить колоду", callback_data='change_deck')],
        [InlineKeyboardButton("ℹ️ О метафорических картах", callback_data='meta_info')],
        [InlineKeyboardButton("🔄 Перезапустить", callback_data='restart')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(
        "📜 *Меню от Оли Евглевской*\n"
        "Что хочешь сделать?",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Обработка кнопок меню
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'change_deck':
        await query.message.delete()
        reply_keyboard = [
            [KeyboardButton("🌌 Космос подсознания"), KeyboardButton("🌟 Мне сейчас важно")],
            [KeyboardButton("📜 Меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
        await query.message.reply_text(
            "🌟 Пора выбрать новую колоду:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    elif query.data == 'meta_info':
        meta_text = (
            "ℹ️ *Метафорические карты — что это?*\n"
            "Это волшебный способ заглянуть в своё подсознание через образы. Они помогают найти ответы и вдохновение!\n"
            "---\n"
            "Хочешь узнать, какие вопросы им задавать?"
        )
        keyboard = [
            [InlineKeyboardButton("🌟 Да", callback_data='meta_questions_yes'),
             InlineKeyboardButton("🌙 Нет", callback_data='meta_questions_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(meta_text, parse_mode='Markdown', reply_markup=reply_markup)

    elif query.data == 'restart':
        user_id = str(update.effective_user.id)
        if 'users' in context.bot_data and user_id in context.bot_data['users']:
            del context.bot_data['users'][user_id]
            save_bot_data(context.bot_data)
        await query.message.delete()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Удаляем старую клавиатуру...",
            reply_markup=ReplyKeyboardRemove()
        )
        await start(update, context)

    elif query.data == 'meta_questions_yes':
        await query.edit_message_text(
            "❓ *Вопросы для метафорических карт:*\n"
            "✨ Что мне нужно сегодня?\n"
            "🌿 Какой у меня ресурс?\n"
            "🌙 Что ждёт меня впереди?",
            parse_mode='Markdown'
        )
    elif query.data == 'meta_questions_no':
        await query.edit_message_text("🌸 Хорошо, давай вернёмся к меню!")
        fake_update = Update(update_id=update.update_id, message=query.message)
        await menu(fake_update, context)

# Карта дня (ежедневная отправка)
async def send_daily_card(context: ContextTypes.DEFAULT_TYPE):
    logging.info("Starting send_daily_card function")
    users = context.bot_data.get('users', {})
    logging.info(f"Found {len(users)} users in bot_data")
    current_date = datetime.now().strftime('%Y-%m-%d')

    for user_id in users:
        user_data = users[user_id]
        deck = user_data.get('deck')
        last_card_date = user_data.get('last_card_date')

        if last_card_date == current_date:
            logging.info(f"Skipping user {user_id}: already received card today")
            continue

        if deck and deck in CARDS:
            await send_card_to_user(user_id, deck, context)
            context.bot_data['users'][user_id]['last_card_date'] = current_date
            save_bot_data(context.bot_data)
        else:
            logging.info(f"Skipping user {user_id}: no deck selected or invalid deck")

# Команда для ручного вызова send_daily_card (для теста)
async def test_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_chat or update.effective_chat.type != "private":
        logging.info("Ignoring non-private chat update in test_card")
        return

    user_id = str(update.effective_user.id)
    if 'users' in context.bot_data and user_id in context.bot_data['users']:
        context.user_data['deck'] = context.bot_data['users'][user_id]['deck']
    else:
        context.user_data['deck'] = None

    if not context.user_data.get('subscribed', False):
        await update.message.reply_text("🌟 Подпишись на канал: https://t.me/omellkas")
        return
    logging.info(f"User {user_id} called /testcard with deck {context.user_data['deck']}")
    await send_daily_card(context)

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_chat or update.effective_chat.type != "private":
        logging.info("Ignoring non-private chat update in handle_message")
        return

    user_id = str(update.effective_user.id)
    if 'users' in context.bot_data and user_id in context.bot_data['users']:
        context.user_data['deck'] = context.bot_data['users'][user_id]['deck']
    else:
        context.user_data['deck'] = None

    text = update.message.text
    if text == "🌟 Старт":
        await start(update, context)
    elif text == "🚀 Проверить подписку":
        await check_subscription(update, context)
    elif text == "📜 Меню":
        await menu(update, context)
    elif text in DECKS:
        deck_name = text.split(' ', 1)[1]
        await handle_deck_selection(update, context, deck_name)
    else:
        await update.message.reply_text("🌟 Используй кнопки, чтобы общаться со мной!")

# Главная функция
def main():
    application = Application.builder().token(TOKEN).build()
    application.bot_data['users'] = load_bot_data()
    application.add_handler(CommandHandler("start", init_start))
    application.add_handler(CommandHandler("testcard", test_card))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, handle_message))
    application.add_handler(CallbackQueryHandler(button))
    application.add_error_handler(error_handler)

    # Запускаем ежедневную отправку карт в 9:00 по местному времени
    if application.job_queue:
        local_tz = pytz.timezone('Europe/Moscow')  # Замени на свой часовой пояс
        local_time = time(hour=9, minute=0, tzinfo=local_tz)
        application.job_queue.run_daily(send_daily_card, time=local_time)
        logging.info("Scheduled daily card sending at 9:00 AM (local time, Europe/Moscow)")

    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()