FROM python:alpine

WORKDIR /home/appuser/
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py" ]
