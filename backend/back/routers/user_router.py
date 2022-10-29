from datetime import datetime

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import News, User, Events, Timetable, DanceGroup, UserAddress, UserDCP, UserСharacteristic
from database.engine import get_async_session


user_router = APIRouter(prefix='/user', tags=['Пользователь'])


@user_router.get('/news', name='Все новости')
async def get_all_news(session: AsyncSession = Depends(get_async_session)):
    q = select(News.id, News.news_title, News.news_description, User.surename, User.name, User.patronymic).join(News, User.id == News.id_autor)
    
    news = (await session.execute(q)).all()
    return news


@user_router.get('/tabletime/{user_id}', name='Расписание пользователя')
async def get_all_events_by_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    q = select(Events.id, Events.event_title, Events.event_description, Events.event_date
        ).join(Timetable, Events.id == Timetable.id_event
        ).join(DanceGroup, Timetable.id_group == DanceGroup.id_group
        ).join(User, DanceGroup.id_user == User.id
        ).where(User.id == user_id
        ).where(Events.event_date >= datetime.now()).order_by(Events.event_date)

    tt = (await session.execute(q)).all()
    return tt


@user_router.get('/{user_id}', name='Профиль пользователя')
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_async_session)):
    q = select(User.surename, User.name, User.patronymic, 
        UserAddress.street, UserAddress.house_number, UserAddress.flat,
        UserDCP.amount, 
        UserСharacteristic.Strength, UserСharacteristic.Agility,
        UserСharacteristic.Flexibility, UserСharacteristic.Stamina, 
        UserСharacteristic.Stress_resist
        ).join(UserAddress, User.id_address == UserAddress.id
        ).join(UserDCP, User.id_dcp == UserDCP.id
        ).join(UserСharacteristic, User.id_characteristic == UserСharacteristic.id
        ).where(User.id == user_id)

    profile = (await session.execute(q)).all()
    return profile
