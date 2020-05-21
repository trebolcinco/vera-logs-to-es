FROM python:3.6
ENV ES_HOST="0.0.0.0" \
    ES_PORT="0000" \
    PYTHONUNBUFFERED=1 \
    VERA_LOG_INDEX="vera-log" \
    VERA_HOST="0.0.0.0" \
    SLEEP_TIME=60 \
    SKIP_RELOAD="false"
WORKDIR /vera-log-to-es
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY main.py .
COPY functions/ functions/
COPY elastic-search/ elastic-search/
CMD ["python","-u","main.py"]