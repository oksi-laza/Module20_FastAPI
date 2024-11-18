from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from backend.db_depends import get_db
from sqlalchemy import select
from models import ServicesOffered, InfoGlavnoe
from routers import page_navigation, form_of_record_routers

app = FastAPI()
# python -m uvicorn main:app - команда для запуска в терминале

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def main_page(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    """
    Renders the main page. Data on the services provided and
    the specifics of the company's work are extracted from the database.
    """
    services_offered = db.scalars(select(ServicesOffered)).all()
    info_main = db.scalars(select(InfoGlavnoe)).all()
    return templates.TemplateResponse('main_page.html', {'request': request,
                                                         'services_offered': services_offered,
                                                         'info_main': info_main})


app.include_router(page_navigation.router)
app.include_router(form_of_record_routers.router)
