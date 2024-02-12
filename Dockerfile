FROM docker.io/python:3.10

WORKDIR /

# --- [Install python and pip] ---
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip git
COPY . /

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

<<<<<<< HEAD
ENV GUNICORN_CMD_ARGS="--workers=1 --bind=0.0.0.0:8082"

EXPOSE 8082
=======
ENV GUNICORN_CMD_ARGS="--workers=1 --bind=0.0.0.0:8028"

EXPOSE 8028
>>>>>>> 91a971119f0a13f4cc9f3f2f4632747879b0eb3b

CMD [ "gunicorn", "main:app" ]
