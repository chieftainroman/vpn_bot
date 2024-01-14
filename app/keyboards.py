from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton



main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add("Купить").add("Инструкция пользования")

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add("Купить").add("Инструкция пользования").add("Админ-панель")

main_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin_panel.add("Добавить сервер").add("Просмотреть пользователей").add("Назад")

buy_variants = InlineKeyboardMarkup(row_width=1)
buy_variants.add(InlineKeyboardButton(text="Купить на месяц (300 руб)",callback_data="month"),
                 InlineKeyboardButton(text="Купить на 3 месяца (600 руб)",callback_data="3month"),
                 InlineKeyboardButton(text="Купить на год (1000 руб)",callback_data="year"),
                 ) 

''' buy_variants = ReplyKeyboardMarkup(resize_keyboard=True)
buy_variants.add("Купить на месяц (300руб)").add("Купить на 3 месяца (600руб)").add("Купить на год (1000руб)") '''

instruction_keyboard = InlineKeyboardMarkup(row_width=2)
instruction_keyboard.add(InlineKeyboardButton(text="Для Iphone",url="https://sites.google.com/view/xrayiphone/%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F-%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"),
                         InlineKeyboardButton(text="Для Android",url='https://sites.google.com/view/xrayy/%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F-%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'))