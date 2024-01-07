from aiogram import Bot, Dispatcher, executor, types
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
      
   
@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == "month":
        await bot.send_message(chat_id=callback_query.from_user.id,text="Вы выбрали подписку на месяц")
    elif callback_query.data == "3month":
        await bot.send_message(chat_id=callback_query.from_user.id,text="Вы выбрали подписку на 3 месяца")
    elif callback_query.data == "year":
        await bot.send_message(chat_id=callback_query.from_user.id,text="Вы выбрали подписку на год")
        
@dp.message_handler()
async def reply_on(message: types.Message):
    await message.reply("Я вас не понимаю")
    
    

if __name__ == "__main__":
    executor.start_polling(dp,on_startup=on_startup,skip_updates=True)