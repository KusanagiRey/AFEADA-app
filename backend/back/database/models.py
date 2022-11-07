import enum

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from database.base import Base
from database.mixins import TimestampMixin


class UserRole(enum.IntEnum):

    teacher = 1
    student = 2


class User(TimestampMixin, Base):
    __tablename__ = "user_table"

    login = Column(String(64), index=True, nullable=False)
    password = Column(String(64), index=True, nullable=False)
    surename = Column(String(24), nullable=False)
    name = Column(String(24), nullable=False)
    patronymic = Column(String(24))
    avatar = Column(URLType)
    phone = Column(String(12))
    dcp = Column(Integer)
    role = Column(Enum(UserRole))
    qr_code = Column(URLType)
    
    address = relationship("UserAddress", back_populates="owner", uselist=False)
    characterisric = relationship("UserСharacteristic", back_populates="owner", uselist=False)
    userdeck = relationship("UserDeck", back_populates="owner")
    group = relationship("Group", back_populates="owner")
    dancegroupUser = relationship("DanceGroup", back_populates="owner")
    news = relationship("News", back_populates="owner")
    events = relationship("Events", back_populates="owner")

    # affinity = relationship("Affinity")
    
    
class UserAddress(TimestampMixin, Base):
    __tablename__ = "address_table"

    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    street = Column(String(128), nullable=False)
    house_number = Column(String(64), nullable=False)
    flat = Column(Integer)

    owner = relationship("User", back_populates="address")


class UserСharacteristic(TimestampMixin, Base):
    __tablename__ = "characteristic_table"

    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    Strength = Column(Integer)
    Agility = Column(Integer)
    Flexibility = Column(Integer)
    Stamina = Column(Integer)
    Stress_resist = Column(Integer)

    owner = relationship("User", back_populates="characterisric")


class Cards(Base):
    __tablename__ = "cards_table"

    card_name = Column(String(32), index=True, nullable=False)
    card_discription = Column(String(512), nullable=False)
    card_look = Column(URLType)

    cardsdeck = relationship("UserDeck", back_populates="card")


class UserDeck(Base):
    __tablename__ = "deck_table"

    id_card = Column(Integer, ForeignKey("cards_table.id"))
    id_user = Column(Integer, ForeignKey("user_table.id"))

    owner = relationship("User", back_populates="userdeck")
    card = relationship("Cards", back_populates="cardsdeck")


# class Affinity(Base):
#     __tablename__ = "affinity_table"

#     id_relative = Column(Integer, ForeignKey("user_table.id"), nullable=False)
#     id_child = Column(Integer, ForeignKey("user_table.id"), nullable=False)


class Group(Base):
    __tablename__ = "group_table"

    name = Column(String(32), nullable=False)
    id_teacher = Column(Integer, ForeignKey("user_table.id"))

    owner = relationship("User", back_populates="group")
    dancegroup = relationship("DanceGroup", back_populates="group")
    timetable = relationship("Timetable", back_populates="group")


class DanceGroup(Base):
    __tablename__ = "dancegroup_table"

    id_group = Column(Integer, ForeignKey("group_table.id"))
    id_user = Column(Integer, ForeignKey("user_table.id"))

    owner = relationship("User", back_populates="dancegroupUser")
    group = relationship("Group", back_populates="dancegroup")


class News(Base):
    __tablename__ = "news_table"

    news_title = Column(String(32), nullable=False)
    news_description = Column(String(512))
    photo = Column(URLType)
    id_autor = Column(Integer, ForeignKey("user_table.id"))

    owner = relationship("User", back_populates="news")


class Events(Base):
    __tablename__ = "events_table"

    event_title = Column(String(32), nullable=False)
    event_description = Column(String(512))
    event_date = Column(DateTime, nullable=False)
    id_autor = Column(Integer, ForeignKey("user_table.id"))

    owner = relationship("User", back_populates="events")
    timetable = relationship("Timetable", back_populates="event")


class Timetable(Base):
    __tablename__ = "time_table"

    id_group = Column(Integer, ForeignKey("group_table.id"))
    id_event = Column(Integer, ForeignKey("events_table.id"))

    group = relationship("Group", back_populates="timetable")
    event = relationship("Events", back_populates="timetable")