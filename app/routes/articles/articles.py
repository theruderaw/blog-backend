from fastapi import APIRouter, Query, HTTPException
from app.database import get_db
from app.schemas import CreateArticle, EditArticle
import json

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)


@router.get("/")
def read_articles(
    page_no: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    q = """
        SELECT
            a.id,
            a.title,
            a.slug,
            a.body,
            a.status,
            a.author_id,
            a.created_at,
            p.username as posted_by
        FROM articles a
        JOIN profiles p 
            ON p.id = a.author_id 
        WHERE
            a.status = 'published'
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """

    params = (
        page_size,
        (page_no - 1) * page_size
    )

    with get_db() as cursor:
        cursor.execute(q, params)
        return cursor.fetchall()

@router.get("/user")
def read_article_by_user(
    page_no: int = Query(default=1, ge=1),
    page_size: int = Query(default=8, ge=1, le=100),
    author_id: str = Query(...)
):
    q = """
        SELECT
            a.id,
            a.title,
            a.slug,
            a.status,
            a.author_id,
            a.created_at,
            p.username as posted_by,
            a.views
        FROM articles a
        JOIN profiles p 
            ON p.id = a.author_id
        WHERE
            a.author_id = %s
        AND
            a.status != 'deleted'
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """

    params = (
        author_id,
        page_size,
        (page_no - 1) * page_size
    )

    with get_db() as cursor:
        cursor.execute(q, params)
        return cursor.fetchall()


@router.get("/read")
def read_article_by_slug(slug: str):
    update_q = """
        UPDATE articles 
        SET views = views + 1 
        WHERE slug = %s;
    """

    select_q = """
        SELECT
            a.id,
            a.title,
            a.slug,
            a.body,
            a.author_id,
            p.username AS posted_by,
            a.created_at,
            a.views
        FROM articles a
        JOIN profiles p
            ON p.id = a.author_id
        WHERE 
            a.slug = %s     
    """

    with get_db() as cursor:
        cursor.execute(update_q, (slug,))
        
        cursor.execute(select_q, (slug,))
        article = cursor.fetchone()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

@router.post("/")
def create_article(payload: CreateArticle):
    q = """
        INSERT INTO articles (
            title,
            slug,
            status,
            body,
            author_id
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
    """

    params = (
        payload.title,
        payload.slug,
        payload.status,
        json.dumps(payload.body),
        str(payload.user_uuid)
    )

    with get_db() as cursor:
        cursor.execute(q, params)
        return cursor.fetchone()


@router.patch("/")
def edit_article(payload: EditArticle):
    q = """
        UPDATE articles
        SET
            title = %s,
            slug = %s,
            status = %s,
            body = %s
        WHERE id = %s
        RETURNING *
    """

    params = (
        payload.title,
        payload.slug,
        payload.status,
        json.dumps(payload.body),
        str(payload.article_id)
    )

    with get_db() as cursor:
        cursor.execute(q, params)
        return cursor.fetchone()
    

@router.delete("/")
def delete_article(article_id: str = Query(..., description="The UUID of the article to delete")):
    q = """
        UPDATE articles
        SET status = 'deleted'
        WHERE id = %s
        RETURNING id,title,slug
    """

    with get_db() as cursor:
        cursor.execute(q, (article_id,))
        deleted_article = cursor.fetchone()
        
        if not deleted_article:
            raise HTTPException(status_code=404, detail="Article not found")
            
        return {
            "status": "success",
            "message": "Article deleted successfully",
            "deleted_id": deleted_article["id"]
        }   