FROM rust:slim-bookworm

WORKDIR /chatgpt
ENV PATH="${PATH}:/usr/local/bin:/usr/bin:/bin"

COPY . .
RUN apt update && apt install pip -y
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
