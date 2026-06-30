from fastapi import APIRouter, Query
from uuid import UUID
from app.database import get_db

router = APIRouter(
    prefix="/gen",
    tags=["Utils"]
)

@router.get("/slug")
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
        cursor.execute(q,[slug])
        return cursor.fetchone()

@router.get("/username")
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
        return cursor.fetchone()
    
@router.get("/users")
def get_user_list():
    q = """
        SELECT id as uuid,username
        FROM profiles
"""
    with get_db() as cursor:
        cursor.execute(q)
        return cursor.fetchall()