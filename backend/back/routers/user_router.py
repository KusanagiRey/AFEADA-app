import shutil

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import News, User, Cards, UserDeck, Events, Timetable, DanceGroup 
from database.engine import get_async_session

from passlib.context import CryptContext
from jose import jwt

from routers.schemas import UserAvatarSchema, UserSchemaOut, SignUpUserSchema


user_router = APIRouter(prefix='/user')


SECRET_KEY = '602e4618337c03a842253a53466661f4ac2fd618e47bd69691c9ab9291b1b329'
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, role: int, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "role": role})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    to_decode = jwt.decode(token, SECRET_KEY)
    return to_decode


def check_admin(token: str = Depends(oauth2_scheme)):
    claims = decode_token(token)
    check = claims.get("role")
    if check["role"] != 1:
        raise HTTPException(status_code=401, detail="Access only for admins!")
    return claims


@user_router.post('/sign_up', name='Регистрация', tags=['Регистрация / Вход'])
async def sign_up(new_user: SignUpUserSchema, session: AsyncSession = Depends(get_async_session)):
    u = User()
    d = new_user.dict()
    for k in d:
        setattr(u, k, d[k])
    setattr(u, 'password', get_password_hash(new_user.password))
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return {"message": "Новый пользователь зарегистрирован!"}


@user_router.post('/token', name='Вход', tags=['Регистрация / Вход'])
async def login(from_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    query = select(User.password, User.role).where(User.login == from_data.username)
    result = (await session.execute(query)).fetchone()
    if result is None:
        raise HTTPException(status_code=400, detail="Incorrect login or password!")
    password_check = pwd_context.verify(from_data.password, result[0])
    if password_check:
        access_token = create_access_token(
            data={"sub":from_data.username}, role={"role":result[1]}, expires_delta=timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type":"bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect login or password!")


@user_router.post('/{user_id}/userimg', name='Загрузить аватар', response_model=UserAvatarSchema, tags=['Пользователь'])
async def change_img(
    user_id: int, 
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(get_async_session), 
    token: str = Depends(oauth2_scheme)):

    date = datetime.now().strftime("%Y%m%d%H%M%S")

    with open("static/media/avatars/"+date+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    avatar = str("static/media/avatars/"+date+file.filename)
    

    u = await session.get(User, user_id)
    if u is not None:
        setattr(u, 'avatar', avatar)
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return UserAvatarSchema.from_orm(u)
    raise HTTPException(status_code=404, detail='User not found!')


@user_router.get('/{user_id}', name='Профиль пользователя', response_model=UserSchemaOut, tags=['Пользователь'])
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_scheme)):
    user = await session.get(User, user_id, options=[selectinload(User.characterisric)])
    if user is not None:
        return UserSchemaOut.from_orm(user)
    raise HTTPException(status_code=404, detail='User not found!')


@user_router.get('/{user_id}/userdeck', name='Посмотреть колоду пользователя', tags=['Пользователь'])
async def get_user_deck(user_id: int, session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_scheme)):

   query = select(Cards).join(UserDeck, UserDeck.id_card == Cards.id).where(UserDeck.id_user == user_id)

   result = (await session.execute(query)).scalars().all()
   if not result:
        raise HTTPException(status_code=404, detail='User deck not found!')
   return result


@user_router.get('/news/get', name='Все новости', tags=['Новостная лента'])
async def get_all_news(session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_scheme)):
    q = select(News.id, News.news_title, News.news_description, News.photo, User.surename, User.name, User.patronymic)\
        .join(News, User.id == News.id_autor)
    
    news = (await session.execute(q)).all()
    return news


@user_router.get('/tabletime/{user_id}', name='Расписание пользователя', tags=['Расписание'])
async def get_all_events_by_user(user_id: int, session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2_scheme)):
    q = select(Events.id, Events.event_title, Events.event_description, Events.event_date
        ).join(Timetable, Events.id == Timetable.id_event
        ).join(DanceGroup, Timetable.id_group == DanceGroup.id_group
        ).join(User, DanceGroup.id_user == User.id
        ).where(User.id == user_id
        ).where(Events.event_date >= datetime.now()).order_by(Events.event_date)

    tt = (await session.execute(q)).all()
    return tt