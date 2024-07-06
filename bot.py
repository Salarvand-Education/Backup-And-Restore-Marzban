import os
import zipfile
import shutil
import time
import schedule
import asyncio
import nest_asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# مسیرهای پوشه‌های marzban
MARZBAN_SRC1 = '/opt/marzban/'
MARZBAN_SRC2 = '/var/lib/marzban/'
BACKUP_DIR = '/tmp'

updater = None  # تعریف متغیر application در سطح بالا
backup_interval = 1  # فاصله زمانی اولیه بکاپ‌گیری به دقیقه

logging.basicConfig(level=logging.INFO)

def backup_marzban():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_name = f"backup_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(MARZBAN_SRC1):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, MARZBAN_SRC1))

        for root, dirs, files in os.walk(MARZBAN_SRC2):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, MARZBAN_SRC2))

    logging.info(f"Backup created: {backup_path}")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! من اینجا هستم تا به شما کمک کنم.")

def backup_command(update: Update, context: CallbackContext):
    backup_marzban()
    update.message.reply_text("بکاپ‌گیری انجام شد!")

def restore_command(update: Update, context: CallbackContext):
    # فرمان ریستور
    update.message.reply_text("ریستور در دسترس نیست.")

def set_interval(update: Update, context: CallbackContext):
    global backup_interval
    try:
        new_interval = int(context.args[0])
        backup_interval = new_interval
        schedule_jobs()
        update.message.reply_text(f"فاصله زمانی بکاپ‌گیری به {new_interval} دقیقه تغییر یافت.")
    except (IndexError, ValueError):
        update.message.reply_text("لطفا یک عدد صحیح وارد کنید.")

def handle_document(update: Update, context: CallbackContext):
    # فرمان هندل فایل‌های آپلود شده
    update.message.reply_text("فایل دریافت شد.")

def schedule_jobs():
    schedule.clear()
    schedule.every(backup_interval).minutes.do(backup_marzban)
    logging.info(f"Scheduled backup every {backup_interval} minutes.")

async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    global updater
    # استفاده از توکن جدید تلگرام
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('backup', backup_command))
    dispatcher.add_handler(CommandHandler('restore', restore_command))
    dispatcher.add_handler(CommandHandler('setinterval', set_interval))  # فرمان جدید برای تنظیم فاصله زمانی
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

    schedule_jobs()
    
    # اجرای run_schedule به عنوان یک تسک asyncio
    asyncio.create_task(run_schedule())
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
