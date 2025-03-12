import logging
import socketio
import telebot
import time
from threading import Timer

# Telegram bot token
TELEGRAM_BOT_TOKEN = '8105401955:AAGR_snjSPicJBcL4WoHgAm2X7g7802Lbns'
# Telegram chat ID
TELEGRAM_CHAT_ID = -1002459101321  # Numeric ID for the chat

# Telegram topic IDs
TELEGRAM_TOPIC_IDS = {
    'TamaGadget': 5,
    'SnowGlobe': 85,
    'CandyCane': 122,
    'WinterWreath': 522,
    'SantaHat': 584,
    'SignetRing': 566,
    'PreciousPeach': 572,
    'StarNotepad': 662,
    'PlushPepe': 596,
    'SpicedWine': 598,
    'JellyBunny': 586,
    'DurovsCap': 564,
    'PerfumeBottle': 600,
    'EternalRose': 602,
    'BerryBox': 578,
    'VintageCigar': 604,
    'MagicPotion': 606,
    'KissedFrog': 608,
    'HexPot': 610,
    'EvilEye': 612,
    'SharpTongue': 614,
    'TrappedHeart': 616,
    'SkullFlower': 618,
    'ScaredCat': 620,
    'SpyAgaric': 622,
    'HomemadeCake': 570,
    'GenieLamp': 624,
    'LunarSnake': 588,
    'PartySparkler': 582,
    'JesterHat': 592,
    'WitchHat': 626,
    'HangingStar': 628,
    'LoveCandle': 630,
    'CookieHeart': 632,
    'DeskCalendar': 634,
    'JingleBells': 636,
    'SnowMittens': 638,
    'VoodooDoll': 640,
    'MadPumpkin': 590,
    'HypnoLollipop': 642,
    'BDayCandle': 594,
    'BunnyMuffin': 644,
    'AstralShard': 646,
    'FlyingBroom': 648,
    'CrystalBall': 650,
    'EternalCandle': 652,
    'SwissWatch': 654,
    'GingerCookie': 580,
    'MiniOscar': 656,
    'LolPop': 658,
    'IonGem': 660,
    'LootBag': 664,
    'LovePotion': 568,
    'ToyBear': 666,
    'DiamondRing': 668,
    'TopHat': 674,
    'SleighBell': 672,
}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Initialize the Socket.IO client
sio = socketio.Client()

# Handle connection event
@sio.event
def connect():
    logger.info('Connected to the server')

# Handle disconnection event
@sio.event
def disconnect():
    logger.info('Disconnected from the server')

# Handle new messages from the server
def handle_message(data):
    logger.info(f'Получено сообщение: {data}')
    if isinstance(data, dict):
        gift_name = data.get('gift_name', 'Неизвестен')
        number = data.get('number', 'Неизвестен')
        model = data.get('Model', 'Неизвестен')
        backdrop = data.get('backdrop', 'Неизвестен')
        symbol = data.get('Symbol', 'Неизвестен')
        owner = data.get('owner', {})
        owner_name = owner.get('name', 'Неизвестен')
        quantity = data.get('Quantity', 'Неизвестен').replace('\xa0', ',')
        link = f"t.me/nft/{gift_name}-{number}"
        
        message = (f"🆕 *New Mint for {gift_name}!*"
                   f"\n\n🔢 *Number:* {number}"
                   f"\n\n*Model:* `{model}`"
                   f"\n*Backdrop:* `{backdrop}`"
                   f"\n*Symbol:* `{symbol}`"
                   f"\n\n👤 *Owner:* {owner_name}"
                   f"\n\n📊 *Availability:* {quantity}"
                   f"\n\n🔗 *Link to the gift -* {link}")
        
        if gift_name in TELEGRAM_TOPIC_IDS:
            bot.send_message(
                TELEGRAM_CHAT_ID, message, parse_mode='Markdown',
                message_thread_id=TELEGRAM_TOPIC_IDS[gift_name]
            )

@sio.on('*')
def catch_all(event, data):
    Timer(0.5, handle_message, [data]).start()

# Connect to the Socket.IO server
sio.connect('https://gsocket.trump.tg')

# Start the Socket.IO client
sio.wait()

# Start polling for Telegram bot
bot.polling(none_stop=True)