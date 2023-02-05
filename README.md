# Causal Inference

This repository contains R codes about the Causal Inference.

## How to use

- create a directory for docker
- make a YAML file as follows

```yaml: docker-compose.yml
version: '3'

services:
  rstudio:
    image: rocker/rstudio
    container_name: rstudio
    ports:
      - 8787:8787
    environment:
      PASSWORD: xxxxxx #arbitrary pass
      TZ: Asia/Tokyo
    volumes:
      - ../R:/home/rstudio
```

- execute ```docker-compose up``` in docker directory
- insert URL ```http://localhost:8787/```
- input a user information
  - user name
  - password
