from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
from langchain_openai import ChatOpenAI
import Elasticsearch
import config
import extractor
import jdatetime

llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", base_url="https://api.avalai.ir/v1",
                 api_key=config.api_token)

gptc =  False
text = ""
year = 0


async def start(update: Update, context: CallbackContext) -> None:
    global year
    year = 0
    # determining who the user is
    name = update.message.from_user.full_name
    print(name)
    # keyboard layout
    keyboard = [
        ["/help"]
    ]
    # making the markup
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # welcoming the user
    await update.message.reply_text(f'سلام کاربر {name} خوش آمدید')

    await update.message.reply_text("لطفا سال ورودی خود را بصورت کامل وارد کنید", reply_markup=reply_markup)


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
    global year
    if year == 0:
        return
    gptc = True
    keyboard = [
        ["/cancel"]
    ]
    reply = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("لطفا سوال خود را بپرسید", reply_markup=reply)


async def cancel(update: Update, context: CallbackContext) -> None:
    global gptc
    if gptc:
        gptc = False
        keyboard = [
            ["/gpt", "/help"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("چت بات غیرفعال شد", reply_markup=reply_markup)
    else:
        keyboard = [
            ["/gpt", "/help"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("The ChatGPT is not active",reply_markup=reply_markup)


async def mem(update: Update, context: CallbackContext) -> None:
    global gptc
    global text
    global year
    #print(update.message.text)

    # Determine the year of enter
    if year == 0:
        try:
            num = int(update.message.text)
        except:
            await update.message.reply_text("سال ورودی فقط شامل عدد است", reply_to_message_id=update.message.message_id)
            return
        keyboard = [
            ["/gpt", "/help"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        if num < 1397:
            await update.message.reply_text(f"سال ورودی انتخاب شده مورد تایید برای دانشجوی کارشناسی نمیباشد.",
                                            reply_to_message_id=update.message.message_id, reply_markup=reply_markup)
            return
        elif 1397 <= num < 1402:
            year = 97
        elif num >= 1402:
            year = 402
        await update.message.reply_text(f"سال ورودی شما {num} انتخاب شد، برای انتخاب دوباره start را فشار بدهید",
                                        reply_to_message_id=update.message.message_id, reply_markup=reply_markup)
        text = extractor.return_doc(f"docs/{year}/ayin.pdf")
        return

    if gptc:
        question = update.message.text
        today_shamsi = jdatetime.date.today()
        qe = f"من ورودی {year} هستم، سوال من اینست که:\n" + update.message.text
        # Replace time adverbs with shamsi date
        question = question.replace("امروز", today_shamsi.strftime("%Y/%m/%d"))
        question = question.replace("دیروز", (today_shamsi - jdatetime.timedelta(days=1)).strftime("%Y/%m/%d"))
        question = question.replace("فردا", (today_shamsi + jdatetime.timedelta(days=1)).strftime("%Y/%m/%d"))

        possible_answer = Elasticsearch.search_question(qe)
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
                    text = <{text}>
                    question = ```{question}```       
                    """
            keyboard = [
                ["/gpt", "/help"]
            ]
            # making the markup
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            response = llm.invoke(query)
            await update.message.reply_text(response.content.__str__(), reply_markup=reply_markup)
            Elasticsearch.index_data(qe, response.content.__str__())
            gptc = False
    else:
        mes = "ربات را با زدن دکمه /gpt فعال کنید."
        if mes != "":
            keyboard = [
                ["/gpt", "/help"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(mes, reply_to_message_id=update.message.message_id,reply_markup=reply_markup)
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
