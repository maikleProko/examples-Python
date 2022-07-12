from typing import Optional, List, Dict, Any
import json
from pymongo import MongoClient, ASCENDING
from db.classes import User, DuckieBot, DuckieBotSession, TGUser
from db.session_utils import convert_tz_and_sort_sessions

import jwt
import random

MAX_LIMIT = 256
MONGO_CLIENT = None
HOST: str = 'localhost'
PORT: int = 27017
USER: str = 'users'
DUCKIEBOT: str = 'duckiebots'
BOT_SESSION: str = "duckiebot_sessions"
NAME: str = "name"
OWNER: str = "owner"
HOSTNAME: str = "hostname"
TG_USERS: str = "tg_users"
TG_NAME: str = "tg_github_name"
TG_CHAT_ID: str = "tg_chat_id"
TOKEN: str = "user_jwt"
ID: str = "id"
START_TIME: str = "start_time"
END_TIME: str = "end_time"


def get_db_name():
    return 'lab-duckietown'


def get_db_object():
    return get_client_object()[get_db_name()]


def get_client_object():
    global MONGO_CLIENT
    if MONGO_CLIENT is None:
        MONGO_CLIENT = MongoClient(HOST, PORT)
    return MONGO_CLIENT


def close_connection():
    if MONGO_CLIENT is not None:
        MONGO_CLIENT.close()


def load_db_from_json(file_name: str = "data.json") -> None:
    with open(file_name, 'r') as fp:
        f = json.load(fp)
    users = f["users"]
    duckiebots = f["duckiebots"]
    for user in users:
        for key in user.keys():
            add_user(User(name=key, role=user[key], user_jwt=""))
    for duckiebotname in duckiebots:
        add_duckiebot(DuckieBot(duckiebotname))


def prepare_for_first_start() -> None:
    get_client_object().drop_database(get_db_name())
    load_db_from_json()


# USER PART

def add_user(user: User, db=get_db_object()) -> Optional[dict]:
    if not get_user(user):
        db[USER].insert_one(user.dict())
        return user.dict()


def del_user(user: User, db=get_db_object()):
    db[USER].delete_one(user.dict())


def get_user(user: User, db=get_db_object()) -> Optional[User]:
    db_user = db[USER].find_one({NAME: user.name})
    if db_user:
        return User(name=db_user["name"], role=db_user["role"], user_jwt=db_user["user_jwt"])


def create_jwt(user: User) -> str:
    # generate secret code
    secret = ""
    for _ in range(10):
        random_integer = random.randint(0, MAX_LIMIT)
        secret += chr(random_integer)
    # generate jwt
    user_jwt = jwt.encode({"name": user.name, "role": user.role}, secret, algorithm="HS256")
    if not isinstance(user_jwt, str):
        user_jwt = user_jwt.decode('ascii')
    return user_jwt


def get_jwt_and_store_it_in_db(user: User, db=get_db_object()) -> str:
    user = get_user(user)
    user_jwt = create_jwt(user)
    # store jwt in db
    db_filter = {'name': user.name}
    new_values = {"$set": {"name": user.name, "role": user.role, "user_jwt": user_jwt}}
    db[USER].update_one(db_filter, new_values)
    return user_jwt


def delete_jwt_for_user(user: User, db=get_db_object()):
    # delete jwt
    user = get_user(user)
    db_filter = {'name': user.name}
    new_values = {"$set": {"name": user.name, "role": user.role, "user_jwt": ""}}
    db[USER].update_one(db_filter, new_values)


def get_list_of_users(db=get_db_object()) -> List[dict]:
    users: List[dict] = []
    for user in db[USER].find({}).sort('role', ASCENDING):
        del user["_id"]
        users.append(user)
    return users


# DUCKIEBOT PART


def get_duckiebot(bot: DuckieBot, db=get_db_object()) -> Optional[DuckieBot]:
    bot = db[DUCKIEBOT].find_one({HOSTNAME: bot.hostname})
    if bot:
        return DuckieBot(hostname=bot["hostname"])


def get_duckiebots(db=get_db_object()) -> list:
    duckiebots: List[dict] = []
    for duck in db[DUCKIEBOT].find({}).sort('hostname', ASCENDING):
        del duck["_id"]
        duckiebots.append(duck)
    return duckiebots


def add_duckiebot(bot: DuckieBot, db=get_db_object()) -> Optional[dict]:
    if not get_duckiebot(bot):
        db[DUCKIEBOT].insert_one(bot.dict())
        return bot.dict()


