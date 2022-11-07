import shutil
from typing import List

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from pydantic import parse_obj_as

from database import News, User, UserСharacteristic, Cards, UserDeck, Events, Timetable, DanceGroup, UserAddress
from database.engine import get_async_session

from routers.schemas import UserCreateSchema, UserAvatarSchema, UserSchemaOut, \
    СharacteristicSchemaIn, СharacteristicUpdateSchema,\
    CardsSchemaIn, CardsSchemaOut, CardsList,\
    DecksSchema, UserDeckSchema


user_router = APIRouter(prefix='/user')


# @user_router.get('/news', name='Все новости', tags=['Пользователь'])
# async def get_all_news(session: AsyncSession = Depends(get_async_session)):
#     q = select(News.id, News.news_title, News.news_description, User.surename, User.name, User.patronymic).join(News, User.id == News.id_autor)
    
#     news = (await session.execute(q)).all()
#     return news

@user_router.post('/createuser', name='Добавить пользователя', response_model=UserCreateSchema, tags=['Пользователь'])
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):

    u = User()
    d = user.dict()
    for k in d:
        setattr(u, k, d[k])
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return UserCreateSchema.from_orm(u)


@user_router.post('/{user_id}/userimg', name='Загрузить аватар', response_model=UserAvatarSchema, tags=['Пользователь'])
async def change_img(
    user_id: int, 
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(get_async_session)):

    date = datetime.now().strftime("%Y%m%d%H%M%S")

    with open("static/media/"+date+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    avatar = str("static/media/"+date+file.filename)
    

    u = await session.get(User, user_id)
    if u is not None:
        setattr(u, 'avatar', avatar)
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return UserAvatarSchema.from_orm(u)
    raise HTTPException(status_code=404, detail='User not found!')


@user_router.post('/createcharacteristic', name='Создать характеристику пользователя', response_model=СharacteristicSchemaIn, tags=['Пользователь'])
async def create_user(userCharacteristic: СharacteristicSchemaIn, session: AsyncSession = Depends(get_async_session)):

    u = UserСharacteristic()
    d = userCharacteristic.dict()
    for k in d:
        setattr(u, k, d[k])
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return СharacteristicSchemaIn.from_orm(u)


@user_router.put('/{characteriscic_id}/changecharacteristic', name='Изменить характеристику пользователя', response_model=СharacteristicSchemaIn, tags=['Пользователь'])
async def update_characteristic(
    characteriscic_id: int, 
    new_user_data: СharacteristicUpdateSchema, 
    session: AsyncSession = Depends(get_async_session)):
    
    сharact = await session.get(UserСharacteristic, characteriscic_id)
    if сharact is not None:
        data = new_user_data.dict()
        for key in data:
            if data[key] is not None:
                setattr(сharact, key, data[key])
        session.add(сharact)
        await session.commit()
        await session.refresh(сharact)
        return СharacteristicSchemaIn.from_orm(сharact)
    raise HTTPException(status_code=404, detail='Сharacteristic not found!')


@user_router.get('/{user_id}', name='Профиль пользователя', response_model=UserSchemaOut, tags=['Пользователь'])
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user_id, options=[selectinload(User.characterisric)])
    if user is not None:
        return UserSchemaOut.from_orm(user)
    raise HTTPException(status_code=404, detail='User not found!')


@user_router.post('/createnewcard', name='Создать карту', response_model=CardsSchemaIn, tags=['Карты'])
async def create_user(card: CardsSchemaIn, session: AsyncSession = Depends(get_async_session)):

    c = Cards()
    d = card.dict()
    for k in d:
        setattr(c, k, d[k])
    session.add(c)
    await session.commit()
    await session.refresh(c)
    return CardsSchemaIn.from_orm(c)


@user_router.post('/{card_id}/addcardlook', name='Добавить обложку карты', response_model=CardsSchemaOut, tags=['Карты'])
async def create_user(card_id: int, file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):

    with open("static/cards/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    look = str("static/cards/"+file.filename)
    

    c = await session.get(Cards, card_id)
    if c is not None:
        setattr(c, 'card_look', look)
        session.add(c)
        await session.commit()
        await session.refresh(c)
        return CardsSchemaOut.from_orm(c)
    raise HTTPException(status_code=404, detail='Card not found!')


# @user_router.get('/cards', name='Все карты', response_model=CardsList, tags=['Карты'])
# async def get_all_cards(session: AsyncSession = Depends(get_async_session)):
#     query = select(Cards)
#     cards = (await session.execute(query)).scalars().all()
#     if cards is not None:
#         return CardsList(count=len(cards), cards=parse_obj_as(List[CardsSchemaOut], cards))
#     raise HTTPException(status_code=404, detail='Cards not found!')


@user_router.post('/givecard', name='Дать карту пользователю', response_model=DecksSchema, tags=['Карты'])
async def give_card(
    deck:DecksSchema,
    session: AsyncSession = Depends(get_async_session)):

    ud = UserDeck()
    cd = deck.dict()
    for key in cd:
        setattr(ud, key, cd[key])
    session.add(ud)
    await session.commit()
    await session.refresh(ud)
    return DecksSchema.from_orm(ud)

@user_router.get('/{user_id}/userdeck', name='Посмотреть колоду пользователя', tags=['Пользователь'])
async def get_user_deck(user_id: int, session: AsyncSession = Depends(get_async_session)):

   query = select(Cards).join(UserDeck, UserDeck.id_card == Cards.id).where(UserDeck.id_user == user_id)

   result = (await session.execute(query)).scalars().all()
   if not result:
        raise HTTPException(status_code=404, detail='User deck not found!')
   return result



# @user_router.get('/tabletime/{user_id}', name='Расписание пользователя')
# async def get_all_events_by_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
#     q = select(Events.id, Events.event_title, Events.event_description, Events.event_date
#         ).join(Timetable, Events.id == Timetable.id_event
#         ).join(DanceGroup, Timetable.id_group == DanceGroup.id_group
#         ).join(User, DanceGroup.id_user == User.id
#         ).where(User.id == user_id
#         ).where(Events.event_date >= datetime.now()).order_by(Events.event_date)

#     tt = (await session.execute(q)).all()
#     return tt



