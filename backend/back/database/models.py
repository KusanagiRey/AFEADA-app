from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import backref, relationship

from database.base import Base
from database.mixins import TimestampMixin


class UserAddress(TimestampMixin, Base):
    __tablename__ = "address_table"

    street = Column(String(128), nullable=False)
    house_number = Column(String(64), nullable=False)
    flat = Column(Integer)


class UserDCP(Base):
    __tablename__ = "dcp_table"

    amount = Column(Integer)


class UserRole(Base):
    __tablename__ = "role_table"

    role = Column(String(64), index=True, nullable=False)


class UserСharacteristic(Base):
    __tablename__ = "characteristic_table"

    Strength = Column(Integer)
    Agility = Column(Integer)
    Flexibility = Column(Integer)
    Stamina = Column(Integer)
    Stress_resist = Column(Integer)


class User(Base):
    __tablename__ = "user_table"

    login = Column(String(64), index=True, nullable=False)
    password = Column(String(64), index=True, nullable=False)
    surename = Column(String(24), nullable=False)
    name = Column(String(24), nullable=False)
    patronymic = Column(String(24))
    # avatar = Column()
    id_address = Column(Integer, ForeignKey("address_table.id"), nullable=False)
    phone = Column(String(12))
    id_dcp = Column(Integer, ForeignKey("dcp_table.id"))
    id_role = Column(Integer, ForeignKey("role_table.id"))
    id_characteristic = Column(Integer, ForeignKey("characteristic_table.id"))
    # qr_code = Column()

    address = relationship("UserAddress", backref=backref("user", uselist=False))
    dcp = relationship("UserDCP", backref=backref("user", uselist=False))
    role = relationship("UserRole", backref=backref("user", uselist=False))
    characteristic = relationship("UserСharacteristic", backref=backref("user", uselist=False))

    userdeck = relationship("UserDeck")
    affinity = relationship("Affinity")
    group = relationship("Group")
    news = relationship("News")
    events = relationship("Events")
    dancegroupUser = relationship("DanceGroup")


class Cards(Base):
    __tablename__ = "cards_table"

    card_name = Column(String(32), index=True, nullable=False)
    card_discription = Column(String(512), nullable=False)
    # card_look = Column()

    cardsdeck = relationship("UserDeck")


class UserDeck(Base):
    __tablename__ = "deck_table"

    id_card = Column(Integer, ForeignKey("cards_table.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("user_table.id"), nullable=False)


class Affinity(Base):
    __tablename__ = "affinity_table"

    id_relative = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    id_child = Column(Integer, ForeignKey("user_table.id"), nullable=False)


class Group(Base):
    __tablename__ = "group_table"

    name = Column(String(32), nullable=False)
    id_teacher = Column(Integer, ForeignKey("user_table.id"), nullable=False)

    dancegroup = relationship("DanceGroup")
    timetable = relationship("Timetable")


class News(Base):
    __tablename__ = "news_table"

    news_title = Column(String(32), nullable=False)
    news_description = Column(String(512))
    # photo = Column()
    id_autor = Column(Integer, ForeignKey("user_table.id"), nullable=False)


class Events(Base):
    __tablename__ = "events_table"

    event_title = Column(String(32), nullable=False)
    event_description = Column(String(512))
    event_date = Column(DateTime, nullable=False)
    id_autor = Column(Integer, ForeignKey("user_table.id"), nullable=False)

    timetable = relationship("Timetable")


class DanceGroup(Base):
    __tablename__ = "dancegroup_table"

    id_group = Column(Integer, ForeignKey("group_table.id"), nullable=False)
    id_user = Column(Integer, ForeignKey("user_table.id"), nullable=False)


class Timetable(Base):
    __tablename__ = "time_table"

    id_group = Column(Integer, ForeignKey("group_table.id"), nullable=False)
    id_event = Column(Integer, ForeignKey("events_table.id"), nullable=False)