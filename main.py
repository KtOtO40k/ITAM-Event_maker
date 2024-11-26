from EventPlaner.DB import create_event, read_user_events, join_user_to_event, read_event_users, user_to_admin, \
    read_admin_or_not
from EventPlaner.DB import create_user
from EventPlaner.RandomServise import event_id_make
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi import HTTPException
app = FastAPI()

@app.post("/join")
def Joiner(user_id:int, event_id: str):
    join_user_to_event(user_id,event_id)
    #raise HTTPException(status_code=200)

class EventModel(BaseModel):
    name: str
    start: str
    stop: str
    count: str
    tags: str
@app.post("/create_event")
def EventCreator(event: EventModel):
    id = event_id_make()
    create_event(id,event.name,event.start,event.stop,event.count,event.tags)

class UserModel(BaseModel):
    name: str
    second_name: str
    surname: str
    number_group: str
    age: str
@app.post("/create_user")
def EventCreator(user: UserModel):
    create_user(user.name,user.second_name,user.surname,user.number_group,user.age)
@app.get("/read_user_events")
def ReadUserEvents(user_id: int):
    return read_user_events(user_id)
@app.get("/read_event_users")
def ReadEventUsers(event_id: str):
    return read_event_users(event_id)
@app.post("/user_to_admin")
def UserToAdmin(user_id: int):
    user_to_admin(user_id)
@app.get("/read_admin_or_not")
def ReadAdminOrNot(user_id: int):
    return read_admin_or_not(user_id)
    





uvicorn.run(app)