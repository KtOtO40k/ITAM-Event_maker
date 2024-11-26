from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from contextlib import contextmanager
from EventPlaner.RandomServise import event_id_make
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

# таблица для связи
user_event_association = Table(
    'user_event_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', String, ForeignKey('events.id'), primary_key=True)
)

# модель для мероприятий
class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    start = Column(String, nullable=True)
    stop = Column(String, nullable=True)
    count = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    users = relationship('Users', secondary=user_event_association, back_populates='events')

# модель для пользователей
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    number_group = Column(String, nullable=True)
    age = Column(String, nullable=True)
    events = relationship('Event', secondary=user_event_association, back_populates='users')


engine = create_engine(
    'sqlite:///C:/Users/co730/PycharmProjects/EventPlanerITAM/.venv/EventPlaner/database.db'
)
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()

# функция для создания мероприятия
def create_event(id,name, start, stop, count, tags):
    with get_session() as session:
        new_event = Event(
            id=id,
            name=name,
            start=start,
            stop=stop,
            count=count,
            tags=tags
        )
        session.add(new_event)

# функция для создания пользователя
def create_user(name, second_name, surname, number_group, age):
    with get_session() as session:
        new_user = Users(
            name=name,
            second_name=second_name,
            surname=surname,
            number_group=number_group,
            age=age
        )
        session.add(new_user)

# получение всех мероприятий, на которые записан пользователь
def read_user_events(user_id):
    with get_session() as session:
        user = session.query(Users).filter(Users.id == user_id).first()
        if not user:
            return f"Пользователь с ID {user_id} не найден."
        return [event.name for event in user.events]

# получение всех пользователей, записанных на мероприятие
def read_event_users(event_id):
    with get_session() as session:
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return f"Мероприятие с ID {event_id} не найдено."
        return [f"{user.name} {user.surname}" for user in event.users]

# присоединение пользователя к мероприятию
def join_user_to_event(user_id, event_id):
    with get_session() as session:
        user = session.query(Users).filter(Users.id == user_id).first()
        event = session.query(Event).filter(Event.id == event_id).first()
        if not user:
            return f"Пользователь с ID {user_id} не найден."
        if not event:
            return f"Мероприятие с ID {event_id} не найдено."
        event.users.append(user)

#Event.__table__.drop(engine)
#Users.__table__.drop(engine)