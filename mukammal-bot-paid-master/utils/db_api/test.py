import asyncio
from nod import Database

async def test():
    db = Database()
    await db.create()

    baza_uylar = await db.select_uy(shaxar_ber=f"Toshkent",xona_ber=3)
    print(f"soralgan: {baza_uylar[3]}")
    print("#######")

asyncio.run(test())