import shutil

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import News, User, Cards, UserDeck, Events, Timetable, DanceGroup 
from database.engine import get_async_session

from routers.schemas import UserAvatarSchema, UserSchemaOut


user_router = APIRouter(prefix='/user')


@user_router.post('/{user_id}/userimg', name='Загрузить аватар', response_model=UserAvatarSchema, tags=['Пользователь'])
async def change_img(
    user_id: int, 
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(get_async_session)):

    date = datetime.now().strftime("%Y%m%d%H%M%S")

    with open("static/media/avatar/"+date+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    avatar = str("static/media/avatar/"+date+file.filename)
    

    u = await session.get(User, user_id)
    if u is not None:
        setattr(u, 'avatar', avatar)
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return UserAvatarSchema.from_orm(u)
    raise HTTPException(status_code=404, detail='User not found!')


@user_router.get('/{user_id}', name='Профиль пользователя', response_model=UserSchemaOut, tags=['Пользователь'])
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user_id, options=[selectinload(User.characterisric)])
    if user is not None:
        return UserSchemaOut.from_orm(user)
    raise HTTPException(status_code=404, detail='User not found!')


@user_router.get('/{user_id}/userdeck', name='Посмотреть колоду пользователя', tags=['Пользователь'])
async def get_user_deck(user_id: int, session: AsyncSession = Depends(get_async_session)):

   query = select(Cards).join(UserDeck, UserDeck.id_card == Cards.id).where(UserDeck.id_user == user_id)

   result = (await session.execute(query)).scalars().all()
   if not result:
        raise HTTPException(status_code=404, detail='User deck not found!')
   return result


@user_router.get('/news/get', name='Все новости', tags=['Новостная лента'])
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    q = select(News.id, News.news_title, News.news_description, News.photo, User.surename, User.name, User.patronymic)\
        .join(News, User.id == News.id_autor)
    
    news = (await session.execute(q)).all()
    return news


@user_router.get('/tabletime/{user_id}', name='Расписание пользователя', tags=['Расписание'])
async def get_all_events_by_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    q = select(Events.id, Events.event_title, Events.event_description, Events.event_date
        ).join(Timetable, Events.id == Timetable.id_event
        ).join(DanceGroup, Timetable.id_group == DanceGroup.id_group
        ).join(User, DanceGroup.id_user == User.id
        ).where(User.id == user_id
        ).where(Events.event_date >= datetime.now()).order_by(Events.event_date)

    tt = (await session.execute(q)).all()
    return tt