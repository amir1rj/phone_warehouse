FROM python:3.10.13-bookworm
LABEL authors="Amir"

EXPOSE 8000
WORKDIR /main_src
COPY requirements.txt /main_src
RUN pip install -U pipD
RUN pip install -r requirements.txt
COPY . /main_src
CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]