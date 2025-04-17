import openai
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==== Configurations ====
TELEGRAM_TOKEN = "7101873768:AAHCsefEGuf4KFbesjo7TBd_TrIqIuwg2uo"
OPENAI_API_KEY = "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"
GOOGLE_SHEET_NAME = "My Arman"
CREDENTIALS_JSON = "secret-sphinx-457017-j2-9f23d084711f.json"  # فایل json احراز هویت Google Sheets

openai.api_key = OPENAI_API_KEY

# ==== Google Sheets Setup ====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_JSON, scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# ==== Telegram Handlers ====

def start(update, context):
    update.message.reply_text("سلام! من دستیار مهاجرت هستم. سوالی درباره مهاجرت داری؟")

def ask_ai(update, context):
    user_question = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_question}]
    )
    answer = response.choices[0].message.content
    update.message.reply_text(answer)

def register_command(update, context):
    user = update.message.from_user
    update.message.reply_text("لطفاً اطلاعات ثبت‌نام خود را به این صورت وارد کنید:\nنام، ایمیل، کشور مورد نظر")
    return

def save_info(update, context):
    info = update.message.text.split(",")
    if len(info) == 3:
        sheet.append_row(info)
        update.message.reply_text("اطلاعات شما ذخیره شد. با شما تماس خواهیم گرفت.")
    else:
        update.message.reply_text("فرمت اشتباه است. لطفاً به صورت «نام، ایمیل، کشور» وارد کنید.")

# ==== Main ====

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register_command))
    dp.add_handler(MessageHandler(Filters.regex(".*@.*"), save_info))  # تشخیص ثبت‌نام
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ask_ai))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

