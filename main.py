from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from langchain_openai import ChatOpenAI
import Elasticsearch
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
    await update.message.reply_text(f'سلام کاربر {name} خوش آمدید')

    await update.message.reply_text("لطفا بخشی که از آن سوال دارید را انتخاب کنید", reply_markup=reply_markup)


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

    await update.message.reply_text("""/gpt: بعد انتخاب این گزینه، جایی که بنظرتان سوال از آن است را انتخاب کرده سپس سوالتان را بپرسید.\n
    /cancel: از آن استفاده کنید تا به حالت اول برگردید بدون سوال پرسیدن""", reply_markup=reply_markup)


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
        possible_answer = Elasticsearch.search_question(question)
        if possible_answer is not None:
            keyboard = [
                ["/gpt", "/help"]
            ]
            print("found possible answer")
            # making the markup
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(possible_answer, reply_markup=reply_markup)

        else:
            query = f"""
                    Answer the question specified in triple backticks based on the text Provided in <>, search the text to insure the answer could be there \
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
            Elasticsearch.index_data(question,response.content.__str__())
            gptc = False
    else:
        mes = "ChatGPT is not active!"
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
