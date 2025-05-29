import random
from datetime import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from apscheduler.schedulers.blocking import BlockingScheduler

# TOKEN va chat ID lar
TOKEN = '7571307271:AAFB103UF5aDX_vV83xKUOVHHM3kePNiLCI'
CHANNEL_ID = '@kiyim_para_kiyim'
HOODIE_GROUP_ID = -4982748525
TSHIRT_GROUP_ID = -4883073648

# Tugmalar
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🛒 Sotib olish", url="https://t.me/sama_pr7nt")],
    [InlineKeyboardButton("💬 Maslahatlashish", url="https://t.me/sama_pr7nt")]
])

# Matnlar
hoodie_caption = """2 xil rangda oq va qora 
2 xil modelda oversize va oddiy
oddiy: 190 ming
oversize: 240 ming

siz aytgan dizaynda tayyorlab beramiz
12 ta viloyatga pochta orqali yetkazib beramiz

SAMA PRINT – mehr va xotiralarni muhrlab beruvchi manzil"""
tshirt_caption = """2 xil rangda oq va qora 
2 xil modelda oversize va oddiy
oddiy: 100 ming
oversize: 190 ming

siz aytgan dizaynda tayyorlab beramiz
12 ta viloyatga pochta orqali yetkazib beramiz

SAMA PRINT – mehr va xotiralarni muhrlab beruvchi manzil"""

bot = Bot(token=TOKEN)
posted_photos = {"hoodie": [], "tshirt": []}

def get_random_photo(group_id, already_posted):
    updates = bot.get_updates()
    photo_messages = []

    for update in updates:
        if update.message and update.message.chat.id == group_id:
            if update.message.photo:
                file_id = update.message.photo[-1].file_id
                if file_id not in already_posted:
                    photo_messages.append(file_id)

    if not photo_messages:
        return None

    chosen = random.choice(photo_messages)
    already_posted.append(chosen)
    if len(already_posted) > 10:
        already_posted.pop(0)
    return chosen

def post_photo():
    try:
        # Hoodie
        photo1 = get_random_photo(HOODIE_GROUP_ID, posted_photos["hoodie"])
        if photo1:
            bot.send_photo(chat_id=CHANNEL_ID, photo=photo1, caption=hoodie_caption, reply_markup=keyboard)
        
        # T-shirt
        photo2 = get_random_photo(TSHIRT_GROUP_ID, posted_photos["tshirt"])
        if photo2:
            bot.send_photo(chat_id=CHANNEL_ID, photo=photo2, caption=tshirt_caption, reply_markup=keyboard)

        print("Postlar yuborildi.")
    except TelegramError as e:
        print(f"Xatolik: {e}")

scheduler = BlockingScheduler()
scheduler.add_job(post_photo, 'cron', hour=18, minute=30)
print("Bot ishga tushdi. Har kuni 18:30 da post yuboriladi.")
scheduler.start()
