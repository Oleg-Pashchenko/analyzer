import dataclasses
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import warnings
from sqlalchemy.exc import SADeprecationWarning
import dotenv
import os

dotenv.load_dotenv()


def as_dict(obj):
    data = obj.__dict__
    if "_sa_instance_state" in data:
        data.pop("_sa_instance_state")
    return data


warnings.filterwarnings("ignore", category=SADeprecationWarning)


@dataclasses.dataclass
class Messages:
    id: int
    message_id: int
    lead_id: int
    text: str
    is_bot: bool
    is_q: bool


@dataclasses.dataclass
class Threads:
    id: int
    lead_id: int
    thread_id: str


dotenv.load_dotenv()
engine = sqlalchemy.create_engine(
    f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}'
    f'@{os.getenv("DB_HOST")}:5432/{os.getenv("AMO_BOT_DB_NAME")}',
    pool_pre_ping=True,
)
Session = sessionmaker(bind=engine)
session = Session()

Base = automap_base()
Base.prepare(engine, reflect=True)
MessagesEntity = Base.classes.messages
ThreadsEntity = Base.classes.threads

for c in [MessagesEntity, ThreadsEntity]:
    c.as_dict = as_dict


def get_messages_history(lead_id: int):
    message_objects = (
        session.query(MessagesEntity).filter(MessagesEntity.lead_id == lead_id).all()
    )
    message_objects = sorted(message_objects, key=lambda x: x.id)
    messages = []
    for message_obj in message_objects:
        if message_obj.is_q:
            continue
        if message_obj.is_bot:
            messages.append({"role": "assistant", "content": message_obj.text})
        else:
            messages.append({"role": "user", "content": message_obj.text})
    return messages
