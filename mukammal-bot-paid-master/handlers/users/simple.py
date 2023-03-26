#PASTDAGILARGA ALOQASI BOLMAGAN ASOSIY IMPORTLAR 
import logging
from aiogram import types
from loader import bot,dp, db
from keyboards.inline.obuna_un_button import check_button
from utils.misc import obunani_tekshiradigan
from data.config import *
#KEYBOARD LAR UCHUN IMPORT 
from aiogram.types import ReplyKeyboardMarkup
from keyboards.default.menyularga import *
#STATE LAR UCHUN IMPORT 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import StateFilter
from aiogram.dispatcher.filters import state
from states.telefon_ism_state import *
#DATABAZA UCHUN IMPORTLAR
import asyncio
########################################################################################################

PHONE_REGEX ="^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
@dp.message_handler(commands=["start"], state=state.any_state)
async def kontakt_sorasin(message: types.Message):
    await message.answer("Botdan to'liq foydalanish uchun iltimos 📲Raqamingizni +998******** shaklida yuboring")
    await FirstStates.kontaktga_state.set()

# @dp.message_handler(is_forwarded=True)
# async def forward_yoq(msg: types.Message):
#     await msg.answer("❌Birovning xabarini ulashmang!!!!!!")

@dp.message_handler(filters.Regexp(PHONE_REGEX),state=FirstStates.kontaktga_state)
async def kontakt_qabul(msg: types.Message, state: FSMContext):
    await msg.answer(f"Kontaktingiz muvaffaqiyatli qabul qilindi✅\n🏠Bosh menyu xizmatingizga tayyor",reply_markup=bosh_menyu)
    await state.finish()
    # await db.create()
    await db.create_table_users()
    await db.add_user(msg.from_user.full_name,msg.from_user.username,msg.from_user.id,f"{msg.text}")
@dp.message_handler(text=["🏠Bosh menyu"] ,state=state.any_state)
async def ism_qabul_qiladigon(msg: types.Message):
    ism = msg.from_user.full_name
    await msg.answer(f"Assalom aleykum {ism}😊. Siz endi botimizdan to'liq foydalanish huquqiga egasiz bo'limlarimizdan o'zingizga keraklisini tanlang!",reply_markup=menyular)
    await state.default_state.set()
@dp.message_handler(text="👤Ma'lumotlarim")
async def malber(msg: types.Message):
    #  await db.create()
     user_id = msg.from_user.id
     a = await db.select_user(f"{user_id}")
     await msg.answer(f"{a[1]}-sizning ismingiz,{a[2]}-username dasiz,{a[3]}-telegram id,{a[4]}-raqamidasiz ma'lumotlaringiz shular")


####################IJARAGA BERISH BO'YICHA KODLAR BOSHLANISHI

@dp.message_handler(text="🏠UY Ijaraga Bermoqchiman")
async def ijarachi(msg: types.Message,state: FSMContext):
    await msg.answer("Shaxarni tanlang",reply_markup=viloyatlar)
    await IjaraStates.Ijara_shaxar_state.set()
@dp.message_handler(state=IjaraStates.Ijara_shaxar_state)
async def shaxar_qabul(msg: types.Message,state: FSMContext):
    await msg.answer("Ijaraga bermoqchi bo'lgan kvartira yoki hovlining honasi nechtadan iborat iltimos raqamda  belgilang👇🏽",reply_markup=xonalar)
    a = ["Toshkent","Fargona","Andijon","Buxoro","Namangan","Jizzax","Xorazm","Navoiy","Qashqadaryo","Qoraqalpogiston","Samarqand","Sirdaryo","Surxondaryo"]
    shaxar = msg.text
    if shaxar in a:
        await state.update_data({
            "shaxar": shaxar
        })
        await msg.answer("Shaxar qabul qilindi keyingi qadam manzilingizni yuboring",reply_markup=orqaga)
        await IjaraStates.Ijara_xona_state.set()
    else:
        await msg.answer("menyudan tanlang",reply_markup=viloyatlar)
