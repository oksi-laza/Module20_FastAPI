# Приложение 'app' на FastAPI
Веб-сайт по продвижению услуг по строительству жилых частных домов или других сопутствующих услуг(фундамент, крыша, септик и т.д.)


## Установка (Windows)

1. Создание нового проекта на ПК с виртуальным окружением в проекте.

В данном проекте была использована версия Python 3.11

2. Клонирование репозитория.

```git clone https://github.com/oksi-laza/Module20_FastAPI.git```

3. Установка зависимостей в виртуальное окружение.

```pip install -r requirements.txt```

4. Переход в директорию приложения 'app'.

```cd app```

5. Запуск проекта для демонстрации возможностей приложения 'app'.

```python -m uvicorn main:app```


## Что доступно в приложении 'app'?
На данный момент веб-сайт может отображать все страницы, которые есть в меню навигации.

Все страницы оформлены в едином стиле, так как наследуются от основного шаблона 'structure.html' и 
имеют общую стилистику, реализованную в файле 'style1.css'. 

Контентом наполнены не все страницы, но у всех есть шапка, горизонтальное меню и подвал.

На любой странице все ссылки в меню навигации являются действующими и переносят на соответствующую страницу.

Раздел 'Контакты' перенаправляет пользователя в 'footer', где и указаны все реквизиты и контакты компании, 
а нажатие на логотип с названием компании перенаправляет пользователя на главную страницу. 
Стрелка, находящаяся в правом нижнем углу, переносит пользователя наверх страницы.

Главная страница и страница 'Фундаменты' загружены небольшим количеством контента, который можно легко дополнить или 
изменить с помощью queryset-запросов в интерактивной консоли Django (python manage.py shell) или непосредственно 
в самой таблице базы данных.

На главной странице в различных местах располагаются три кнопки вызова формы - две из них для возможности оставить 
контактные данные, а одна форма для возможности самостоятельного выбора даты и времени встречи, соответственно, 
с добавлением или изменением указанной информации в таблице базы данных.

Кнопка, по которой пользователь открывает форму для самостоятельной записи находится в самом низу. 
Также, если пользователь уже был записан, но забыл об этом, повится окно с информацией о дате и времени его прежней 
записи и ему будет предложено оставить или изменить время и дату встречи, при это будут внесены соответствующие 
изменения в таблицу с данными о назначенных встречах. КНОПКА САМОМТОЯТЕЛЬНОЙ ЗАПИСИ НА ВСТРЕЧУ -ЕЩЕ НЕДОРАБОТАНА.

Все данные таблицы, можно также посмотреть и изменить, как один из вариантов, в DB Browser for SQLite.


## Описание функций в проекте на FastAPI
| Расположение в проекте             | Название функции             | Описание                                                                                                                                                                                                                                                                                                         |
|------------------------------------|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| app/backend/db_depends.py          | get_db                       | Функция-генератор для подключения к базе данных                                                                                                                                                                                                                                                                  |
| app                                | main_page                    | Отображает главную страницу. Данные о предоставляемых услугах и специфике работы компании извлекаются из базы данных. Содержит в своем отображаемом шаблоне три кнопки вызова формы - две для возможности оставить контактные данные и одна форма для самостоятельной записи на встречу на выбранную дату и время |
| app/routers/page_navigation        | foundation                   | Отображает страницу с типами фундаментов. Данные о типах фундаментов и ссылки на фотографии соответствующего фундамента извлекаются из базы данных                                                                                                                                                               |
| app/routers/page_navigation        | katalog_proektov_domov       | Отображает страницу с каталогом проектов домов. Страница не наполнена контентом!                                                                                                                                                                                                                                 |
| app/routers/page_navigation        | septic_tanks                 | Отображает страницу с разновидностями септиков. Страница не наполнена контентом!                                                                                                                                                                                                                                 |
| app/routers/page_navigation        | o_kompanii                   | Отображает страницу с информацией о компании. Страница не наполнена контентом!                                                                                                                                                                                                                                   |
| app/routers/page_navigation        | contact_form                 | Отображает форму сбора контактных данных                                                                                                                                                                                                                                                                         |
| app/routers/page_navigation        | contact_form_submit          | Получает данные из формы сбора контактных данных и сохраняет их в таблицу базы данных                                                                                                                                                                                                                            |
| app/routers/form_of_record_routers | form_of_record               | Отображает форму для записи пользователя на офисную встречу                                                                                                                                                                                                                                                      |                                                                                                                                                                       | 
| app/routers/form_of_record_routers | form_of_record_submit        | Получает данные из формы для записи пользователя на офисную встречу и логику обработки полученных данных                                                                                                                                                                                                                 |
| app/routers/form_of_record_routers | update_previous_appointment  | Обновляет в таблице базы данных дату и время встречи, указанную пользователем, а также отображает ответ о назначенной встрече пользователю                                                                                                                                                                       

## Описание моделей таблиц базы данных в проекте на FastAPI
| Название модели       | Описание                                                                                                                                    |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| class Base            | Базовый класс для создания моделей таблиц базы данных. Нужен для сопоставления (объединения) классов моделей в python и таблиц базы данных  |
| class ServicesOffered | Таблица для работы с информацией об услугах, предоставляемых компанией                                                                      |
| class InfoGlavnoe     | Таблица для работы с информацией о специфике работы компании                                                                                |
| class Foundations     | Таблица для работы с информацией о фундаментах, которые строит компания                                                                     |
| class Contact         | Таблица для записи и хранения контактов потенциального клиента: его имя, номер телефона и адрес электронной почты                           |                                                                          
| class MeetingAtOffice | Таблица, содержащая информацию о самостоятельной записи пользователя на встречу в офисе на удобную дату и время                             |


## Описание моделей pydantic в проекте на FastApi
| Название модели                   | Описание                                                                                                                                                   |
|-----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| class ContactCreate               | Модель pydantic для записи контактов потенциального клиента: его имя, номер телефона и адрес электронной почты                                             |
| class ContactResponse             | Модель pydantic для получения информации о потенциальном клиенте: его имя, номер телефона и адрес электронной почты, а также время, когда была создана запись |
| class MeetingAtOfficeCreate       | Модель pydantic для создания записи на встречу на выбранную дату и время                                                                                   |
| class MeetingAtOfficeUpdate       | Модель pydantic для внесения изменений в предыдущую запись о встрече, а именно в дату и время встречи с ранее записанным клиентом                          |
| class MeetingAtOfficeResponse     | Модель pydantic для  получения информации о назначенных встречах с потенциальными клиентами                                                                |
| class ServicesOfferedCreateUpdate | Модель pydentic для работы с информацией об услугах, предоставляемых компанией, добавления или изменения услуг и фотографий                                |
| class InfoGlavnoeCreateUpdate     | Модель pydantic для работы с информацией о специфике работы компании, добавление и изменение этой информации                                               |
| class FoundationsCreateUpdate     | Модель pydantiс для работы с блоком информации о фундаментах, которые строит компания, добавление и удаление описания и фотографий                         |


## Примечание
Все используемые фотографии для наполнения контента были взяты с сайта проектного бюро Z500 https://z500proekty.ru/. 

Все ссылки и переходы на страницах являются действующими, 
формы активными и передающими информацию в таблицы базы данных.

Также внесенные изменения в самих таблицах базы данных будут отображены на сайте, 
но пока это касается предлагаемых услуг и видов фундаментов.

Остальные страницы можно дополнить контентом и моделями по своему усмотрению или по аналогии со страницей "Фундаменты".
