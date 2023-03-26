from typing import Union

from loader import bot


async def check(user_id,channel:Union[int,str]):
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    return member.is_chat_member()