FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get install -y binutils

WORKDIR /app

COPY . .
RUN pip3 install --no-cache-dir . pyinstaller

RUN pyinstaller \
    --onefile \
    --collect-data opengeodeweb_back \
    --collect-data vease_back \
    --recursive-copy-metadata vease_back src/vease_back/app.py \
    --distpath dist \
    --name vease-back \
    --clean
ENV PYTHON_ENV="prod"

FROM debian:12-slim

COPY --from=builder /app/dist/vease-back /usr/local/bin/vease-back
RUN chmod +x /usr/local/bin/vease-back

EXPOSE 5000
ENV PYTHON_ENV=prod

ENTRYPOINT ["/usr/local/bin/vease-back"]
CMD ["--data_folder_path", "/data", \
    "--allowed_origins", "['https://next.vease.geode-solutions.com', 'https://vease.geode-solutions.com']", \
    "--timeout", "5"]

