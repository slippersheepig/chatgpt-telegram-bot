FROM ultrafunk/undetected-chromedriver

WORKDIR /chatgpt
ENV PATH="${PATH}:/usr/local/bin:/usr/bin:/bin"

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "bot.py" ]
