FROM python:3.10.6
RUN mkdir /code
RUN mkdir /code/logs/
WORKDIR /code
ADD dagensalbum.py /code/
ADD test.py /code/
ADD da_second.py /code/
ADD version.json /code/
ENV TZ="Europe/Stockholm"
ARG PLAYLIST_ENVIRONMENT_BUILD
ENV PLAYLIST_ENVIRONMENT_BUILD=${PLAYLIST_ENVIRONMENT_BUILD}
ARG HEADER_AUTH_JSON
ENV HEADER_AUTH_JSON=${HEADER_AUTH_JSON}
ARG HEADER_AUTH_JSON2
ENV HEADER_AUTH_JSON2=${HEADER_AUTH_JSON2}
ENV TEST=${TEST}
RUN pip3 install ytmusicapi requests schedule
CMD ["python3", "./da_second.py"]
