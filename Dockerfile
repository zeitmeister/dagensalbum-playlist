FROM python:3.10.6
RUN mkdir /code
RUN mkdir /code/logs/
WORKDIR /code
ADD dagensalbum.py /code/
ADD test.py /code/
ADD header-auth.json /code/
ENV TZ="Europe/Stockholm"
RUN pip3 install ytmusicapi requests schedule
CMD ["python3", "./da_second.py"]
