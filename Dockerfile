FROM python:3.9-slim

WORKDIR /demencia-backend

COPY ./requirements/ ./requirements/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements/dev.txt

COPY ./ ./

COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ./entrypoint.sh