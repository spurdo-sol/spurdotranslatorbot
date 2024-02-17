from telegram import Update
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, filters

import re
import logging

# Your Bot Token
TOKEN = "6517383606:AAGCJNfkXeR1av9r0JcVo_KpqlHVuxw6FvM"


def to_spurdo(text):
    # Case-insensitive replacement using regex
    def regex_replace(pattern, repl, string):
        return re.sub(pattern, repl, string, flags=re.IGNORECASE)

    # Initial replacements for common phrases and patterns
    replacements = {
        r"\bthat\b": "dat",
        r"\bthe\b": "teh",
        r"\bthis\b": "dis",
        r"\bmy\b": "muh",
        r"\byour\b": "ur",
        r"\bepic\b": "ebin",
        r"\bthanks\b": "tank :DD",
        r"\bplease\b": "blease",
        r"\bhello\b": "helo",
        r"\bfriend\b": "freind :DD",
        r"\bhappening\b": "habbening :DD",
        r"\bvagina\b": "bagina",
    }

    for pattern, repl in replacements.items():
        text = regex_replace(pattern, repl, text)

    # Character-based transformations
    char_replacements = {
        "wh": "w",
        "th": "d",
        "af": "ab",
        "ap": "ab",
        "ca": "ga",
        "ck": "gg",
        "co": "go",
        "pe": "be",
        "po": "bo",
        "ve": "b",
        "ex": "egs",
        "et": "ed",
    }

    for pattern, repl in char_replacements.items():
        text = regex_replace(pattern, repl, text)

    # Add ':DD' smartly after specific punctuation marks
    text = re.sub(r"([.!?])", r" :DD\1", text)

    # Add ':DD' at the end if the sentence is not ended with '.'
    if not text.endswith("."):
        text += " :DD"

    return text


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Send /spurdo <message> to Spurdo-fy your message :DD",
    )


def translate(update, context):
    if not context.args:
        update.message.reply_text("Usage: /translate <input>")
        return

    input_text = " ".join(context.args)
    spurdo_text = to_spurdo(input_text)
    user_info = (
        f"{update.effective_user.first_name} (@{update.effective_user.username})"
    )
    reply_text = f"{user_info}\n\n{spurdo_text}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.message.message_id
    )


def handle_text(update, context):
    input_text = update.message.text

    if input_text.startswith("https://") or input_text.startswith("http://"):
        return

    spurdo_text = to_spurdo(input_text)

    user_info = (
        f"{update.effective_user.first_name} (@{update.effective_user.username})"
    )
    reply_text = f"{user_info}\n\n{spurdo_text}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)
    context.bot.delete_message(
        chat_id=update.effective_chat.id, message_id=update.message.message_id
    )


def main():
    updater = Updater(
        token=TOKEN, use_context=True
    )  # Using the token directly without keyword argument
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("spurdo", translate, pass_args=True))
    dp.add_handler(
        MessageHandler(filters.Filters.text & ~filters.Filters.command, handle_text)
    )  # Add this line

    # dp.add_handler(CommandHandler('translate', translate, pass_args=True))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
