from aiogram.dispatcher.filters.state import StatesGroup,State

class FirstStates(StatesGroup):
    kontaktga_state = State()
    ismga_state = State()

class IjaraStates(StatesGroup):
    Ijara_shaxar_state = State()
    Ijara_xona_state = State()
    Ijara_rasm_state = State()
    Ijara_manzil_state = State()
    Ijara_narx_state = State()

class Ijragaoledgon(StatesGroup):
    Ijara_oledgon_shaxar_state = State()
    Ijara_oledgon_xona_state = State()

class Sotadigan(StatesGroup):
    Sotadigan_kvartira_hovli_state = State()
    shaxar_state = State()
    manzil_state = State()
    kvadrat_state = State()
    xona_state = State()
    qavat_state = State()
    romlar_state = State()
    eshiklari_state = State()
    gishtlari_state = State()
    isitish_state = State()
    xolati_state = State()
    qoladigan_state = State()
    narx_state = State()
    rasmlari = State()
class Sotadigan2(StatesGroup):
    shaxar_state = State()
    manzil_state = State()
    kvadrat_state = State()
    xona_state = State()
    romlar_state = State()
    eshiklari_state = State()
    gishtlari_state = State()
    isitish_state = State()
    xolati_state = State()
    qoladigan_state = State()
    narx_state = State()
    rasmlari = State()

class Kvartira_Oledgon(StatesGroup):
    shaxar_state = State()
    kvadrat_state = State()
    xona_state = State()
    qavat_state = State()
    isitish_state = State()
    xolati_state = State()


class Hovli_Oledgon(StatesGroup):
    shaxar_state = State()
    kvadrat_state = State()
    xona_state = State()
    isitish_state = State()
    xolati_state = State()