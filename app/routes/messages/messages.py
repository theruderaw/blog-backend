from fastapi import APIRouter
from app.schemas import MessageModel
from app.database import get_db

router = APIRouter(
    prefix='/message',
    tags=['Message']
)

@router.post("/")
def send_message(
    payload : MessageModel
):
    q = """INSERT INTO messages (
        sender_name,
        sender_email,
        message_text,
        receiver_id
    ) VALUES (%s,%s,%s,%s)
    RETURNING *"""
    params = (
        payload.sender_name,
        payload.sender_email,
        payload.message_text,
        str(payload.uuid)
    )

    with get_db() as cursor:
        cursor.execute(q,params)
        return cursor.fetchall()