def update_duckiebot_from_id(bot: DuckieBot, hostname, db=get_db_object()):
    duckiebot = get_duckiebot(bot)
    db[DUCKIEBOT].update_one({HOSTNAME: duckiebot.hostname}, {"$set": {HOSTNAME: hostname}})
    db[BOT_SESSION].update_one({HOSTNAME: duckiebot.hostname}, {"$set": {HOSTNAME: hostname}})


def del_duckiebot(bot: DuckieBot, db=get_db_object()):
    duckiebot = get_duckiebot(bot)
    if duckiebot:
        db[DUCKIEBOT].delete_one(duckiebot.dict())

# SESSION PART


def get_session(session: Dict[str, Any], db=get_db_object()) -> Optional[DuckieBotSession]:
    try:
        session = db[BOT_SESSION].find_one({ID: session.id})
    except AttributeError:
        session = db[BOT_SESSION].find_one({ID: session["id"]})
    if session:
        return DuckieBotSession(id=session['id'], owner=session["owner"], hostname=session["hostname"],
                                start_time=session["start_time"], end_time=session["end_time"])


def get_sessions_from_name(name: str, db=get_db_object()) -> list:
    sessions: List[dict] = db[BOT_SESSION].find({OWNER: name})
    sort_sessions = []
    for session in sessions:
        del session["_id"]
        sort_sessions.append(session)
    return sort_sessions


def get_session_from_id(session_id: int, db=get_db_object()) -> Dict[str, Any]:
    session = db[BOT_SESSION].find_one({ID: session_id})
    if session:
        del session["_id"]
    return session


def get_sessions(tzoffset: int, db=get_db_object()) -> list:
    duckiebot_sessions: List[dict] = []
    for session in db[BOT_SESSION].find({}).sort('owner', ASCENDING):
        del session["_id"]
        duckiebot_sessions.append(session)
    duckiebot_sessions = convert_tz_and_sort_sessions(duckiebot_sessions, tzoffset)
    return duckiebot_sessions


def add_session(session: DuckieBotSession, db=get_db_object()) -> Optional[dict]:
    if not get_session(session.dict()):
        db[BOT_SESSION].insert_one(session.dict())
        return session.dict()


def del_session(session: Dict[str, Any], db=get_db_object()) -> None:
    duck_session = get_session(session)
    if duck_session:
        db[BOT_SESSION].delete_one(duck_session.dict())


def get_next_id() -> int:
    max_id = 0
    duckiebot_sessions = get_sessions(0)
    if len(duckiebot_sessions) == 0:
        return 1
    else:
        for session in duckiebot_sessions:
            if session['id'] >= max_id:
                max_id = session['id'] + 1
    return max_id


def update_session_from_id(session_id: int, owner: str, hostname: str,
            start_time: Dict[str, Any], end_time: Dict[str, Any], db=get_db_object()) -> None:
    db_filter = {'id': session_id}
    new_values = {"$set": {'owner': owner, "hostname": hostname, "start_time": start_time, "end_time": end_time}}
    db[BOT_SESSION].update_one(db_filter, new_values)


def check_jwt(user_jwt: str, db=get_db_object()) -> bool:
    try:
        user = db[USER].find_one({TOKEN: user_jwt})
        if user:
            return True
        return False
    except TypeError:
        return False


def get_user_data_from_JWT(user_jwt: str, db=get_db_object()) -> Dict[str, Any]:
    exist = check_jwt(user_jwt)
    if exist:
        user = db[USER].find_one({TOKEN: user_jwt})
        if user:
            del user["_id"]
        return user
    else:
        return None

# ARS BOT PART


def tg_add_user(user: Dict[str, Any], db=get_db_object()) -> None:
    if not tg_get_user_from_chat_id(user["tg_chat_id"]):
        db[TG_USERS].insert_one(TGUser(user['tg_chat_id'], user['tg_github_name']).dict())
    else:
        filter = {"tg_chat_id": user["tg_chat_id"]}
        new_value = {"$set": {"tg_chat_id": user["tg_chat_id"],
                              "tg_github_name": user["tg_github_name"]}}
        db[TG_USERS].update_one(filter, new_value)


def tg_get_user_from_chat_id(chat_id: int, db=get_db_object()) -> Dict[str, Any]:
    db_user = db[TG_USERS].find_one({'tg_chat_id': chat_id})
    if db_user:
        return db_user
    return None


def tg_delete_user(chat_id: int, db=get_db_object()) -> None:
    db_user = tg_get_user_from_chat_id(chat_id)
    if db_user:
        db[TG_USERS].delete_one(db_user)


if __name__ == "__main__":
    get_db_object()
