from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

bosh_menyu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[
        KeyboardButton("🏠Bosh menyu")
    ]]
)
menyular = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("🏠UY Ijaraga Bermoqchiman")],
        [KeyboardButton("🔑UY Ijaraga olmoqchiman")],
        [KeyboardButton("🏡Uyimni Sotmoqchiman"),KeyboardButton("🏘Sotiladigan Uylar")],
        [KeyboardButton("👤Ma'lumotlarim"),KeyboardButton("🧑‍💻Dasturchi bilan aloqa")],
        [KeyboardButton("🏠Barcha Uylar")]
    ]
)
viloyatlar = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("Toshkent"),KeyboardButton("Fargona"),KeyboardButton("Andijon")],
        [KeyboardButton("Buxoro"),KeyboardButton("Namangan"),KeyboardButton("Jizzax")],
        [KeyboardButton("Xorazm"),KeyboardButton("Navoiy"),KeyboardButton("Qashqadaryo")],
        [KeyboardButton("Qoraqalpogiston"),KeyboardButton("Samarqand"),KeyboardButton("Sirdaryo"),KeyboardButton("Surxondaryo")],
        [KeyboardButton("🏠Bosh menyu")]
    ]
)
xonalar = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
    [KeyboardButton("1"),KeyboardButton("2"),KeyboardButton("3"),KeyboardButton("4"),KeyboardButton("5")],
    [KeyboardButton("6"),KeyboardButton("7"),KeyboardButton("8"),KeyboardButton("9"),KeyboardButton("10")],
    [KeyboardButton("🏠Bosh menyu")]
    ]
)
orqaga = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("🏠Bosh menyu")]
    ]
)
kvartira_hovli = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("🏬Kvartira"),KeyboardButton("🏡Hovli")],
        [KeyboardButton("🏠Bosh menyu")]
    ]
)
isitish = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton('xa'),KeyboardButton('yoq')],
        [KeyboardButton("🏠Bosh menyu")]
    ]
)

xolati = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton('super'),KeyboardButton('yaxshi')],
        [KeyboardButton('ortacha'),KeyboardButton('yomon')],
        [KeyboardButton("🏠Bosh menyu")]
    ]
)