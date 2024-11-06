import telebot

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота, полученный от BotFather
TOKEN = '7515810323:AAGE8_pnpunOmSwKgarXSEf42xGrAjK4Q40'

bot = telebot.TeleBot(TOKEN)

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я бот с автозапуском")

if __name__ == "__main__":
    bot.infinity_polling()
