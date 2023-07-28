import os
import json
import requests_weather as rw
from dotenv import load_dotenv
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor, BaseStateGroup, OpenLink

load_dotenv()

VK_TOKEN = os.getenv('TOKEN')
DATA_FILE = 'cities.json'

bot = Bot(VK_TOKEN)


class RegData(BaseStateGroup):
    """Класс с состояниями, при необходимости можно продолжить."""

    FIND = 1


@bot.on.private_message(text=['/start', 'mm', 'мм'])
@bot.on.private_message(payload={'cmd': 'menu'})
async def menu(message: Message):
    """Меню бота с командами."""

    await message.answer(

        message='___Меню___',
        keyboard=(
            Keyboard(one_time=False, inline=False)
            .add(Text('Погода'), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text('Функция 1'), color=KeyboardButtonColor.NEGATIVE)
            .add(Text('Об авторе'), color=KeyboardButtonColor.SECONDARY)
        )
    )
    await bot.state_dispenser.delete(message.peer_id)


@bot.on.private_message(text=['Погода'])
async def weather_city(message: Message):
    """Функция ввода города."""

    await message.answer(
        message='Введите наименование города: ',
        keyboard=(
            Keyboard(one_time=False, inline=False)
            .add(Text('Назад', payload={'cmd': 'menu'}))
        )
    )
    await bot.state_dispenser.set(message.peer_id, RegData.FIND)


@bot.on.private_message(state=RegData.FIND)
async def weather_find(message: Message):
    """Функция создания ответа, прогноза погоды в городе."""

    user = await bot.api.users.get(message.from_id)
    city_user = message.text

    if check_city_in_json(city_user):
        wether_responce = rw.what_weather(city_user)
        await message.answer(
            message=f'{user[0].first_name}, погода в {city_user}:\n {wether_responce}',
            keyboard=(
                Keyboard(one_time=False, inline=False)
                .add(Text('Меню', payload={'cmd': 'menu'}))
            )
        )
    else:
        return '<error> – ты не ввел город'


def check_city_in_json(city_name):
    """Функция проверки сообщения пользователя на наименования города."""

    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)

    cities = data.get('city', [])
    for city in cities:
        if city.get('name', '').lower() == city_name.lower():
            return True
    return False


@bot.on.private_message(text=['Об авторе'])
async def author(message: Message):
    """Функция об авторе"""

    await message.answer(
        message='Можешь пока что посетить страницу автора: ',
        keyboard=(
            Keyboard(inline=True)
            .add(OpenLink('https://vk.com/serezhamashoha', 'Автор Бота'))
        )
    )


@bot.on.private_message(text=['Функция 1'])
async def author(message: Message):
    """Функция-заглушка"""

    await message.answer(
        message='Тут пока что ничего нет...',
    )


@bot.on.private_message()
async def author(message: Message):
    """Функция-заглушка на остальные сообщения от пользователя"""
    await message.answer(
        message='Я тебя не понимаю, воспользуйся моей клавиатурой с кнопками :)',
    )


bot.run_forever()

