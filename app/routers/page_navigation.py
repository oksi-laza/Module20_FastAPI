from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from backend.db_depends import get_db
from sqlalchemy import select, insert
from models import Contact, Foundations
from schemas import ContactCreate


router = APIRouter(prefix='', tags=['navigation'])

templates = Jinja2Templates(directory='templates')


@router.get('/foundation')
async def foundation(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """Displays a page with the types of foundations. Data on the types of foundations and
    links to photos of the corresponding foundation are extracted from the database."""
    foundations_all = db.scalars(select(Foundations)).all()
    return templates.TemplateResponse('foundation.html', {'request': request, 'foundations_all': foundations_all})


@router.get('/katalog_proektov_domov')
async def katalog_proektov_domov(request: Request) -> HTMLResponse:
    """Renders a page with a catalog of house projects."""
    return templates.TemplateResponse('katalog_proektov_domov.html', {'request': request})


@router.get('/septic_tanks')
async def septic_tanks(request: Request) -> HTMLResponse:
    """Renders a page with septic tanks varieties."""
    return templates.TemplateResponse('septic_tanks.html', {'request': request})


@router.get('/o_kompanii')
async def o_kompanii(request: Request) -> HTMLResponse:
    """Renders a page with information about the company."""
    return templates.TemplateResponse('o_kompanii.html', {'request': request})


@router.get('/contact_form')
async def contact_form(request: Request) -> HTMLResponse:
    """Displays the contact data collection form."""
    return templates.TemplateResponse('contact_form.html', {'request': request})


@router.post('/contact_form_submit')
async def contact_form_submit(request: Request, db: Annotated[Session, Depends(get_db)],
                              name: str = Form(...), phone: str = Form(...), email: str = Form(...)) -> HTMLResponse:
    """Retrieves data from the contact data collection form and saves it to a database table"""
    db.execute(insert(Contact).values(name=name, phone=phone, email=email))
    db.commit()
    return templates.TemplateResponse('answer_after_contact_form.html', {'request': request})