@dp.message_handler(state=IjaraStates.Ijara_xona_state)
async def xona_qabul(msg: types.Message,state: FSMContext):
    xona = int(msg.text)
    xona2 = xona
    print(type(xona2))
    if xona2 < 100000000:
        await state.update_data({
            "xona":xona2
        })
        await msg.answer("xona qabul qilindi✅ \n aniq manzilingizni kiriting",reply_markup=bosh_menyu)
        await IjaraStates.Ijara_manzil_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')
@dp.message_handler(state=IjaraStates.Ijara_manzil_state)
async def manzil_qabul(msg:types.Message,state: FSMContext):
    manzil = str(msg.text)
    await msg.answer("Manzilingiz qabul qilindi keyingi qadam narx ni yozib qoldiring",reply_markup=None)
    await state.update_data({
        "manzil": manzil
    })
    await IjaraStates.Ijara_narx_state.set()
@dp.message_handler(state=IjaraStates.Ijara_narx_state)
async def narx_qabul(msg: types.Message,state: FSMContext):
    narx = str(msg.text)
    await msg.answer("Barcha uy haqidagi ma'lumotlar saqlandi ijarachi topilishi bilan sizga admin aloqaga chiqadi",reply_markup=menyular)
    await state.update_data({
        "narx": narx
    })
    data = await state.get_data()
    shaxar = data.get("shaxar")
    xona = data.get("xona")
    manzil = data.get("manzil")
    narx = data.get("narx")
    # await db.create()
    await db.create_table_Uylar()
    await db.add_uy(shaxar=f"{shaxar}", xonalari=xona, manzil=f"{manzil}", narx=f"{narx}")
    await state.finish()
    # rasm = data.get("rasm")

####################IJARAGA BERISH BO'YICHA KODLAR TUGADI


@dp.message_handler(text="🔑UY Ijaraga olmoqchiman")
async def ijara_olmoqchi_shaxar(msg: types.Message,state: FSMContext):
    await msg.answer("Qaysi viloyatdan Ijaraga uy olmoqchisiz belgilang👇🏽",reply_markup=viloyatlar)
    await Ijragaoledgon.Ijara_oledgon_shaxar_state.set()

@dp.message_handler(state=Ijragaoledgon.Ijara_oledgon_shaxar_state)
async def ijara_olmoqchi_shaxardi_ezganda(msg: types.Message,state: FSMContext):
    await msg.answer("Viloyat qabul qilindi necha xonalik uylardan bo'lsin belgilang👇🏽",reply_markup=xonalar)
    viloyat = str(msg.text)
    viloyat2 = viloyat.capitalize()

    await state.update_data({
        "viloyat": viloyat2
    })
    await Ijragaoledgon.Ijara_oledgon_xona_state.set()

@dp.message_handler(state=Ijragaoledgon.Ijara_oledgon_xona_state)
async def ijara_olmoqchi_xonani_ezganda(msg: types.Message,state: FSMContext):
    await msg.answer("Xona qabul qilindi✅ Tez orada sizga variant lar yuboriladi",reply_markup=orqaga)
    xona = msg.text
    await state.update_data({
        "xona": xona
    })
    data = await state.get_data()
    viloyat = data.get("viloyat")
    xona = data.get("xona")
    # await db.create()
    baza_uylar = await db.select_uy(shaxar_ber=f"{viloyat}",xona_ber=f"{xona}")
    tanlangan_uylar_soni = await db.select_uy_count(shaxar_ber=f"{viloyat}",xona_ber=f"{xona}")
    i = 0
    text=' '
    while True:
        text = baza_uylar
        await msg.answer(f"{text[1]}-shaxridan,{text[2]}-xonalik,{text[3]}-manzili,{text[4]}-narxi shundan iborat")
        i+=1
        if i == tanlangan_uylar_soni[0]:
            await msg.answer("Bor uylar shular edi",reply_markup=bosh_menyu)
            await state.finish()
            break

        
