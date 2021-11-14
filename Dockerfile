FROM python:3.9

WORKDIR /app

COPY requirements.txt ./requirements.txt

COPY data data

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]