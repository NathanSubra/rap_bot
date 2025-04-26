# Rap Bot – Full Stack

Comprehensive implementation for generating rap lyrics with a fine‑tuned LLM and Bark TTS, served via a Flask + Tailwind website.

## 1 Quick demo (after training)

```bash
docker compose --env-file .env up --build
open http://localhost:8000
```

## 2 Collect lyrics

```bash
pip install -r requirements.txt
export GENIUS_TOKEN=…
python scripts/fetch_lyrics.py --artist "Kendrick Lamar" --max 120
python scripts/fetch_lyrics.py --artist "Drake" --max 120
```

## 3 Fine‑tune LoRA

```bash
python scripts/train_rap_model.py             --data data/lyrics.jsonl             --base mistralai/Mistral-7B-Instruct-v0.2             --out models/rap-lora             --epochs 3             --bsz 2
```

> Need a GPU with ~30 GB or two 24 GB cards (QLoRA 4‑bit).

## 4 Run the app

1. Ensure `models/rap-lora` exists (from step 3).  
2. `docker compose --env-file .env up --build`  
3. Browse to http://localhost:8000

## 5 Endpoints

* **POST /generate** – JSON `{artist, sub_genre, topic}` → returns `lyrics`, `audio` (base64 WAV)
* **POST /songs** – save song
* **GET /library** – list saved songs
* **GET /song/<id>** – fetch single song

## 6 Tests

```bash
pytest -q --cov
```