@dp.message_handler(text="Barcha Uylar")
async def barcha_uylar(msg: types.Message):
    # await db.create()
    uylarhammasi = await db.select_all_uylar()
    print(uylarhammasi)
    uylarsoni = await db.count_uylar()
    text = ' '
    uylarhammasi2 = uylarhammasi
    a=0
    while True:
        text = uylarhammasi2
        await msg.answer(f"{text[a][1]}-shaxridan,{text[a][2]}-xonalik,{text[a][3]}-manzili,{text[a][4]}-narxi shundan iborat")
        a+=1
        if a == uylarsoni:
            await msg.answer("Bor uylar shular edi")
            break
        
####################IJARAGA Olish BO'YICHA KODLAR TUGADI

@dp.message_handler(text="🏡Uyimni Sotmoqchiman")
async def seller(msg: types.Message,state: FSMContext):
    await msg.answer("Sotmoqchi bolgan uyingiz kvartira yoki hovlimi ? 👇🏽pastdagi tugmalar orqali belgilang",reply_markup=kvartira_hovli)
    await Sotadigan.Sotadigan_kvartira_hovli_state.set()

@dp.message_handler(state=Sotadigan.Sotadigan_kvartira_hovli_state,text="🏬Kvartira")
async def seller2(msg: types.Message,state: FSMContext):
    # await db.create()
    await db.create_table_Kvartiralar()
    await msg.answer('Siz sotmoqchi bo`lgan uyingiz qaysi shaxarda pastdagi tugmalar orqali belgilang',reply_markup=viloyatlar)
    await Sotadigan.shaxar_state.set()

@dp.message_handler(state=Sotadigan.shaxar_state)
async def qobketgan1(msg: types.Message,state: FSMContext):
    a = ["Toshkent","Fargona","Andijon","Buxoro","Namangan","Jizzax","Xorazm","Navoiy","Qashqadaryo","Qoraqalpogiston","Samarqand","Sirdaryo","Surxondaryo"]
    shaxar = msg.text
    if shaxar in a:
        await state.update_data({
            "shaxar": shaxar
        })
        await msg.answer("Shaxar qabul qilindi keyingi qadam manzilingizni yuboring",reply_markup=orqaga)
        await Sotadigan.manzil_state.set()
    else:
        msg.answer("Faqat tugmalar orqali belgilang iltimos",reply_markup=viloyatlar)

@dp.message_handler(state=Sotadigan.manzil_state)
async def qobketgan2(msg: types.Message,state: FSMContext):
    manzil = msg.text
    await state.update_data({
        "manzil":manzil
    })
    await msg.answer("Manzilingiz qabul qilindi uyingiz necha kvadrat metr dan iborat buni faqatgina raqamda belgilang")
    await Sotadigan.kvadrat_state.set()

@dp.message_handler(state=Sotadigan.kvadrat_state)
async def seller3(msg: types.Message,state: FSMContext):
    print(type(msg))
    kvadrat = int(msg.text)
    kvadrat2 = kvadrat
    print(type(kvadrat2))
    if kvadrat2 < 100000000:
        await state.update_data({
            "kvadrat":kvadrat2
        })
        await msg.answer('Kvadrat qabul qilindi✅ \n kvartira necha xonadan iborat ekanini 👇🏽pastdagi tugmalar orqali belgilang',reply_markup=xonalar)
        await Sotadigan.xona_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')

@dp.message_handler(state=Sotadigan.xona_state)
async def seller4(msg: types.Message,state: FSMContext):
    print(type(msg))
    xona = int(msg.text)
    xona2 = xona
    print(type(xona2))
    if xona2 < 100000000:
        await state.update_data({
            "xona":xona2
        })
        await msg.answer('xona qabul qilindi✅ \n kvartira necha qavatda ekanini 👇🏽pastdagi tugmalar orqali belgilang',reply_markup=xonalar)
        await Sotadigan.qavat_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')


@dp.message_handler(state=Sotadigan.qavat_state)
async def seller5(msg: types.Message,state: FSMContext):
    print(type(msg))
    qavat = int(msg.text)
    qavat2 = qavat
    print(type(qavat2))
    if qavat2 < 100000000:
        await state.update_data({
            "qavat":qavat2
        })
        await msg.answer('qavat qabul qilindi✅ \n romlaringizni nomini yozib qoldiring',reply_markup=orqaga)
        await Sotadigan.romlar_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')

