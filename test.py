from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler
import config


async def start(update: Update, context: CallbackContext) -> None:
    # determining who the user is
    wade = update.message.from_user.full_name
    check = update.message.from_user.username
    print(wade)
    # wlcoming the user
    await update.message.reply_text(f'hi {wade}!, welcome to the show')

async def mem(update: Update, context: CallbackContext) -> None:
    print(update.message.text)
        mes = input(f"answer the message from {update.message.from_user.username}:")
        if mes != "":
            await update.message.reply_text(mes, reply_to_message_id=update.message.message_id)
    print("done")


def main():
    Token = config.telegram_token

    application = Application.builder().token(Token).build()

    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    print("started")
    main()
