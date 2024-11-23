from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from backend.db_depends import get_db
from sqlalchemy import select
from models import MeetingAtOffice
from schemas import MeetingAtOfficeUpdate
from datetime import datetime


router = APIRouter(prefix='/form_of_record', tags=['form_of_record'])

templates = Jinja2Templates(directory='templates')


@router.get('')
async def form_of_record(request: Request) -> HTMLResponse:
    """Displays a form for recording a user for an office meeting."""
    return templates.TemplateResponse('form_of_record.html', {'request': request})


@router.get('/no_changes_previous_appointment')
async def no_changes_previous_appointment(request: Request) -> HTMLResponse:
    """Displays the response to the user about saving the previously scheduled date and time of the meeting"""
    first_name = request.session.get('first_name')
    previous_date_of_meeting = request.session.get('previous_date_of_meeting')
    previous_meeting_time = datetime.strptime(request.session.get('previous_meeting_time'), '%H:%M').time()

    if not all([first_name, previous_date_of_meeting, previous_meeting_time]):
        return templates.TemplateResponse('error.html',
                                          {'request': request, 'message': 'Недостаточно данных для обновления записи.'})

    print(f'Клиент {first_name} оставил прежнюю запись: {previous_date_of_meeting} в {previous_meeting_time}')
    context = {
        'previous_date_of_meeting': previous_date_of_meeting,
        'previous_meeting_time': previous_meeting_time,
        'first_name': first_name,
    }
    request.session.pop('first_name', None)
    request.session.pop('last_name', None)
    request.session.pop('phone', None)
    request.session.pop('date_of_meeting', None)
    request.session.pop('meeting_time', None)
    request.session.pop('previous_date_of_meeting', None)
    request.session.pop('previous_meeting_time', None)
    return templates.TemplateResponse('answer_about_saving_previous_record.html', {'request': request, **context})