@dp.message_handler(state=Sotadigan.romlar_state)
async def seller6(msg: types.Message,state: FSMContext):
    romlari = msg.text
    await state.update_data({
        "romlari":romlari
    })
    await msg.answer('romlaringiz qabul qilindi✅ \n endigi navbat eshiklaringizni nomini yozib qoldiring',reply_markup=orqaga)
    await Sotadigan.eshiklari_state.set()

@dp.message_handler(state=Sotadigan.eshiklari_state)
async def seller7(msg: types.Message,state: FSMContext):
    eshiklari = msg.text
    await state.update_data({
        "eshiklari":eshiklari
    })
    await msg.answer('eshiklaringiz qabul qilindi✅ \n endigi navbat gishtlaringizni nomini yozib qoldiring',reply_markup=orqaga)
    await Sotadigan.gishtlari_state.set()


@dp.message_handler(state=Sotadigan.gishtlari_state)
async def seller8(msg: types.Message,state: FSMContext):
    gishtlari = msg.text
    await state.update_data({
        "gishtlari":gishtlari
    })
    await msg.answer('gishtlaringiz qabul qilindi✅ \n Xosh uyingizda gaz bormi bolsa pastadgi xa ni bosing bolmasa yoq tugmachasini ',reply_markup=isitish)
    await Sotadigan.isitish_state.set()

@dp.message_handler(state=Sotadigan.isitish_state)
async def seller9(msg: types.Message,state: FSMContext):
    isitish = msg.text
    if isitish == "xa" or "yoq":            
        await state.update_data({
            "isitish":isitish
        })
        await msg.answer('isitish javobingiz qabul qilindi✅ \n uyingizning umumiy xolatini qanday baholaysiz pastadgi tugmachalar orqali kiriting ',reply_markup=xolati)
        await Sotadigan.xolati_state.set()
    else:
        await msg.answer('notogri variant kiritildi buyruqlardan birini tanlang',reply_markup=isitish)

@dp.message_handler(state=Sotadigan.xolati_state)
async def seller10(msg: types.Message,state: FSMContext):
    xolati = msg.text
    if xolati == "super" or "yaxshi" or "ortacha" or "yomon":            
        await state.update_data({
            "xolati":xolati
        })
        await msg.answer('xolatingiz qabul qilindi✅ \n uyingizda qoldirib ketmoqchi bolgan buyumlaringiz bolsa yozib qoldiring',reply_markup=orqaga)
        await Sotadigan.qoladigan_state.set()
    else:
        await msg.answer('notogri variant kiritildi buyruqlardan birini tanlang',reply_markup=xolati)


@dp.message_handler(state=Sotadigan.qoladigan_state)
async def seller11(msg: types.Message,state: FSMContext):
    qoladigan = msg.text
    await state.update_data({
        "qoladigan":qoladigan
    })
    await msg.answer('qoladiganlaringiz qabul qilindi✅ \n oxirgi qadamlardan bittasi uyingizni narxini yozib qoldiring',reply_markup=orqaga)
    await Sotadigan.narx_state.set()


@dp.message_handler(state=Sotadigan.narx_state)
async def seller12(msg: types.Message,state: FSMContext):
    narx = msg.text
    await state.update_data({
        "narx":narx
    })
    await msg.answer('narx qabul qilindi✅ \n huuuh endi faqat uyingizni rasmlarini jonatishingiz qoldi.. ',reply_markup=orqaga)
    await Sotadigan.rasmlari.set()

