from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import json

TOKEN = "7633206691:AAGFxRSHrsf99Png8nYtBKvBUyEZNo0xmX0"

# JSON fayldan so'zlarni yuklaymiz
with open("data/book/unit1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Har bir foydalanuvchining holati
user_states = {}

def start(update: Update, context: CallbackContext):
    keyboard = [["📘 Book 1", "📙 Book 2"], ["📗 Book 3", "📕 Book 4"]]
    update.message.reply_text("Kitobni tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

def handle_book_choice(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id

    if "Book" in text:
        book_number = text.split()[1]
        user_states[user_id] = {"book": f"book{book_number}"}
        update.message.reply_text(f"{text} tanlandi. Endi Unitni tanlang:", 
                                  reply_markup=ReplyKeyboardMarkup([["Unit 1", "Unit 2"]], resize_keyboard=True))

    elif "Unit" in text:
        unit_number = text.split()[1]
        state = user_states.get(user_id, {})
        book = state.get("book")
        if book:
            words = data[book][f"unit{unit_number}"]
            state["unit"] = f"unit{unit_number}"
            state["words"] = words
            state["quiz_index"] = 0
            user_states[user_id] = state

            # So'zlarni ko'rsatamiz
            reply = "\n".join([f"{w['word']} — {w['translation']}" for w in words])
            update.message.reply_text("Yodlaymiz:\n\n" + reply)
            update.message.reply_text("Tayyor bo‘lsangiz 'Testni boshlash' deb yozing.")
        else:
            update.message.reply_text("Avval kitobni tanlang.")

    elif text.lower() == "testni boshlash":
        state = user_states.get(user_id, {})
        words = state.get("words", [])
        index = state.get("quiz_index", 0)

        if index < len(words):
            word = words[index]
            state["expected_answer"] = word["word"].lower()
            update.message.reply_text(f"Tarjimasi: {word['translation']}")
        else:
            update.message.reply_text("Test tugadi!")
            state["quiz_index"] = 0

def handle_answer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    state = user_states.get(user_id, {})
    expected = state.get("expected_answer")
    answer = update.message.text.strip().lower()

    if expected:
        if answer == expected:
            update.message.reply_text("✅ To‘g‘ri!")
        else:
            update.message.reply_text(f"❌ Noto‘g‘ri. To‘g‘risi: {expected}")
        state["quiz_index"] += 1
        handle_book_choice(update, context)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_book_choice))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_answer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
