# Rap Bot – Full Stack

Comprehensive implementation for generating rap lyrics and music generation.

## 1 Quick demo (after training)

```bash
docker compose --env-file .env up --build
open http://localhost:8000
```




## 4 Run the app

2. `docker compose --env-file .env up --build`  
3. Browse to http://localhost:8000

## 5 Endpoints

* **POST /generate** – JSON `{artist, sub_genre, topic}` → returns `lyrics`, `audio` (base64 WAV)
* **POST /songs** – save song
* **GET /library** – list saved songs
* **GET /song/<id>** – fetch single song

## 6 Tests

```bash

```
