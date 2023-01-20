FROM python:3.10-slim

WORKDIR /chatgpt
ENV PATH="${PATH}:/usr/local/bin:/usr/bin:/bin"

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install chromium xvfb xauth -y

CMD [ "python", "bot.py" ]
