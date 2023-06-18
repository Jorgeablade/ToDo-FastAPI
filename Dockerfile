FROM python:3.9

WORKDIR /todo-list

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./todo ./todo

RUN python3 ./todo/random_key.py

CMD [ "python3", "./todo/app.py" ]