from telegram import Update, ForceReply, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, MessageHandler, CommandHandler, Filters
from environs import Env
from random import choice
from quiz_handlers import dictify_questions


def echo(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text(text)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [
        ["Новый вопрос", "Сдаться"],
        ["Мой счёт"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_markdown_v2(
        fr"Hola {user.mention_markdown_v2()}\! I'm your bot for today ❤️",
        reply_markup=reply_markup
    )


def send_question(update: Update, context: CallbackContext):
    questionnaire = context.bot_data["questionnaire"]
    question, answer = choice(questionnaire)
    update.message.reply_text(question)


def main():
    env = Env()
    env.read_env()

    bot_token = env.str("TELEGRAM_BOT_TOKEN")

    updater = Updater(token=bot_token)
    dp = updater.dispatcher
    with open("quiz_questions/pliga51.txt", encoding="KOI8-R") as file:
        text = file.read()
    dp.bot_data["questionnaire"] = dictify_questions(text)
    dp.update_persistence()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex(r"^Новый вопрос$"), send_question))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
