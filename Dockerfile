FROM python:3.12-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV OPENAI_API_KEY=your_openai_api_key

CMD ["streamlit", "run", "app.py"]
