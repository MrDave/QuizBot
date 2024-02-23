from telegram import Update, ForceReply, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext, MessageHandler, CommandHandler, Filters, ConversationHandler
from environs import Env
from random import choice
from quiz_handlers import dictify_questions
import redis

ANSWERING = 0


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
    context.chat_data["current_quiz"] = question, answer

    return ANSWERING


def check_answer(update: Update, context: CallbackContext):
    question, answer = context.chat_data["current_quiz"]
    user_answer = update.message.text
    if user_answer in answer.split(".", maxsplit=1):
        text = "Хорош! Жми на \"Новый вопрос\"!"
        update.message.reply_text(text)
        return ConversationHandler.END
    else:
        text = "Неправильно… Попробуешь ещё раз?"
        update.message.reply_text(text)


def main():
    env = Env()
    env.read_env()

    bot_token = env.str("TELEGRAM_BOT_TOKEN")
    redis_host = env.str("REDIS_HOST", "localhost")
    redis_port = env.str("REDIS_PORT", 6379)
    redis_password = env.str("REDIS_PASSWORD")

    updater = Updater(token=bot_token)
    dp = updater.dispatcher
    with open("quiz_questions/ars12.txt", encoding="KOI8-R") as file:
        text = file.read()
    dp.bot_data["questionnaire"] = dictify_questions(text)
    dp.bot_data["redis"] = redis.Redis(
        host=redis_host,
        port=redis_port,
        protocol=3,
        password=redis_password,
        decode_responses=True)
    dp.update_persistence()
    question_conversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^Новый вопрос$"), send_question)],
        states={
            ANSWERING: [MessageHandler(Filters.text & ~Filters.command, check_answer)]
        },
        fallbacks=[CommandHandler("cancel", start)]
    )
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(question_conversation)
    # dp.add_handler(MessageHandler(Filters.regex(r"^Новый вопрос$"), send_question))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
