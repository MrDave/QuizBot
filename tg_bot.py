from telegram import Update, ForceReply
from telegram.ext import Updater, CallbackContext, MessageHandler, CommandHandler, Filters
from environs import Env


def echo(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text(text)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hola {user.mention_markdown_v2()}\! I'm your bot for today ❤️",
        reply_markup=ForceReply(selective=True)
    )


def main():
    env = Env()
    env.read_env()

    bot_token = env.str("TELEGRAM_BOT_TOKEN")

    updater = Updater(token=bot_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
