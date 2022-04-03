Houses rental system API.
------------------------

I went over the whole FastAPI framework, you can find great examples here for authentication and CRUD,

this app is free to use for any purpose.

For installing:

create your virtual environment and type inside:

pip install -r ./requirements.txt

you simply need to create .env file in the backend folder and enter your db details, for example in my case:

POSTGRES_USER=
POSTGRES_DB=
POSTGRES_PASSWORD=
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
SECRET_KEY=


and the run command is:

uvicorn main:app --reload
