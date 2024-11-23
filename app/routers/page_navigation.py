from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from backend.db_depends import get_db
from sqlalchemy import select, insert, update, and_
from models import Contact, Foundations, MeetingAtOffice
from schemas import ContactCreate, MeetingAtOfficeCreate, MeetingAtOfficeUpdate
from datetime import datetime


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


@router.post('/form_of_record_submit')
async def form_of_record_submit(request: Request, db: Annotated[Session, Depends(get_db)],
                                first_name: str = Form(...), last_name: str = Form(...), phone: str = Form(...),
                                date_of_meeting: str = Form(...), meeting_time: str = Form()) -> HTMLResponse:
    """
    Retrieves data from the form for recording a user for an office meeting
    and the logic of processing the received data
    """
    meeting_time = datetime.strptime(meeting_time, '%H:%M').time()
    date_of_meeting = datetime.strptime(date_of_meeting, '%Y-%m-%d').strftime('%d.%m.%Y')
    context = {
        'date_of_meeting': date_of_meeting,
        'meeting_time': meeting_time,
        'first_name': first_name,
    }
    if not db.query(MeetingAtOffice).filter(
            MeetingAtOffice.first_name == first_name,
            MeetingAtOffice.last_name == last_name,
            MeetingAtOffice.phone == phone).first():
        db.execute(insert(MeetingAtOffice).values(first_name=first_name,
                                                  last_name=last_name,
                                                  phone=phone,
                                                  date_of_meeting=date_of_meeting,
                                                  meeting_time=meeting_time))
        db.commit()
        return templates.TemplateResponse('answer_after_form_of_record.html', {'request': request, **context})
    else:
        queryset = db.scalar(select(MeetingAtOffice).where(
            MeetingAtOffice.first_name == first_name,
            MeetingAtOffice.last_name == last_name,
            MeetingAtOffice.phone == phone))
        previous_date_of_meeting = queryset.date_of_meeting
        previous_meeting_time = queryset.meeting_time
        context.update({'previous_date_of_meeting': previous_date_of_meeting,
                        'previous_meeting_time': previous_meeting_time})

        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['phone'] = phone
        request.session['date_of_meeting'] = date_of_meeting
        request.session['meeting_time'] = meeting_time.strftime('%H:%M')
        request.session['previous_date_of_meeting'] = previous_date_of_meeting
        request.session['previous_meeting_time'] = previous_meeting_time.strftime('%H:%M')
        return templates.TemplateResponse('recording_error.html', {'request': request, **context})


@router.post('/update_previous_appointment')
async def update_previous_appointment(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Updates the date and time of the meeting specified by the user in the database table,
    and also displays the response about the scheduled meeting to the user
    """
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    phone = request.session.get('phone')
    date_of_meeting = request.session.get('date_of_meeting')
    meeting_time = datetime.strptime(request.session.get('meeting_time'), '%H:%M').time()

    if not all([first_name, last_name, phone, date_of_meeting, meeting_time]):
        return templates.TemplateResponse('error.html',
                                          {'request': request, 'message': 'Недостаточно данных для обновления записи.'})

    db.execute(update(MeetingAtOffice).where(and_(
        MeetingAtOffice.first_name == first_name,
        MeetingAtOffice.last_name == last_name,
        MeetingAtOffice.phone == phone)).values(
        date_of_meeting=date_of_meeting,
        meeting_time=meeting_time))
    db.commit()
    print(f'Клиент {first_name} {last_name} перезаписался на {date_of_meeting} в {meeting_time}')
    context = {'date_of_meeting': date_of_meeting, 'meeting_time': meeting_time, 'first_name': first_name}

    request.session.pop('first_name', None)
    request.session.pop('last_name', None)
    request.session.pop('phone', None)
    request.session.pop('date_of_meeting', None)
    request.session.pop('meeting_time', None)
    request.session.pop('previous_date_of_meeting', None)
    request.session.pop('previous_meeting_time', None)
    return templates.TemplateResponse('answer_after_form_of_record.html', {'request': request, **context})
