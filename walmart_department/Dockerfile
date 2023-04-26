FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./walmart_departments.py" ]
