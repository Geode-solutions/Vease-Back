FROM python:3.9-slim

WORKDIR /server

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install .

RUN apt-get update 
RUN apt-get install libgomp1
RUN apt-get install -y curl

RUN apt-get update && apt-get install -y wget

CMD ["vease-back", "--data_folder_path", "/data"]

EXPOSE 5000