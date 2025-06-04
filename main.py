import logging
import json
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# 🔧 Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 📍 Holatlar
CHOOSE_BOOK, CHOOSE_UNIT, SHOW_WORDS, START_QUIZ, QUIZ, REVIEW_MISTAKES, REINFORCE = range(7)

# 📘 Global o'zgaruvchilar
USER_DATA = {}
BOOKS = ["Book 1", "Book 2", "Book 3", "Book 4"]

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    USER_DATA[user_id] = {}

    reply_keyboard = [[book] for book in BOOKS]
    update.message.reply_text(
        "🇬🇧 *English Vocabulary Bot* ga xush kelibsiz!\n\n"
        "Iltimos, boshlash uchun kitobni tanlang:",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )
    return CHOOSE_BOOK

def choose_book(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    book = update.message.text
    if book not in BOOKS:
        update.message.reply_text("Iltimos, ro‘yxatdan kitob tanlang.")
        return CHOOSE_BOOK

    USER_DATA[user_id]['book'] = book
    unit_list = [f"Unit {i}" for i in range(1, 31)]  # 30 ta unit
    reply_keyboard = [[unit] for unit in unit_list]

    update.message.reply_text(
        f"{book} tanlandi.\n\nEndi esa unitni tanlang:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )
    return CHOOSE_UNIT
