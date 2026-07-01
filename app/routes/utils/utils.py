from fastapi import APIRouter, Query
from uuid import UUID
from app.database import get_db
# Import your response structures
from app.schemas import StandardResponse, ResponseMeta

router = APIRouter(
    prefix="/gen",
    tags=["Utils"]
)

@router.get("/slug", response_model=StandardResponse)
def check_slug(
    slug : str = Query(...)
):
    q = """
        SELECT EXISTS(
            SELECT 1
            FROM articles
            WHERE slug = %s
        )
        """

    with get_db() as cursor:
        cursor.execute(q, [slug])
        exists_result = cursor.fetchone()['exists']
        
        return StandardResponse(
            meta=ResponseMeta(message="Found" if exists_result else "Not Found"),
            data=exists_result
        )

@router.get("/username", response_model=StandardResponse)
def get_username(
    user_id: UUID = Query(...)
):
    q = """
        SELECT username
        FROM profiles
        WHERE id = %s
    """

    with get_db() as cursor:
        cursor.execute(q, (str(user_id),))
        username_result = cursor.fetchone()
        
        return StandardResponse(
            meta=ResponseMeta(message="Username retrieved successfully"),
            data=username_result
        )
    
@router.get("/users", response_model=StandardResponse)
def get_user_list():
    q = """
        SELECT id as uuid, username
        FROM profiles
    """
    with get_db() as cursor:
        cursor.execute(q)
        users = cursor.fetchall()
        
        return StandardResponse(
            meta=ResponseMeta(
                message="User list retrieved successfully",
                count=len(users)
            ),
            data=users
        )