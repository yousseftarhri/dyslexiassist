import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PORT = int(os.environ.get('PORT', 5000))
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

#voice_808870631.mp3


def response(messages) :
    prompt = ("""You are Dyslexia Assist, an intelligent and empathetic assistant designed to help individuals with dyslexia improve their reading and speaking skills. Your task is to take a user's spoken input, and then correct any grammatical or syntactical errors while preserving the original meaning and intent of the user's speech. Provide clear and concise corrections that are easy for the user to understand and learn from. \""
          Example:

User Input (spoken): "I goed to the store and buyed some apple."

Correction: "I went to the store and bought some apples."

Explanation: The words "goed" and "buyed" are incorrect past tense forms. The correct forms are "went" and "bought," and "some apple" should be "some apples" to indicate plural.


              """)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": messages}
    ]
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=0.8,
        messages=messages)

    return completion.choices[0].message.content

def STT(bot,name_audio,file_id,chat_id) :
    file = bot.getFile(file_id)

    file.download(name_audio)

    file_path = f'voice_{chat_id}.mp3'
    audio_file = open(file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

def start(update, context):
    """Send a message when the command /start is issued."""
    bot = context.bot

    bot.send_message(chat_id=update.message.chat_id, text="welcome",parse_mode= 'Markdown')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def voice_handler(update, context):
    bot = context.bot
    chat_id = update.message.chat_id
    try:
        try:
            file_id = update.message.voice.file_id
        except:
            file_id = update.message.audio.file_id
        file_path = f'voice_{chat_id}.mp3'
        msg = STT(bot,file_path,file_id,chat_id)
        output_ai = response(msg)
        print(output_ai)
        bot.send_message(chat_id=update.message.chat_id, text=f"{msg}", parse_mode='Markdown')

        bot.send_message(chat_id=update.message.chat_id, text=output_ai, parse_mode='Markdown')

    except Exception as e:
        bot = context.bot
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text='We have a problem in our bot we gonna fix it ASAP')
        print(f"An unexpected error occurred: {e}")
    print("ok")

def text_handler(update, context):
    bot = context.bot
    chat_id = update.message.chat_id
    try:

        msg = update.message.text


        output_ai = response(msg)
        print(output_ai)
        bot.send_message(chat_id=update.message.chat_id, text=output_ai)


    except Exception as e:
        bot = context.bot
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text='We have a problem in our bot we gonna fix it ASAP')
        print(f"An unexpected error occurred: {e}")
    print("ok")
def main():
    """Start the bot."""

    updater = Updater(bot_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    dp.add_handler(MessageHandler(Filters.audio, voice_handler))
    dp.add_handler(MessageHandler(Filters.text, text_handler))

    # log all errors
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
