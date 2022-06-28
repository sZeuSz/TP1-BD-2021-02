FROM python:3
WORKDIR /app
COPY . /app
RUN pip install psycopg2
RUN pip install rich
RUN pip install tomlkit
RUN pip install toml
# CMD ["python", "tp1_3.2.py"]
