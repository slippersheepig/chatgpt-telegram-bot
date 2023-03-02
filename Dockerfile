FROM rust:slim-bookworm

RUN apt update && apt install pip -y

RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser/

ENV PATH="/home/appuser/.local/bin:$PATH"
COPY . .
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
