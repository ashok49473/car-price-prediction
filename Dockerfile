FROM python:3.7

COPY . /usr/car_price/

EXPOSE 5000

WORKDIR /usr/car_price/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]