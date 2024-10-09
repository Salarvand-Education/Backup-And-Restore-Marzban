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
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# مسیرهای پوشه‌های marzban
MARZBAN_SRC1 = '/opt/marzban/'
MARZBAN_SRC2 = '/var/lib/marzban/'
BACKUP_DIR = '/tmp'

application = None  # تعریف متغیر application در سطح بالا
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
                arcname = os.path.relpath(file_path, start='/')
                zipf.write(file_path, arcname=arcname)
        for root, dirs, files in os.walk(MARZBAN_SRC2):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start='/')
                zipf.write(file_path, arcname=arcname)
    
    return backup_path

async def restore_marzban(backup_path):
    logging.info(f"Starting restore from {backup_path}")
    if not os.path.exists(backup_path):
        logging.error("Backup file does not exist.")
        return False

    try:
        if os.path.exists(MARZBAN_SRC1):
            shutil.rmtree(MARZBAN_SRC1)
        if os.path.exists(MARZBAN_SRC2):
            shutil.rmtree(MARZBAN_SRC2)
        
        os.makedirs(MARZBAN_SRC1)
        os.makedirs(MARZBAN_SRC2)

        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall('/')

        logging.info("Files extracted successfully. Restarting Marzban...")
        process = await asyncio.create_subprocess_shell(
            'marzban restart',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            line = await process.stdout.readline()
            if line:
                logging.info(line.decode().strip())
                if 'Uvicorn running on' in line.decode():
                    return True
            else:
                break

        await process.wait()
        return process.returncode == 0
    except Exception as e:
        logging.error(f"Error during restore: {str(e)}")
        return False

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('سلام! از دستور /backup برای گرفتن بکاپ و از /restore برای ریستور استفاده کنید.')

async def backup_command(update: Update, context: CallbackContext) -> None:
    backup_path = backup_marzban()
    with open(backup_path, 'rb') as f:
        await update.message.reply_document(document=InputFile(f, filename=os.path.basename(backup_path)))
    os.remove(backup_path)

async def restore_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('لطفا فایل بکاپ را ارسال کنید.')

async def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    file = await context.bot.get_file(document.file_id)
    backup_path = os.path.join('/tmp', document.file_name)
    await file.download_to_drive(backup_path)
    
    if await restore_marzban(backup_path):
        await update.message.reply_text('بکاپ با موفقیت ریستور شد و Marzban ری‌استارت شد!')
    else:
        await update.message.reply_text('خطا در ریستور بکاپ یا ری‌استارت Marzban.')
    os.remove(backup_path)

async def send_backup():
    logging.info("Sending backup...")
    backup_path = backup_marzban()
    with open(backup_path, 'rb') as f:
        await application.bot.send_document(chat_id=ADMIN_CHAT_ID, document=InputFile(f, filename=os.path.basename(backup_path)))
    os.remove(backup_path)
    logging.info("Backup sent.")

def schedule_jobs():
    schedule.clear()  # حذف همه زمان‌بندی‌های قبلی
    schedule.every(backup_interval).minutes.do(lambda: asyncio.create_task(send_backup()))
    logging.info(f"Scheduled backup every {backup_interval} minutes.")

async def set_interval(update: Update, context: CallbackContext) -> None:
    global backup_interval
    try:
        new_interval = int(context.args[0])
        backup_interval = new_interval
        schedule_jobs()  # به‌روزرسانی زمان‌بندی‌ها
        await update.message.reply_text(f'فاصله زمانی بکاپ‌گیری به {backup_interval} دقیقه تغییر یافت.')
        logging.info(f"Backup interval set to {backup_interval} minutes.")
    except (IndexError, ValueError):
        await update.message.reply_text('لطفاً یک عدد معتبر وارد کنید.')

async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main() -> None:
    global application
    # استفاده از توکن جدید تلگرام
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("backup", backup_command))
    application.add_handler(CommandHandler("restore", restore_command))
    application.add_handler(CommandHandler("setinterval", set_interval))  # فرمان جدید برای تنظیم فاصله زمانی
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    schedule_jobs()
    
    # اجرای run_schedule به عنوان یک تسک asyncio
    asyncio.create_task(run_schedule())
    await application.run_polling()

if __name__ == '__main__':
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