@dp.message_handler(state=Sotadigan.rasmlari,content_types="photo")
async def seller13(msg: types.Message,state: FSMContext):
    print("#############")
    print(msg)
    rasm = str(msg.photo[-1].file_id)
    print("###################")
    print(rasm)
    print("###################")
    await bot.send_photo(chat_id=BAZA_CHANNEL[0],photo=f"{rasm}",caption=f"{rasm}")
    # await bot.send_message(chat_id=BAZA_CHANNEL[0],text=f"{rasm}")
    await state.update_data({
        "rasm": rasm
    })
    
    data = await state.get_data()
    # if data.get("rasm")==None:
    #     l = [rasm]
    # else:
    #     l = data.get('rasm').append(rasm)
    # await state.update_data({'rasm': l})
    shaxar = data.get("shaxar")
    manzil = data.get("manzil")
    kvadrat = data.get("kvadrat")
    xona = data.get("xona")
    qavat = data.get("qavat")
    romlari = data.get("romlari")
    eshiklari = data.get("eshiklari")
    gishtlari = data.get("gishtlari")
    isitish = data.get("isitish")
    xolati = data.get("xolati")
    qoladigan = data.get("qoladigan")
    narx = data.get("narx")
    rasmi = data.get("rasm")
    # await db.create()
    await db.add_kvartira(shaxar,manzil,kvadrat,xona,qavat,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmi)
    await msg.answer("Xammasi uchun raxmat xaridor topilishi bilan aloqaga chiqamiz",reply_markup=bosh_menyu)
    await state.finish()

########################## KVARTIRA SOTADIGAN  KODLAR TUGADI ###################################################################


@dp.message_handler(state=Sotadigan.Sotadigan_kvartira_hovli_state,text="🏡Hovli")
async def seller_hovli1(msg: types.Message,state: FSMContext):
    # await db.create()
    await db.create_table_Hovlilar()
    await msg.answer("Siz sotmoqchi bo'lgan hovlingiz qaysi shaxarda pastdagi tugmalar orqali belgilang",reply_markup=viloyatlar)
    await Sotadigan2.shaxar_state.set()

@dp.message_handler(state=Sotadigan2.shaxar_state)
async def seller_hovli2(msg: types.Message,state: FSMContext):
    a = ["Toshkent","Fargona","Andijon","Buxoro","Namangan","Jizzax","Xorazm","Navoiy","Qashqadaryo","Qoraqalpogiston","Samarqand","Sirdaryo","Surxondaryo"]
    shaxar = msg.text
    if shaxar in a:
        await state.update_data({
            "shaxar": shaxar
        })
        await msg.answer("Shaxar qabul qilindi keyingi qadam manzilingizni yuboring",reply_markup=orqaga)
        await Sotadigan2.manzil_state.set()
    else:
        msg.answer("Faqat tugmalar orqali belgilang iltimos",reply_markup=viloyatlar)

@dp.message_handler(state=Sotadigan2.manzil_state)
async def seller_hovli3(msg: types.Message,state: FSMContext):
    manzil = msg.text
    await state.update_data({
        "manzil":manzil
    })
    await msg.answer("Manzilingiz qabul qilindi hovlingiz necha kvadrat metr dan iborat buni faqatgina raqamda belgilang")
    await Sotadigan2.kvadrat_state.set()

@dp.message_handler(state=Sotadigan2.kvadrat_state)
async def seller_hovli35(msg: types.Message,state: FSMContext):
    print(type(msg))
    kvadrat = int(msg.text)
    kvadrat2 = kvadrat
    print(type(kvadrat2))
    if kvadrat2 < 100000000:
        await state.update_data({
            "kvadrat":kvadrat2
        })
        await msg.answer('Kvadrat qabul qilindi✅ \n hovli necha xonadan iborat ekanini 👇🏽pastdagi tugmalar orqali belgilang',reply_markup=xonalar)
        await Sotadigan2.xona_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')

@dp.message_handler(state=Sotadigan2.xona_state)
async def seller_hovli4(msg: types.Message,state: FSMContext):
    print(type(msg))
    xona = int(msg.text)
    xona2 = xona
    print(type(xona2))
    if xona2 < 100000000:
        await state.update_data({
            "xona":xona2
        })
        await msg.answer("xona qabul qilindi✅ \n hovli romlari qanday ekanini yozib qoldiring taxta yoki akfa shunga o'xshash narsalar",reply_markup=bosh_menyu)
        await Sotadigan2.romlar_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')


