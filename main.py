from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from langchain_openai import ChatOpenAI
import config
import extractor

llm = ChatOpenAI(model="gpt-4o-mini", base_url="https://api.avalai.ir/v1",
                 api_key=config.api_token)

gptc = True
ayin97 = extractor.return_97("1633766767-ayinnamehkarshenasi97-v3.pdf")


async def start(update: Update, context: CallbackContext) -> None:
    # determining who the user is
    name = update.message.from_user.full_name
    print(name)
    # keyboard layout
    keyboard = [
        ["/gpt", "/help"]
    ]
    # making the markup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # wlcoming the user
    await update.message.reply_text(f'hi {name}!, welcome to the show')

    await update.message.reply_text("Please select a command!", reply_markup=reply_markup)


async def help(update: Update, context: CallbackContext) -> None:
    # determining who the user is
    wade = update.message.from_user.full_name
    check = update.message.from_user.username
    print(wade)
    # keyboard layout
    keyboard = [
        ["/gpt", "/help"]
    ]
    # making the markup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("""/gpt: Use it to ask a question from ChatGPT, Then Proceed to ask your question.\n
    /cancel: Use it To Cancel your /gpt command""", reply_markup=reply_markup)


async def gpt(update: Update, context: CallbackContext) -> None:
    global gptc
    gptc = True
    keyboard = [
        ["/cancel"]
    ]
    reply = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Please send the message you want to ask ChatGPT.", reply_markup=reply)


async def cancel(update: Update, context: CallbackContext) -> None:
    global gptc
    if gptc:
        gptc = False
        keyboard = [
            ["/gpt", "/help"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("The ChatGPT is inactivated",reply_markup=reply_markup)
    else:
        await update.message.reply_text("The ChatGPT is not active")


async def mem(update: Update, context: CallbackContext) -> None:
    global gptc
    global ayin97
    print(update.message.text)
    if gptc:
        question = update.message.text
        query = f"""
        Answer the question specified in triple backticks based on the text Provided in <>, and be specific about it, \
        if you couldn't find any related information in the text, reply with irrelevant question, \
        both text and question are in persian(farsi), and you should as well answer in persian.\n
        text = <{ayin97}>
        question = ```{question}```       
        """
        keyboard = [
            ["/gpt", "/help"]
        ]
        # making the markup
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        response = llm.invoke(query)
        await update.message.reply_text(response.content.__str__(), reply_markup=reply_markup)
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
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("gpt", gpt))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(None, mem))
    application.run_polling()


if __name__ == '__main__':
    print("started")
    main()
