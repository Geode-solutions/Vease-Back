FROM python:3.9-slim

ARG TOKEN

WORKDIR /server

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update 
RUN apt-get install libgomp1
RUN apt-get install -y curl

RUN curl -H "Accept: application/vnd.github.VERSION.raw" -H "Authorization: token $TOKEN" https://api.github.com/repos/Geode-solutions/open-license-manager/contents/projects/geode/geode.lic\?ref\=master > /server/geode.lic
RUN apt-get update && apt-get install -y wget

ENV GEODE_LICENSE_LOCATION=/server/geode.lic

CMD ["python3", "app.py"]

EXPOSE 5000