@dp.message_handler(state=Sotadigan2.romlar_state)
async def seller_hovli5(msg: types.Message,state: FSMContext):
    romlari = msg.text
    await state.update_data({
        "romlari":romlari
    })
    await msg.answer('romlaringiz qabul qilindi✅ \n endigi navbat eshiklaringizni nomini yozib qoldiring',reply_markup=orqaga)
    await Sotadigan2.eshiklari_state.set()

@dp.message_handler(state=Sotadigan2.eshiklari_state)
async def seller_hovli6(msg: types.Message,state: FSMContext):
    eshiklari = msg.text
    await state.update_data({
        "eshiklari":eshiklari
    })
    await msg.answer('eshiklaringiz qabul qilindi✅ \n endigi navbat gishtlaringizni nomini yozib qoldiring',reply_markup=orqaga)
    await Sotadigan2.gishtlari_state.set()


@dp.message_handler(state=Sotadigan2.gishtlari_state)
async def seller_hovli7(msg: types.Message,state: FSMContext):
    gishtlari = msg.text
    await state.update_data({
        "gishtlari":gishtlari
    })
    await msg.answer('gishtlaringiz qabul qilindi✅ \n Xosh uyingizda gaz bormi bolsa pastadgi xa ni bosing bolmasa yoq tugmachasini ',reply_markup=isitish)
    await Sotadigan2.isitish_state.set()

@dp.message_handler(state=Sotadigan2.isitish_state)
async def seller_hovli8(msg: types.Message,state: FSMContext):
    isitish = msg.text
    if isitish == "xa" or "yoq":            
        await state.update_data({
            "isitish":isitish
        })
        await msg.answer('isitish javobingiz qabul qilindi✅ \n uyingizning umumiy xolatini qanday baholaysiz pastadgi tugmachalar orqali kiriting ',reply_markup=xolati)
        await Sotadigan2.xolati_state.set()
    else:
        await msg.answer('notogri variant kiritildi buyruqlardan birini tanlang',reply_markup=isitish)

@dp.message_handler(state=Sotadigan2.xolati_state)
async def seller_hovli9(msg: types.Message,state: FSMContext):
    xolati = msg.text
    if xolati == "super" or "yaxshi" or "ortacha" or "yomon":            
        await state.update_data({
            "xolati":xolati
        })
        await msg.answer('xolatingiz qabul qilindi✅ \n uyingizda qoldirib ketmoqchi bolgan buyumlaringiz bolsa yozib qoldiring',reply_markup=orqaga)
        await Sotadigan2.qoladigan_state.set()
    else:
        await msg.answer('notogri variant kiritildi buyruqlardan birini tanlang',reply_markup=xolati)


@dp.message_handler(state=Sotadigan2.qoladigan_state)
async def seller_hovli10(msg: types.Message,state: FSMContext):
    qoladigan = msg.text
    await state.update_data({
        "qoladigan":qoladigan
    })
    await msg.answer('qoladiganlaringiz qabul qilindi✅ \n oxirgi qadamlardan bittasi uyingizni narxini yozib qoldiring',reply_markup=orqaga)
    await Sotadigan2.narx_state.set()


@dp.message_handler(state=Sotadigan2.narx_state)
async def seller_hovli11(msg: types.Message,state: FSMContext):
    narx = msg.text
    await state.update_data({
        "narx":narx
    })
    await msg.answer('narx qabul qilindi✅ \n huuuh endi faqat uyingizni rasmlarini jonatishingiz qoldi..',reply_markup=orqaga)
    await Sotadigan2.rasmlari.set()

