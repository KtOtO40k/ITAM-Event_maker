from EventPlaner.DB import create_event, read_user_events, join_user_to_event, read_event_users, user_to_admin, \
    read_admin_or_not, update_user, update_event, delete_admin, leave_event, update_event_image, get_all_events, \
    get_user_info, get_event_image, get_all_users, delete_event, delete_user
from EventPlaner.DB import create_user
from EventPlaner.RandomServise import event_id_make
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import LargeBinary
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
import io
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


origins=[
    'http://localhost:5173',
    '*'
    'http://localhost'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.post("/join")
def Joiner(user_id:int, event_id: str):
    return join_user_to_event(user_id,event_id)


class EventModel(BaseModel):
    name: str
    start: str
    stop: str
    count: int
    tags: str
    descr: str


@app.post("/create_event")
async def EventCreator(event: EventModel):
    id = event_id_make()
    create_event(id, event.name, event.start, event.stop, event.count, event.tags, event.descr)

@app.patch("/update_event_image")
async def UpdateEventImage(event_id:str,image: UploadFile = File(...)):
    image_data = await image.read()
    return update_event_image(event_id,image_data)


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
@app.patch("/update_user")
def UpdateUser(user_id:int,updates: dict):
    return update_user(user_id,updates)
@app.patch("/update_event")
def UpdateEvent(event_id:str,updates: dict):
    return update_event(event_id,updates)
@app.delete("/delete_admin")
def DeleteAdmin(user_id:int):
    delete_admin(user_id)
@app.delete("/leave_event")
def LeaveEvent(user_id: int,event_id: str):
    return (leave_event(user_id, event_id))
@app.get("/get_all_events")
def ReadEventUsers():
    return get_all_events()

@app.get("/get_user_info")
def GetUserInfo(user_id: int):
    return get_user_info(user_id)
@app.get("/get_event_image")
def get_event_image_endpoint(event_id: str):
    image_data = get_event_image(event_id)
    return StreamingResponse(io.BytesIO(image_data), media_type="image/png")
@app.get("/get_all_users")
def ReadEventUsers():
    return get_all_users()
@app.delete("/delete_event")
def DeleteEvent(event_id: str):
    delete_event(event_id)
@app.delete("/delete_user")
def DeleteUser(user_id: int):
    delete_user(user_id)
uvicorn.run(app)
