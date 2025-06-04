import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# === Sozlamalar ===
TOKEN = "7633206691:AAGFxRSHrsf99Png8nYtBKvBUyEZNo0xmX0"
DATA_FOLDER = "data"

# === Boshlang‘ich menyu ===
def start(update: Update, context: CallbackContext):
    books = sorted(os.listdir(DATA_FOLDER))
    keyboard = [[book] for book in books]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("📚 Kitobni tanlang:", reply_markup=reply_markup)

# === Kitob tanlanganda ===
def handle_book(update: Update, context: CallbackContext):
    selected_book = update.message.text
    book_path = os.path.join(DATA_FOLDER, selected_book)

    if not os.path.isdir(book_path):
        update.message.reply_text("❌ Noto‘g‘ri tanlov. Iltimos, menyudan tanlang.")
        return

    units = sorted(os.listdir(book_path))
    keyboard = [[unit.replace(".json", "")] for unit in units]
    context.user_data["selected_book"] = selected_book
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(f"📖 {selected_book} ichidagi unitni tanlang:", reply_markup=reply_markup)
    def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_book))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
