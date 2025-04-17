import os
import openai
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import gspread
import json

# ==== Load Secrets from Environment ====
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_SHEET_NAME = "My Arman"
GOOGLE_CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON")  # GitHub Secret (json string)

# ==== Prepare Google Credentials ====
with open("google_credentials.json", "w") as f:
    f.write(GOOGLE_CREDENTIALS_JSON)

# ==== Setup APIs ====
openai.api_key = OPENAI_API_KEY

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = gspread.service_account(filename="google_credentials.json")
sheet = creds.open(GOOGLE_SHEET_NAME).sheet1

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
    update.message.reply_text("لطفاً اطلاعات ثبت‌نام خود را به این صورت وارد کنید:\nنام، ایمیل، کشور مورد نظر")

def save_info(update, context):
    info = update.message.text.split(",")
    if len(info) == 3:
        sheet.append_row([i.strip() for i in info])
        update.message.reply_text("اطلاعات شما ذخیره شد. با شما تماس خواهیم گرفت.")
    else:
        update.message.reply_text("فرمت اشتباه است. لطفاً به صورت «نام، ایمیل، کشور» وارد کنید.")

# ==== Main ====
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register_command))
    dp.add_handler(MessageHandler(Filters.regex(".*@.*"), save_info))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ask_ai))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
