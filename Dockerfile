FROM python:3.9-slim

WORKDIR /server

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install . && \
    apt-get update && \
    apt-get install libgomp1 && \
    apt-get install -y curl && \
    apt-get update && apt-get install -y wget

CMD ["vease-back", "--data_folder_path", "/data", "--allowed_origins", "['https://next.vease.geode-solutions.com', 'https://vease.geode-solutions.com']" , "--timeout", "300"]

EXPOSE 5000