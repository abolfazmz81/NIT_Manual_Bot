from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler
from langchain_openai import ChatOpenAI
import config

llm = ChatOpenAI(model="gpt-3.5-turbo", base_url="https://api.avalai.ir/v1",
                 api_key=config.api_token)

gptc = True


async def start(update: Update, context: CallbackContext) -> None:
    # determining who the user is
    wade = update.message.from_user.full_name
    check = update.message.from_user.username
    print(wade)
    # wlcoming the user
    await update.message.reply_text(f'hi {wade}!, welcome to the show')

async def gpt(update: Update, context: CallbackContext) -> None:
    global gptc
    gptc = True
    await update.message.reply_text("Please send the message you want to ask ChatGPT.")


async def mem(update: Update, context: CallbackContext) -> None:
    global gptc
    print(update.message.text)
    if gptc:
        query = update.message.text
        response = llm.invoke(query)
        await update.message.reply_text(response.content.__str__())
        gptc = False
    else:
        mes = input(f"answer the message from {update.message.from_user.username}:")
        if mes != "":
            await update.message.reply_text(mes, reply_to_message_id=update.message.message_id)
    print("done")


def main():
    Token = config.telegram_token

    application = Application.builder().token(Token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gpt", gpt))
    application.add_handler(MessageHandler(None, mem))
    application.run_polling()


if __name__ == '__main__':
    print("started")
    main()
