from fastapi import APIRouter, HTTPException, Depends, Query

from schemas import Quarter
from services import kundoluk
from services.auth import AuthHandler

auth_handler = AuthHandler()
router = APIRouter(
    prefix='/student',
    tags=['Student'],
)


@router.get('/grades')
async def student_grades(
        cookies: dict = Depends(auth_handler.auth_wrapper),
        student_id: int = Query(...),
        lesson_id: int = Query(...),
        quarter: Quarter = Query(
            default=Quarter.CURRENT,
            description='0 - current, from 1 to 4 are quarter numbers, 5 - total quarters'),
):
    try:
        journal = await kundoluk.get_student_grades_by_lesson(
            cookies, student_id, lesson_id, quarter.value)
    except Exception:
        raise HTTPException(status_code=400)
    return journal
