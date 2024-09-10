FROM python:3.11

WORKDIR /app

COPY requirements.txt .
COPY ./chat_with_history.py /app/chat_with_history.py
COPY ./.streamlit /app/.streamlit

RUN python -m venv /opt/vemv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD [ "streamlit", "run", "./chat_with_history.py" ]