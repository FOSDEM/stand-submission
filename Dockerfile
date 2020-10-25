FROM python:3

WORKDIR /code

COPY ./ /code/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code/standssubmission

CMD ["python", "manage.py", "runserver", "0:8000"]
