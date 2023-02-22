# HTTP File Server

A simple HTTP File Server implemented using Python, [FastAPI](https://fastapi.tiangolo.com/), and [Docker](https://www.docker.com/).
The server exposes HTTP endpoint `/files/{file_path}` that returns files from the specified directory.

The server also includes Prometheus metrics exporter from library [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator).

## Get Started

Pull image from the Docker Hub.
```bash
docker pull chamidullinr/http-file-server:latest
```

Or build the docker image.
```bash
docker build --tag http-file-server .
```

Then, run the docker container. Change `[DIRECTORY_TO_MOUNT]` with a path to some directory on the host machine.  
```bash
docker run \
  --publish 8080:8080 \
  --volume [DIRECTORY_TO_MOUNT]:/Data \
  --name http-file-server \
  http-file-server
```

Access files in directory `[DIRECTORY_TO_MOUNT]` from URL `http://localhost:8080/files/{file_path}`. 
