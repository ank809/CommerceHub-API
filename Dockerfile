FROM ubuntu

WORKDIR /app

COPY . .

RUN apt update && apt install -y python3 python3-pip

RUN pip3 install flask

RUN pip3 install flask-pymongo

RUN pip3 install Flask-JWT-Extended

# EXPOSE 5000

CMD [ "python3", "run.py" ]