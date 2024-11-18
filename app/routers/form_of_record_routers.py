from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from backend.db_depends import get_db
from sqlalchemy import select, insert, update
from models import MeetingAtOffice
from schemas import MeetingAtOfficeCreate, MeetingAtOfficeUpdate
from datetime import datetime


router = APIRouter(prefix='/form_of_record', tags=['form_of_record'])

templates = Jinja2Templates(directory='templates')


@router.get('')
async def form_of_record(request: Request) -> HTMLResponse:
    """Displays a form for recording a user for an office meeting."""
    return templates.TemplateResponse('form_of_record.html', {'request': request})


@router.post('/form_of_record_submit')
async def form_of_record_submit(request: Request, db: Annotated[Session, Depends(get_db)],
                                first_name: str = Form(...), last_name: str = Form(...), phone: str = Form(...),
                                date_of_meeting: str = Form(...), meeting_time: str = Form()) -> HTMLResponse:
    """
    Retrieves data from the form for recording a user for an office meeting
    and the logic of processing the received data
    """
    if not db.query(MeetingAtOffice).filter(MeetingAtOffice.first_name == first_name,
                                            MeetingAtOffice.last_name == last_name,
                                            MeetingAtOffice.phone == phone).first():
        new_meeting = MeetingAtOffice(first_name=first_name, last_name=last_name, phone=phone,
                                      date_of_meeting=date_of_meeting, meeting_time=meeting_time)
        db.add(new_meeting)
        db.commit()
        return templates.TemplateResponse('answer_after_form_of_record.html', {'request': request})
    else:
        queryset = db.scalar(select(MeetingAtOffice).where(
            first_name=first_name, last_name=last_name, phone=phone).values_list('date_of_meeting', 'meeting_time'))
        previous_date_of_meeting = queryset[date_of_meeting]
        previous_meeting_time = queryset[meeting_time]
        # Сохранение данных в сессию
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['phone'] = phone
        request.session['date_of_meeting'] = date_of_meeting
        request.session['meeting_time'] = meeting_time
        request.session['previous_date_of_meeting'] = previous_date_of_meeting
        request.session['previous_meeting_time'] = previous_meeting_time
        return templates.TemplateResponse('recording_error.html', {'request': request,
                                                                   'previous_date_of_meeting': previous_date_of_meeting,
                                                                   'previous_meeting_time': previous_meeting_time
                                                                   })


@router.put('/update_previous_appointment')
async def update_previous_appointment(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Updates the date and time of the meeting specified by the user in the database table,
    and also displays the response about the scheduled meeting to the user
    """
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    phone = request.session.get('phone')
    date_of_meeting = request.session.get('date_of_meeting')
    meeting_time = request.session.get('meeting_time')

    print(f'Клиент {first_name} {last_name} перезаписался на {date_of_meeting} в {meeting_time}')
    update_meeting = MeetingAtOffice(first_name=first_name, last_name=last_name, phone=phone,
                                     date_of_meeting=date_of_meeting, meeting_time=meeting_time)
    db.add(update_meeting)
    db.commit()
    return templates.TemplateResponse('answer_after_form_of_record.html', {'request': request})


@router.get('/no_changes_previous_appointment')
async def no_changes_previous_appointment(request: Request) -> HTMLResponse:
    """Displays the response to the user about saving the previously scheduled date and time of the meeting"""
    first_name = request.session.get('first_name')
    # last_name = request.session.get('last_name')
    # phone = request.session.get('phone')
    previous_date_of_meeting = request.session.get('previous_date_of_meeting')
    previous_meeting_time = request.session.get('previous_meeting_time')
    # queryset = MeetingAtOffice.objects.filter(
    #     first_name=first_name, last_name=last_name, phone=phone).values_list('date_of_meeting', 'meeting_time')
    # previous_date_of_meeting = queryset[0][0]
    # previous_meeting_time = queryset[0][1]
    #
    print(f'Клиент {first_name} оставил прежнюю запись: {previous_date_of_meeting} в {previous_meeting_time}')
    # context = {
    #     'previous_date_of_meeting': previous_date_of_meeting,
    #     'previous_meeting_time': previous_meeting_time,
    #     'first_name': first_name,
    # }
    return templates.TemplateResponse('answer_about_saving_previous_record.html',
                                      {'request': request,
                                       'previous_date_of_meeting': previous_date_of_meeting,
                                       'previous_meeting_time': previous_meeting_time,
                                       'first_name': first_name})
