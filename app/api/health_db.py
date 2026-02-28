from fastapi import APIRouter, status

from app.core.db import check_db_connection

router = APIRouter()


@router.get("/health/db")
def health_db():
    ok, detail = check_db_connection()
    if ok:
        return {"status": "ok"}
    return {"status": "fail", "detail": detail}, status.HTTP_503_SERVICE_UNAVAILABLE