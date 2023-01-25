FROM python:3.9.16-slim

COPY ./ /api

# create directory for logs
RUN mkdir "/logs"

# install python dependencies
ENV APP_DIR='/api'
WORKDIR $APP_DIR
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --compile -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

# expose ports and run application
EXPOSE 8080
CMD uvicorn rest_server:app \
    --host 0.0.0.0 \
    --port 8080 \
    --log-config logging.yaml \
    --log-level info
