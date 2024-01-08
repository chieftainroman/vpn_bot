from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message,LabeledPrice,ContentType
from dotenv import load_dotenv
from app import keyboards as kb
from app import database as db
import os


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

async def on_startup(_):
    await db.db_start()
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
        max_tip_amount=5000,
        suggested_tip_amounts=[1000,2000,3000,4000],
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
        max_tip_amount=5000,
        suggested_tip_amounts=[1000,2000,3000,4000],
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
        max_tip_amount=5000,
        suggested_tip_amounts=[1000,2000,3000,4000],
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
   
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def succesful_payment(message: Message):
    if message.successful_payment.total_amount // 100 == 300:
        await message.answer("Вам будет выслан конфиг на месяц")
    elif message.successful_payment.total_amount // 100 == 600:
        await message.answer("Вам будет выслан конфиг на 3 месяца")
    elif message.successful_payment.total_amount // 100 == 600:
        await message.answer("Вам будет выслан конфиг на год")

    
@dp.message_handler()
async def reply_on(message: types.Message):
    await message.reply("Я вас не понимаю")
    
    

if __name__ == "__main__":
    executor.start_polling(dp,on_startup=on_startup,skip_updates=True)