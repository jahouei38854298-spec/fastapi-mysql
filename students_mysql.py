import re
from datetime import date

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from auth_mysql import (
    require_admin,
    get_csrf_token,
    validate_csrf_token,
)
from mysql_database import get_db
from models import StudentDB
from schemas import Student, get_persian_errors


router = APIRouter()
templates = Jinja2Templates(directory="templates")


def serialize_student(student: StudentDB) -> dict:
    return {
        "_id": str(student.id),
        "name": student.name,
        "age": student.age,
        "birth_date": student.birth_date.isoformat(),
        "father_name": student.father_name,
        "birth_place": student.birth_place,
        "phone": student.phone,
        "email": student.email,
        "address": student.address,
    }


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    message: str | None = None,
    name: str = "",
    phone: str = "",
    email: str = "",
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(StudentDB)

    if name.strip():
        query = query.filter(
            StudentDB.name.ilike(f"%{name.strip()}%")
        )

    if phone.strip():
        query = query.filter(
            StudentDB.phone.like(f"%{phone.strip()}%")
        )

    if email.strip():
        query = query.filter(
            StudentDB.email.ilike(f"%{email.strip()}%")
        )

    students = [
        serialize_student(student)
        for student in query.order_by(StudentDB.id).all()
    ]

    messages = {
        "added": {
            "text": "کاربر جدید اضافه شد.",
            "type": "success",
        },
        "deleted": {
            "text": "کاربر با موفقیت حذف شد.",
            "type": "error",
        },
        "updated": {
            "text": "اطلاعات کاربر با موفقیت اصلاح شد.",
            "type": "warning",
        },
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "students": students,
            "notification": messages.get(message),
            "search_name": name,
            "search_phone": phone,
            "search_email": email,
            "csrf_token": get_csrf_token(request),
            "search_performed": any(
                value.strip()
                for value in (name, phone, email)
            ),
        },
    )


@router.get("/add", response_class=HTMLResponse)
def show_add_form(
    request: Request,
    admin=Depends(require_admin),
):
    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context={
            "student": None,
            "page_title": "افزودن کاربر جدید",
            "form_action": "/add",
            "submit_text": "ثبت کاربر",
            "csrf_token": get_csrf_token(request),
        },
    )


@router.get("/add/{student_id}", response_class=HTMLResponse)
def show_edit_form(
    request: Request,
    student_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="student not found",
        )

    student_data = serialize_student(student)

    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context={
            "student": student_data,
            "page_title": "ویرایش اطلاعات کاربر",
            "form_action": f"/add?student_id={student_id}",
            "submit_text": "ذخیره تغییرات",
            "csrf_token": get_csrf_token(request),
        },
    )


@router.post("/add")
def save_student_from_page(
    request: Request,
    student_id: int | None = None,
    name: str = Form(""),
    age: str = Form(""),
    birth_date: str = Form(""),
    father_name: str = Form(""),
    birth_place: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    address: str = Form(""),
    admin=Depends(require_admin),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    validate_csrf_token(request, csrf_token)

    existing_student = None

    if student_id is not None:
        existing_student = db.query(StudentDB).filter(
            StudentDB.id == student_id
        ).first()

        if existing_student is None:
            raise HTTPException(
                status_code=404,
                detail="کاربر پیدا نشد.",
            )

    form_data = {
        "name": name,
        "age": age,
        "birth_date": birth_date,
        "father_name": father_name,
        "birth_place": birth_place,
        "phone": phone,
        "email": email,
        "address": address,
    }

    is_editing = existing_student is not None

    page_title = (
        "ویرایش اطلاعات کاربر"
        if is_editing
        else "افزودن کاربر جدید"
    )

    form_action = (
        f"/add?student_id={student_id}"
        if is_editing
        else "/add"
    )

    submit_text = (
        "ذخیره تغییرات"
        if is_editing
        else "ثبت کاربر"
    )

    try:
        student = Student(
            name=name,
            age=age,
            birth_date=birth_date,
            father_name=father_name,
            birth_place=birth_place,
            phone=phone,
            email=email,
            address=address.strip() or None,
        )

    except ValidationError as exc:
        return templates.TemplateResponse(
            request=request,
            name="add.html",
            context={
                "student": (
                    serialize_student(existing_student)
                    if existing_student
                    else None
                ),
                "page_title": page_title,
                "form_action": form_action,
                "submit_text": submit_text,
                "errors": get_persian_errors(exc),
                "form_data": form_data,
                "csrf_token": get_csrf_token(request),
            },
            status_code=422,
        )

    student_data = student.model_dump()

    if is_editing:
        for field, value in student_data.items():
            setattr(existing_student, field, value)

        message = "updated"

    else:
        db.add(StudentDB(**student_data))
        message = "added"

    db.commit()

    return RedirectResponse(
        url=f"/?message={message}",
        status_code=303,
    )


@router.post("/students/{student_id}/delete")
def delete_student_from_page(
    request: Request,
    student_id: int,
    csrf_token: str = Form(...),
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    validate_csrf_token(request, csrf_token)

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="student not found",
        )

    db.delete(student)
    db.commit()

    return RedirectResponse(
        url="/?message=deleted",
        status_code=303,
    )
