import os
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, LabeledPrice, ContentType
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from sqlalchemy import select, func
from app import keyboards as kb
from app.database import *
from vpn_methods.constants import *
from vpn_methods.main import add_client, add_inbound, generate_config

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await async_main()
    print("success")


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    with open('start.txt', encoding="utf-8") as f:
        start_words = f.read()
    await message.answer(start_words, reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f"Добро пожаловать {message.from_user.full_name} ", reply_markup=kb.main_admin)


@dp.message_handler(text="Купить")
async def buy_product(message: types.Message):
    await message.answer("Просмотрите варианты наших товаров!", reply_markup=kb.buy_variants)


@dp.message_handler(text="Инструкция пользования")
async def using_instruction(message: types.Message):
    await message.answer("Инструкция", reply_markup=kb.instruction_keyboard)


@dp.message_handler(text="Админ-панель")
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Вы вошли в админ панель", reply_markup=kb.main_admin_panel)
    else:
        await message.reply("Я вас не понимаю")


@dp.message_handler(text="Добавить сервер")
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        with requests.Session() as s:
            data = {
                'username': ADMIN_LOGIN,
                'password': ADMIN_PASSWORD,
            }

            login_resp = s.post(SERVER_URL + "/login", data=data)
            print(login_resp.json())
            inbound_resp = add_inbound(s, SERVER_URL)
            if inbound_resp.get('success'):
                indound = session.add(ConfigInbound(SERVER_URL, inbound_resp.get("obj")))

                await session.commit()
                await message.answer("Inbound был добавлен")
    else:
        await message.reply("Я вас не понимаю")


@dp.message_handler(text="Просмотреть пользователей")
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        result = await session.execute(select(func.count(ConfigClient.id)))
        count = result.scalar()
        await message.answer(count)

    else:
        await message.reply("Я вас не понимаю")


@dp.message_handler(text="Назад")
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Возвращаемся в главное", reply_markup=kb.main_admin)
    else:
        await message.reply("Я вас не понимаю")


@dp.callback_query_handler(text="month")
async def order_month(message: Message):
    await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка VPN',
        description="Покупка впн на месяц",
        payload="Payment through a bot",
        provider_token='381764678:TEST:75091',
        currency="rub",
        prices=[
            LabeledPrice(
                label='VPN на месяц',
                amount=30000
            ),
        ],
        start_parameter='nzstcoder',
        provider_data=None,
        photo_url='https://assetsblog.bsbportal.com/wp-content/uploads/2022/08/What-is-VPN.jpg',
        photo_height=450,
        photo_size=100,
        photo_width=800,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,

    )


@dp.callback_query_handler(text="3month")
async def order_3month(message: Message):
    await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка VPN',
        description="Покупка впн на 3 месяца",
        payload="Payment through a bot",
        provider_token='381764678:TEST:75091',
        currency="rub",
        prices=[
            LabeledPrice(
                label='VPN на 3 месяца',
                amount=60000
            ),
        ],
        start_parameter='nzstcoder',
        provider_data=None,
        photo_url='https://assetsblog.bsbportal.com/wp-content/uploads/2022/08/What-is-VPN.jpg',
        photo_height=450,
        photo_size=100,
        photo_width=800,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,

    )


@dp.callback_query_handler(text="year")
async def order_year(message: Message):
    await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка VPN',
        description="Покупка впн на год",
        payload="Payment through a bot",
        provider_token='381764678:TEST:75091',
        currency="rub",
        prices=[
            LabeledPrice(
                label='VPN на год',
                amount=100000
            ),
        ],
        start_parameter='nzstcoder',
        provider_data=None,
        photo_url='https://assetsblog.bsbportal.com/wp-content/uploads/2022/08/What-is-VPN.jpg',
        photo_height=450,
        photo_size=100,
        photo_width=800,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,

    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, )
async def succesful_payment(message: types.Message):
    sub_months = {
        300: 1,
        600: 3,
        1000: 12
    }
    now = datetime.now()
    expire_time = now + relativedelta(months=sub_months[message.successful_payment.total_amount // 100])
    print(type(expire_time))
    config = await create_client(expire_time)

    await message.answer(config)


async def create_client(expire_time):
    expire_time_timestamp = expire_time.timestamp()
    date_in_ms = int(expire_time_timestamp * 1000)

    inbounds_db = await session.execute(select(ConfigInbound))
    inbound = inbounds_db.scalars().first()

    with requests.Session() as s:
        data = {
            'username': ADMIN_LOGIN,
            'password': ADMIN_PASSWORD,
        }

        login_resp = s.post(SERVER_URL + "/login", data=data)

        client_resp, client_args = add_client(s, date_in_ms, inbound.id, SERVER_URL)

        if client_resp.get('success'):
            client = ConfigClient(SERVER_URL, *client_args)
            session.add(client)

            config = generate_config(client, inbound)
            await session.commit()

            return config


@dp.message_handler()
async def reply_on(message: types.Message):
    await message.reply("Я вас не понимаю")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
