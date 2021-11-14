FROM python:3.9

WORKDIR /app

COPY requirements.txt ./requirements.txt

COPY data data

COPY app.py .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]