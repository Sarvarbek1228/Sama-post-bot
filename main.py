import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import httpx
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8024656591:AAHG9PWLQkVnnSGtyhnKPqIEbBQqV63wG7U"

CHANNELS = {
    "Andijon": "@Andijon_nomoz_vaqti",
    "Namangan": "@Namangan_nomoz",
    "Toshkent": "@Toshkent_nomoz",
    "Fargona": "@fargona_nomoz_vaqtlari"
}

VILOYAT_COORDINATES = {
    "Andijon": (40.7829, 72.3442),
    "Namangan": (41.0000, 71.6667),
    "Toshkent": (41.2995, 69.2401),
    "Fargona": (40.3780, 71.7843),
}

CHANNEL_USERNAMES = "\n".join(CHANNELS.values())

async def get_prayer_times(lat: float, lon: float):
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        if data["code"] != 200:
            raise Exception("Namoz vaqtlarini olishda xatolik")
        return data["data"]["timings"]

def format_prayer_times(viloyat: str, timings: dict) -> str:
    text = f"🕌 Namoz vaqtlari — {viloyat}\n\n"
    text += f"Bomdod: {timings.get('Fajr')}\n"
    text += f"Quyosh: {timings.get('Sunrise')}\n"
    text += f"Peshin: {timings.get('Dhuhr')}\n"
    text += f"Asr: {timings.get('Asr')}\n"
    text += f"Shom: {timings.get('Maghrib')}\n"
    text += f"Xufton: {timings.get('Isha')}\n\n"
    text += CHANNEL_USERNAMES
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Namoz vaqtini yuborish", callback_data='send_prayer_times')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Assalomu alaykum!\nNamoz vaqtlarini olish uchun quyidagi tugmani bosing.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'send_prayer_times':
        bot = context.bot
        # 4 ta kanalga namoz vaqtlarini alohida yuborish
        for viloyat, channel in CHANNELS.items():
            lat, lon = VILOYAT_COORDINATES[viloyat]
            try:
                timings = await get_prayer_times(lat, lon)
                msg = format_prayer_times(viloyat, timings)
                await bot.send_message(chat_id=channel, text=msg)
                logger.info(f"{viloyat} uchun namoz vaqtlari kanalga yuborildi.")
            except Exception as e:
                logger.error(f"{viloyat} uchun namoz vaqtini olishda xatolik: {e}")
        await query.edit_message_text("Namoz vaqtlarini barcha kanallarga yubordim ✅")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot ishga tushdi.")
    app.run_polling()
