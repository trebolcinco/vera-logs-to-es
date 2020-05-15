FROM python:3.6
ENV ES_HOST="0.0.0.0" \
    ES_PORT="0000" \
    PYTHONUNBUFFERED=1 \
    VERA_LOG_INDEX="vera-log" \
    VERA_HOST="0.0.0.0" \
    SLEEP_TIME=60 \
    REBOOT_TIME=
WORKDIR /vera-log-to-es
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
WORKDIR /vera-log-to-es
COPY *.py .
COPY functions/ functions/
CMD ["python","-u","main.py"]