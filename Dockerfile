FROM python:3.7.9

MAINTAINER Nik Mourelatos

RUN apt-get update

RUN apt-get install tesseract-ocr -y

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y  python3-pip python-dev

RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

RUN apt-get install libssl-dev

RUN apt-get install make build-essential libssl-dev zlib1g-dev libbz2-dev libsqlite3-dev

ARG DEBIAN_FRONTEND=noninteractive

# We copy just the requirements.txt first to leverage Docker cache

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

RUN python3.7 -c "import nltk; nltk.download('wordnet')"
RUN python3.7 -c "import nltk; nltk.download('punkt')"

ENTRYPOINT [ "python" ]

CMD [ "./application.py" ]