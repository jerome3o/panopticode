FROM python:3.8

WORKDIR /app
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --deploy
COPY apitools/ ./apitools/
COPY srv/ ./srv/
COPY models.py .

CMD ["pipenv", "run", "serve"]