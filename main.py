import requests
from requests import get
import json
from datetime import datetime
import iso8601
import pytz
import telebot
from auth_data import token


def app(update, context):
    text = update.message.text
    context.user_data["choice"] = text

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    
    req = requests.get("https://haqq-t.api.manticore.team/cosmos/gov/v1beta1/proposals")
    data = json.loads(req.text)   


    
    bot.message_handler(commands=["start"])
    def start_message(message):
            
                try:
                    for item in data:
                        if item['proposal_status'] == 'PROPOSAL_STATUS_VOTING_PERIOD' and iso8601.parse_date(item['submit_time'][:-1]) > datetime.now(tz=pytz.UTC):
                            number = item['id']
                            title = item['title']
                            description = item['description']
                            bot.send_message(
                                message.chat.id,
                                    f"{description}\nProposal {number} is in voting stage!\n{title}"
                                )

                except Exception as e:  
                    print(e)
                    bot.send_message(
                        message.chat.id,
                            "Damn...Something was wrong..."
                            )
          

    bot.polling()


if __name__ == '__main__':
  
    telegram_bot(token)