@dp.message_handler(state=Sotadigan2.rasmlari,content_types="photo")
async def seller_hovli12(msg: types.Message,state: FSMContext):
    print("#############")
    print(msg)
    rasm = str(msg.photo[-1].file_id)
    print("###################")
    print(rasm)
    print("###################")
    await bot.send_photo(chat_id=BAZA_CHANNEL[0],photo=f"{rasm}",caption=f"{rasm}")
    await state.update_data({
        "rasm":rasm
    })
    data = await state.get_data()
    shaxar = data.get("shaxar")
    manzil = data.get("manzil")
    kvadrat = data.get("kvadrat")
    xona = data.get("xona")
    romlari = data.get("romlari")
    eshiklari = data.get("eshiklari")
    gishtlari = data.get("gishtlari")
    isitish = data.get("isitish")
    xolati = data.get("xolati")
    qoladigan = data.get("qoladigan")
    narx = data.get("narx")
    rasmi = data.get("rasm")
    # await db.create()
    await db.add_hovli(shaxar,manzil,kvadrat,xona,romlari,eshiklari,gishtlari,isitish,xolati,qoladigan,narx,rasmi)
    await msg.answer("Xammasi uchun raxmat xaridor topilishi bilan aloqaga chiqamiz",reply_markup=bosh_menyu)
    await state.finish()

########################HOVLI SOTEDGON KODLARI TUGADI##################################################################################


@dp.message_handler(text="🏘Sotiladigan Uylar")
async def kvarita_or_hovli(msg: types.Message,state: FSMContext):
    await msg.answer("Qaysi turdagi uy sotib olmoqchisiz belgilang👇🏽",reply_markup=kvartira_hovli)

@dp.message_handler(text="🏬Kvartira")
async def client1(msg: types.Message,state: FSMContext):
    await msg.answer("Tushunarli qaysi shaxardan bo'lsin kvartira👇🏽",reply_markup=viloyatlar)
    await Kvartira_Oledgon.shaxar_state.set()

@dp.message_handler(state=Kvartira_Oledgon.shaxar_state)
async def client2(msg: types.Message,state: FSMContext):
    a = ["Toshkent","Fargona","Andijon","Buxoro","Namangan","Jizzax","Xorazm","Navoiy","Qashqadaryo","Qoraqalpogiston","Samarqand","Sirdaryo","Surxondaryo"]
    shaxar = msg.text
    if shaxar in a:
            await state.update_data({
                "shaxar": shaxar
            })
            await msg.answer("Shaxar qabul qilindi Necha kvadratlik kvartira bo'lsin?",reply_markup=bosh_menyu)
            await Kvartira_Oledgon.kvadrat_state.set()
    else:
            msg.answer("Faqat tugmalar orqali belgilang iltimos",reply_markup=viloyatlar)

@dp.message_handler(state=Kvartira_Oledgon.kvadrat_state)
async def client3(msg: types.Message,state: FSMContext):
    print(type(msg))
    kvadrat = int(msg.text)
    kvadrat2 = kvadrat
    print(type(kvadrat2))
    if kvadrat2 < 100000000:
        await state.update_data({
            "kvadrat":kvadrat2
        })
        await msg.answer("Kvadrat qabul qilindi✅ \n kvartira necha xonadan iborat bo'lishi kerak ekanini 👇🏽pastdagi tugmalar orqali belgilang",reply_markup=xonalar)
        await Kvartira_Oledgon.xona_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')

@dp.message_handler(state=Kvartira_Oledgon.xona_state)
async def client4(msg: types.Message,state: FSMContext):
    print(type(msg))
    xona = int(msg.text)
    xona2 = xona
    print(type(xona2))
    if xona2 < 100000000:
        await state.update_data({
            "xona":xona2
        })
        await msg.answer("xona qabul qilindi✅ \n kvartirani nechinchi qavatda bolishini xoxlaysiz?",reply_markup=xonalar)
        await Kvartira_Oledgon.qavat_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')

@dp.message_handler(state=Kvartira_Oledgon.qavat_state)
async def client5(msg: types.Message,state: FSMContext):
    print(type(msg))
    qavat = int(msg.text)
    qavat2 = qavat
    print(type(qavat2))
    if qavat2 < 100000000:
        await state.update_data({
            "qavat":qavat2
        })
        await msg.answer('qavat qabul qilindi✅ \n sizga isitish tizimi yani gazi bor kvartira kerakmi pastdagi tugma orqali belgilang',reply_markup=isitish)
        await Kvartira_Oledgon.isitish_state.set()
    else:
        await msg.answer('faqat raqam bosn ddm sanga')


