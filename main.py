import json
import os
import asyncio
from datetime import datetime
from pytz import timezone
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ==== Asosiy sozlamalar ====
BOT_TOKEN = "7571307271:AAFB103UF5aDX_vV83xKUOVHHM3kePNiLCI"
CHANNEL_ID = "@kiyim_para_kiyim"
GROUP_IDS = [-4883073648, -4982748525]  # Futbolka va Hudi guruhlari
MEDIA_FILE = "media_store.json"

# ==== Media saqlash ====
def load_media():
    if os.path.exists(MEDIA_FILE):
        with open(MEDIA_FILE, "r") as f:
            return json.load(f)
    return {group_id: {"photos": [], "videos": [], "index": 0} for group_id in GROUP_IDS}

def save_media(media):
    with open(MEDIA_FILE, "w") as f:
        json.dump(media, f)

media_storage = load_media()

def add_media(group_id, media_type, file_id):
    if group_id not in media_storage:
        media_storage[group_id] = {"photos": [], "videos": [], "index": 0}
    media_storage[group_id][media_type + "s"].append(file_id)
    save_media(media_storage)

def get_next_media(group_id):
    group_data = media_storage.get(group_id, {"photos": [], "videos": [], "index": 0})
    combined = [{"type": "photo", "file_id": f} for f in group_data.get("photos", [])] + \
               [{"type": "video", "file_id": f} for f in group_data.get("videos", [])]
    if not combined:
        return None
    index = group_data.get("index", 0) % len(combined)
    media_storage[group_id]["index"] = index + 1
    save_media(media_storage)
    return combined[index]

# ==== Mediani qabul qilish ====
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        add_media(group_id, "photo", file_id)
        print(f"{group_id} dan RASM olindi.")
    elif update.message.video:
        file_id = update.message.video.file_id
        add_media(group_id, "video", file_id)
        print(f"{group_id} dan VIDEO olindi.")

# ==== Kanalga yuborish ====
async def post_to_channel():
    FUTBOLKA_TEXT = (
        "👕 FUTBOLKA KO'YLAKLAR\n\n"
        "🖤 Ranglar: Oq | Qora\n"
        "📏 Modellar: Oversize | Oddiy\n\n"
        "💸 Narxlar:\n"
        "• Oddiy — 100 000 so‘m\n"
        "• Oversize — 190 000 so‘m\n\n"
        "🎨 Siz istagan dizaynda tayyorlaymiz\n"
        "🚚 O‘zbekiston bo‘ylab 12 viloyatga pochta orqali yetkazib beramiz\n\n"
        "✨ SAMA PRINT — mehr va xotiralarni muhrlab beruvchi manzil."
    )

    HUDI_TEXT = (
        "🧥 HUDILAR\n\n"
        "🖤 Ranglar: Oq | Qora\n"
        "📏 Modellar: Oversize | Oddiy\n\n"
        "💸 Narxlar:\n"
        "• Oddiy — 190 000 so‘m\n"
        "• Oversize — 240 000 so‘m\n\n"
        "🎨 Siz istagan dizaynda tayyorlaymiz\n"
        "🚚 O‘zbekiston bo‘ylab 12 viloyatga pochta orqali yetkazib beramiz\n\n"
        "✨ SAMA PRINT — mehr va xotiralarni muhrlab beruvchi manzil."
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛒 Sotib olish", url="https://t.me/sama_pr7nt"),
            InlineKeyboardButton("📸 Instagramdan kuzatish", url="https://instagram.com/sama_pr1nt")
        ]
    ])

    bot = Bot(BOT_TOKEN)

    for group_id in GROUP_IDS:
        media = get_next_media(group_id)
        if not media:
            print(f"{group_id} dan media topilmadi.")
            continue
        try:
            caption = FUTBOLKA_TEXT if group_id == -4883073648 else HUDI_TEXT
            if media['type'] == 'photo':
                await bot.send_photo(chat_id=CHANNEL_ID, photo=media['file_id'], caption=caption, reply_markup=keyboard)
                print(f"{group_id} dan kanalga RASM yuborildi.")
            elif media['type'] == 'video':
                await bot.send_video(chat_id=CHANNEL_ID, video=media['file_id'], caption=caption, reply_markup=keyboard)
                print(f"{group_id} dan kanalga VIDEO yuborildi.")
        except Exception as e:
            print(f"{group_id} dan media yuborishda xatolik: {e}")

# ==== Botni ishga tushirish ====
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Chat(GROUP_IDS) & (filters.PHOTO | filters.VIDEO), handle_media))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_to_channel, 'cron', hour=13, minute=2, timezone=timezone('Asia/Tashkent'))
    scheduler.add_job(post_to_channel, 'cron', hour=18, minute=42, timezone=timezone('Asia/Tashkent'))
    scheduler.start()

    print("🤖 Bot Railway'da ishga tushdi.")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
