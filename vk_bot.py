import random
import logging

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import redis
from telegram import Bot

from quiz_handlers import assemble_questionnaire
from telegram_logging import TelegramLogsHandler


logger = logging.getLogger()


def start(event, vk_api):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button("Новый вопрос")
    keyboard.add_button("Сдаться")

    keyboard.add_line()
    keyboard.add_button("Мой счёт")

    vk_api.messages.send(
        user_id=event.user_id,
        message="Привет! Я – твой викторинный бот на сегодня ❤️",
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard(),
    )


def send_new_question(event, vk_api, redis_db, questionnaire):
    question, answer = random.choice(questionnaire)
    redis_db.hset(event.user_id, mapping={
        "answer": answer,
        "question": question
    })
    vk_api.messages.send(
        user_id=event.user_id,
        message=question,
        random_id=random.randint(1, 1000),
    )


def check_answer(event, vk_api, redis_db):
    correct_answer = redis_db.hgetall(event.user_id)["answer"]
    user_answer = event.text
    if user_answer.lower() == correct_answer.lower():
        response = "Хорош! Жми на \"Новый вопрос\"!"
    else:
        response = "Неправильно… Попробуешь ещё раз?"

    vk_api.messages.send(
        user_id=event.user_id,
        message=response,
        random_id=random.randint(1, 1000),
    )


def give_correct_answer(event, vk_api, redis_db):
    correct_answer = redis_db.hgetall(event.user_id)["answer"]
    vk_api.messages.send(
        user_id=event.user_id,
        message=correct_answer,
        random_id=random.randint(1, 1000)
    )


def main():
    env = Env()
    env.read_env()

    vk_token = env.str("VK_GROUP_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    logger_bot = Bot(token=env.str("TELEGRAM_LOGGING_BOT_TOKEN"))
    chat_id = env.str("TELEGRAM_USER_ID")

    logger.setLevel(env.str("LOGGING_LEVEL", logging.WARNING))
    logger.addHandler(TelegramLogsHandler(logger_bot, "VK Quiz Bot", chat_id))

    logger.info("VK bot started")

    redis_host = env.str("REDIS_HOST")
    redis_port = env.str("REDIS_PORT")
    redis_password = env.str("REDIS_PASSWORD")

    redis_db = redis.Redis(
        host=redis_host,
        port=redis_port,
        protocol=3,
        password=redis_password,
        decode_responses=True)

    with open(env.str("QUIZ_FILE_PATH", "quiz_questions/example.txt"), encoding="KOI8-R") as f:
        text = f.read()
    questionnaire = assemble_questionnaire(text)

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == "Начать":
                start(event, vk_api)
            elif event.text == "Новый вопрос":
                send_new_question(event, vk_api, redis_db, questionnaire)
            elif event.text == "Сдаться":
                give_correct_answer(event, vk_api, redis_db)
                send_new_question(event, vk_api, redis_db, questionnaire)
            elif event.text == "Мой счёт":
                # TODO: implement counting user's score
                pass
            else:
                check_answer(event, vk_api, redis_db)


if __name__ == "__main__":
    main()
