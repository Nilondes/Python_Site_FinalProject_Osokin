FROM python:3.12-slim

WORKDIR clothing_rental/

COPY requirements.txt /clothing_rental/

RUN pip install -r requirements.txt

COPY . /clothing_rental/

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["bash", "-c"]
CMD ["./docker-entrypoint.sh"]