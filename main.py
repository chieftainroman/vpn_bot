from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from datetime import datetime
from dateutil.relativedelta import relativedelta
from aiogram.types import Message,LabeledPrice,ContentType
from dotenv import load_dotenv
from app import keyboards as kb
from app import database as db
from vpn_methods.constants import *
from vpn_methods.main import add_client,add_inbound,generate_config
from app.database import *
import os
import requests
import json

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
    await message.answer(start_words,reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f"Добро пожаловать {message.from_user.full_name} ",reply_markup=kb.main_admin)  
    
    
    
@dp.message_handler(text="Купить")
async def buy_product(message: types.Message):
    await message.answer("Просмотрите варианты наших товаров!",reply_markup=kb.buy_variants) 

@dp.message_handler(text="Инструкция пользования")
async def using_instruction(message: types.Message):
    await message.answer("Инструкция",reply_markup=kb.instruction_keyboard) 

@dp.message_handler(text="Админ-панель")
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Вы вошли в админ панель",reply_markup=kb.main_admin_panel) 
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
            inbound_resp = add_inbound(s)
            if inbound_resp.get('success'):
                create_info = inbound_resp.get("obj")
                stream_settings = json.loads(create_info.get('streamSettings'))
                reality_settings = stream_settings.get('realitySettings')
                data_dict = {"id":create_info.get("id"),"url":SERVER_URL,"port":create_info.get('port'),"transmission":stream_settings.get('network'),"security":stream_settings.get('security'),"public_key":reality_settings.get('settings').get('publicKey'),"private_key":reality_settings.get('privateKey'),"fingerprint":reality_settings.get('settings').get('fingerprint'),"server_name":reality_settings.get('serverNames')[0],"short_id":reality_settings.get('shortIds')[0],"remark":create_info.get('remark'),}
                indound = session.add(ConfigInbound(**data_dict))
                await session.commit()
                await message.answer("Inbound был добавлен")
            else:
                await message.answer("Идите нахуй")
    else:
        await message.reply("Я вас не понимаю")
        
@dp.message_handler(text="Назад")
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Возвращаемся в главное",reply_markup=kb.main_admin) 
    else:
        await message.reply("Я вас не понимаю")
      
   
@dp.callback_query_handler(text="month")
async def order_month(message:Message):
    await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка VPN',
        description="Покупка впн на месяц",
        payload = "Pyament through a bot",
        provider_token='381764678:TEST:75091',
        currency="rub",
        prices=[
            LabeledPrice(
                label = 'VPN на месяц',
                amount = 30000
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
async def order_3month(message:Message):
    await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка VPN',
        description="Покупка впн на 3 месяца",
        payload = "Pyament through a bot",
        provider_token='381764678:TEST:75091',
        currency="rub",
        prices=[
            LabeledPrice(
                label = 'VPN на 3 месяца',
                amount = 60000
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
async def order_year(message:Message):
    await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка VPN',
        description="Покупка впн на год",
        payload = "Pyament through a bot",
        provider_token='381764678:TEST:75091',
        currency="rub",
        prices=[
            LabeledPrice(
                label = 'VPN на год',
                amount = 100000
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
    
 
    
@dp.pre_checkout_query_handler(lambda query :True)
async def pre_checkout_query(pre_checkout_q:types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id,ok=True)   
   
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT,)
async def succesful_payment(message: types.Message):
    if message.successful_payment.total_amount // 100 == 300:
        now = datetime.now()
        expire_time = now + relativedelta(months=1)
        expire_time_timestamp = expire_time.timestamp()
        inbound_db = await session.execute(select(ConfigInbound))
        inbound_db_data = {"id":"","url":"","port":"","transmission":"","security":"","public_key":"","private_key":"","fingerprint":"","server_name":"","short_id":"","remark":"",}
        for i in inbound_db.scalars():
            inbound_db_data = {
                "id":i.id,"url":i.url,"port":i.port,"transmission":i.transmission,"security":i.security,"public_key":i.public_key,"private_key":i.private_key,"fingerprint":i.fingerprint,"server_name":i.server_name,"short_id":i.short_id,"remark":i.remark,
            }
        with requests.Session() as s:
            data = {
                'username': ADMIN_LOGIN,
                'password': ADMIN_PASSWORD,
            }

            login_resp = s.post(SERVER_URL + "/login", data=data)
            print(login_resp.json())
            client_resp, client_args = add_client(s, expire_time_timestamp, inbound_db_data["id"])

            client_args.append(inbound_db_data["id"])
            if client_resp.get('success'):
                client_data_dict = {"id":str(client_args[0]),"url":inbound_db_data["url"],"sub_id":client_args[1],"expire_time":expire_time_timestamp,"flow":client_args[2],"email":client_args[3],"inbound_id":client_args[4]}
                client_add = session.add(ConfigClient(**client_data_dict))
                await session.commit()
                result = await session.execute(select(ConfigClient))
                client = result.fetchone()
                config = generate_config(client_data_dict,inbound_db_data)
                await message.answer(config)
    elif message.successful_payment.total_amount // 100 == 600:
        now = datetime.now()
        expire_time = now + relativedelta(months=3)
    elif message.successful_payment.total_amount // 100 == 1000:
        now = datetime.now()
        expire_time = now + relativedelta(months=12)
        
    

    
@dp.message_handler()
async def reply_on(message: types.Message):
    await message.reply("Я вас не понимаю")
    
    

if __name__ == "__main__":
    executor.start_polling(dp,on_startup=on_startup,skip_updates=True)