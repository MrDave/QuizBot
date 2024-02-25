# QuizBot
Quiz bot for Telegram and Vkontakte

See for yourself:
- [Telegram bot](https://t.me/MrDaveQuizBot)
- [VK bot](https://vk.com/im?sel=-224351051)

## How to install

Python should already be installed. This project is tested on Python 3.11. You may use other versions as you will, but YMMV.

Clone the repo / download code

Using virtual environment [virtualenv/venv](https://docs.python.org/3/library/venv.html) is recommended for project isolation.

Install requirements:
```commandline
pip install -r requirements.txt
```

### redis DB
This project uses redis database. Create and connect your instance at [redis website](https://app.redislabs.com/) 

### env variables

To configure those settings, create a `.env` file in the root folder of the project and put in there the following:

#### Typical Telegram settings

- `TELEGRAM_BOT_TOKEN` - Access token of your bot. You get one from [BotFather Telegram bot](https://t.me/BotFather) when you create a bot.
- `TELEGRAM_LOGGING_BOT_TOKEN` - same as above, but used for sending logs. Can be the same bot or separate as the main one.
- `TELEGRAM_USER_ID` - Your numeric Telegram ID. Can be checked by writing to special [user info bot](https://t.me/userinfobot). Used to recieve logs.
- `LOGGING_LEVEL` - Desired [logging level](https://docs.python.org/3/library/logging.html#logging-levels)
- `REDIS_HOST` - Host of your redis database
- `REDIS_PORT` - Port of your redis database
- `REDIS_PASSWORD` - Password for your redis database
- `REDIS_DB_NUMBER` - The ID of your redis database

## How to use

Telegram and VK bots are separate and should be launched by executing `telegram_bot.py` and `vk_bot.py`

```commandline
python telegram_bot.py  # launches Telegram bot
python vk_bot.py  # launches VK bot
```

For Telegram bot to be able to send messages, send it a `/start` command

Telegram bot example:  
![Telegram example](https://dvmn.org/filer/canonical/1569215494/324/)

Vkontakte bot example:  
![VK example](https://dvmn.org/filer/canonical/1569215498/325/)

## Project goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).