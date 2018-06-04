FROM python:3
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
CMD [ "python3", "./SensorsBackend/manage.py" ,"runserver", "0.0.0.0:8000" ]
