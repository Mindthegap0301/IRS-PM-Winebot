FROM python:3.10.11-bullseye

# Install Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
WORKDIR /src
COPY . .

# Allow installing dev dependencies to run tests
RUN poetry install

# Update database
RUN alembic upgrade head
RUN flask seed run

EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run", "--port", "5000", "--host", "0.0.0.0"]