@dp.message_handler(state=Kvartira_Oledgon.isitish_state)
async def client6(msg: types.Message,state: FSMContext):
    isitish = msg.text
    if isitish == "xa" or "yoq":            
        await state.update_data({
            "isitish":isitish
        })
        await msg.answer('isitish javobingiz qabul qilindi✅ \n uyingizning umumiy xolatini qanday baholaysiz pastadgi tugmachalar orqali kiriting ',reply_markup=xolati)
        await Kvartira_Oledgon.xolati_state.set()
    else:
        await msg.answer('notogri variant kiritildi buyruqlardan birini tanlang',reply_markup=isitish)


@dp.message_handler(state=Kvartira_Oledgon.xolati_state)
async def client7(msg: types.Message,state: FSMContext):
    xolati = msg.text
    if xolati == "super" or "yaxshi" or "ortacha" or "yomon":            
        await state.update_data({
            "xolati":xolati
        })
        await msg.answer("barchasi qabul qilindi✅ \n tez orada sizga to'g'ri keladigan uylarni yuboramiz agar ular yo'q bo'lsa siga tavsiyamiz barcha uylar  buyruqidan foydalaning",reply_markup=orqaga)
    else:
        await msg.answer('notogri variant kiritildi buyruqlardan birini tanlang',reply_markup=xolati)


    data = await state.get_data()
    shaxar = data.get("shaxar")
    kvadrat = data.get("kvadrat")
    xona = data.get("xona")
    qavat = data.get("qavat")
    isitish = data.get("isitish")
    xolat = data.get("xolati")
    print(shaxar,kvadrat,xona,qavat,isitish,xolat)
    print("########################################")
    # await db.create()
    baza_uylar = await db.select_kvartira(shaxar,kvadrat,xona,qavat,isitish,xolat)
    tanlangan_uylar_soni = await db.select_kvartira_count(shaxar,kvadrat,xona,qavat,isitish,xolat)
    print(baza_uylar[0])
    print("########################################")
    i = 0
    text=' '
    while True:
        text = baza_uylar
        await msg.answer_photo(photo=f"{text[13]}",caption=f"✅Маълумотлар:\n🗄➡️{text[3]} кв.м,\n🗄➡️{text[4]} хона,\n🗄➡️{text[5]}-Қават,\n🗄➡️Ромлари: {text[6]},\n🗄➡️Эшиклар: {text[7]},\n🗄➡️{text[8]}-Ғиштли,\n🗄➡️Иситиш тизими борми-{text[9]},\n⏺➡️Холати:{text[10]},\n✅Қоладиган жихозлар:{text[11]}")
        i+=1
        if i == tanlangan_uylar_soni[0]:
            await msg.answer("Bor kvartiralar shular edi",reply_markup=bosh_menyu)
            await state.finish()
            break


@dp.message_handler(state=state.any_state, text="🧑‍💻Dasturchi bilan aloqa")
async def dasturchi(msg: types.Message,state: FSMContext):
    await msg.answer("@kanonir24 xar qanday takliflar uchun")

@dp.message_handler(state=state.any_state, text="🏠Barcha Uylar")
async def dasturchi(msg: types.Message,state: FSMContext):
    barcha = await db.se


















# @dp.callback_query_handler(text="check_subs")
# async def checker(call: types.CallbackQuery):
#     await call.answer()
#     result = str()
#     for channel in CHANNELS:
#         status = await obunani_tekshiradigan.check(user_id=call.from_user.id, 
#                                                     channel=channel)
#         channel = await bot.get_chat(channel)
#         if status:
#             result += f"✅<b>{channel.title}</b> kanaliga obuna bolgansiz!\n\n"
#         else:
#             invite_link = await channel.export_invite_link()
#             result += (f"❌<b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
#                         f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

#     await call.message.answer(result, disable_web_page_preview=True)
    