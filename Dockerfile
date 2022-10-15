FROM python:3.8.14-slim-buster
WORKDIR /app
COPY ./ThesisManagementSystem ./

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt 

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "manage.py", "collectstatic"]
CMD ["gunicorn", "ThesisManagementSystem.wsgi:application", "--bind", "0.0.0.0:8000"]