from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from DARKTUNNEL import run as dark_run
from HTTPINJECTOR import run as injector_run
from HTTPCUSTOM import run as custom_run
from NPVTUNNEL import run as npv_run
from SSCCUSTOM import run as ssc_run

BOT_TOKEN = "7741526627:AAHrYdSZ2tFdWpqLm2YVvG03UENtjXIL2No"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔓 HABIBI DECRYPTION BOT\n\n"
        "Welcome!\n"
        "Send me any supported config file and I'll decrypt it."
    )


async def decrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        return

    file = await update.message.document.get_file()
    file_bytes = await file.download_as_bytearray()

    decryptors = [
        dark_run,
        injector_run,
        custom_run,
        npv_run,
        ssc_run,
    ]

    for decryptor in decryptors:
        try:
            result = decryptor(bytes(file_bytes))

            if result:
                if len(result) > 4000:
                    with open("result.txt", "w", encoding="utf-8") as f:
                        f.write(result)

                    await update.message.reply_document(
                        document=open("result.txt", "rb")
                    )
                else:
                    await update.message.reply_text(result)

                return

        except Exception:
            pass

    await update.message.reply_text(
        "❌ Unsupported or invalid configuration file."
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, decrypt))

    print("✅ Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
