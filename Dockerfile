FROM python:slim

RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser/

ENV PATH="/home/appuser/.local/bin:$PATH"
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py" ]
