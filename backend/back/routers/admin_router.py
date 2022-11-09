import shutil
from typing import List

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete

from pydantic import parse_obj_as

from database import News, User, UserСharacteristic, Cards, UserDeck, Group, Events, Timetable, DanceGroup
from database.engine import get_async_session

from routers.schemas import UserCreateSchema,\
    СharacteristicSchemaIn, СharacteristicUpdateSchema,\
    CardsSchemaIn, CardsSchemaOut, CardsList, DecksSchema, \
    NewsSchemaIn, NewsAvatarSchema, GroupSchemaIn, GroupSchemaOut, \
    DanceGroupSchemaIn, EventsSchemaIn, TimetableSchemaIn


admin_router = APIRouter(prefix='/admin')


@admin_router.post('/createuser', name='Добавить пользователя', response_model=UserCreateSchema, tags=['Пользователь'])
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):

    u = User()
    d = user.dict()
    for k in d:
        setattr(u, k, d[k])
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return UserCreateSchema.from_orm(u)


@admin_router.post('/createcharacteristic', name='Создать характеристику пользователя', response_model=СharacteristicSchemaIn, tags=['Пользователь'])
async def create_user(userCharacteristic: СharacteristicSchemaIn, session: AsyncSession = Depends(get_async_session)):

    u = UserСharacteristic()
    d = userCharacteristic.dict()
    for k in d:
        setattr(u, k, d[k])
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return СharacteristicSchemaIn.from_orm(u)


@admin_router.put('/{characteriscic_id}/changecharacteristic', name='Изменить характеристику пользователя', response_model=СharacteristicSchemaIn, tags=['Пользователь'])
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


@admin_router.post('/createnewcard', name='Создать карту', response_model=CardsSchemaIn, tags=['Карты'])
async def create_user(card: CardsSchemaIn, session: AsyncSession = Depends(get_async_session)):

    c = Cards()
    d = card.dict()
    for k in d:
        setattr(c, k, d[k])
    session.add(c)
    await session.commit()
    await session.refresh(c)
    return CardsSchemaIn.from_orm(c)


@admin_router.post('/{card_id}/addcardlook', name='Добавить обложку карты', response_model=CardsSchemaOut, tags=['Карты'])
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


@admin_router.get('/cards/get', name='Все карты', response_model=CardsList, tags=['Карты'])
async def get_all_cards(session: AsyncSession = Depends(get_async_session)):
    query = select(Cards)
    cards = (await session.execute(query)).scalars().all()
    if cards is not None:
        return CardsList(count=len(cards), cards=parse_obj_as(List[CardsSchemaOut], cards))
    raise HTTPException(status_code=404, detail='Cards not found!')


@admin_router.post('/givecard', name='Дать карту пользователю', response_model=DecksSchema, tags=['Карты'])
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


@admin_router.post('/news/add/{user_id}', name='Создать новость', response_model=NewsSchemaIn, tags=['Новостная лента'])
async def add_news(user_id: int, news: NewsSchemaIn, session: AsyncSession = Depends(get_async_session)):

    n = News()
    d = news.dict()
    for k in d:
        setattr(n, k, d[k])
    setattr(n, 'id_autor', user_id)
    session.add(n)
    await session.commit()
    await session.refresh(n)
    return NewsSchemaIn.from_orm(n)


@admin_router.post('/add/newsimage/{news_id}', name='Загрузить картинку', response_model=NewsAvatarSchema, tags=['Новостная лента'])
async def change_img(
    news_id: int, 
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(get_async_session)):

    date = datetime.now().strftime("%Y%m%d%H%M%S")

    with open("static/media/news/"+date+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    photo = str("static/media/news/"+date+file.filename)

    n = await session.get(News, news_id)
    if n is not None:
        setattr(n, 'photo', photo)
        session.add(n)
        await session.commit()
        await session.refresh(n)
        return NewsAvatarSchema.from_orm(n)
    raise HTTPException(status_code=404, detail='News not found!')


@admin_router.delete('/news/delete/{news_id}', name='Удалить новость', response_class=Response, tags=['Новостная лента'])
async def delete_user(news_id: int, session: AsyncSession = Depends(get_async_session)):
    q = delete(News).where(News.id == news_id)
    await session.execute(q)
    return Response(status_code=204)


@admin_router.post('/groups/add/{user_id}', name='Создать группу', response_model=GroupSchemaIn, tags=['Танцевальные группы'])
async def add_group(user_id: int, group: GroupSchemaIn, session: AsyncSession = Depends(get_async_session)):

    g = Group()
    d = group.dict()
    for k in d:
        setattr(g, k, d[k])
    setattr(g, 'id_teacher', user_id)
    session.add(g)
    await session.commit()
    await session.refresh(g)
    return GroupSchemaIn.from_orm(g)


@admin_router.get('/groups/all', name='Показать все группы', response_model=List[GroupSchemaOut], tags=['Танцевальные группы'])
async def show_all_groups(session: AsyncSession = Depends(get_async_session)):
    groups = select(Group).options(selectinload(Group.owner))
    result = (await session.execute(groups)).scalars().all()
    if result is not None:
        return [GroupSchemaOut(id=g.id, name=g.name, owner=g.owner) for g in result]
    raise HTTPException(status_code=404, detail='Group not found!')


@admin_router.post('/dancegroup/add', name='Добавить пользователя в группу', response_model=DanceGroupSchemaIn, tags=['Танцевальные группы'])
async def add_group(dancegroup: DanceGroupSchemaIn, session: AsyncSession = Depends(get_async_session)):

    g = DanceGroup()
    d = dancegroup.dict()
    for k in d:
        setattr(g, k, d[k])
    session.add(g)
    await session.commit()
    await session.refresh(g)
    return DanceGroupSchemaIn.from_orm(g)


@admin_router.post('/event/add/{autor_id}', name='Создать мероприятие', response_model=EventsSchemaIn, tags=['Расписание'])
async def add_event(event: EventsSchemaIn, autor_id: int, session: AsyncSession = Depends(get_async_session)):
   
    e = Events()
    d = event.dict()
    for k in d:
        setattr(e, k, d[k])
    setattr(e, 'id_autor', autor_id)
    session.add(e)
    await session.commit()
    await session.refresh(e)
    return EventsSchemaIn.from_orm(e)


@admin_router.post('/timetable/add', name='Добавить группу к мероприятию', response_model=TimetableSchemaIn, tags=['Расписание'])
async def add_timetable(timetable: TimetableSchemaIn, session: AsyncSession = Depends(get_async_session)):

    tt = Timetable()
    d = timetable.dict()
    for k in d:
        setattr(tt, k, d[k])
    session.add(tt)
    await session.commit()
    await session.refresh(tt)
    return TimetableSchemaIn.from_orm(tt)