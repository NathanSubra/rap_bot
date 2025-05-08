# RapBot – Full Stack NLP Application

#### Galileo Steinberg, Nathan Subrahmanian, Effren Haskell

An interactive web application that generates rap lyrics in the style of any artist and produces accompanying music tracks using AI services.

---

## Features

- **Lyric Generation** via OpenAI Chat API using a custom `RapGenerator` service.
- **Music Generation** using the Mureka AI music API through `MurekaMusic`.
- **Web Front-End** built with Flask and Jinja2 templates (`index.html` and `library.html`).
- **Database Back-End** powered by Flask-SQLAlchemy with a SQLite instance for persisting saved tracks.
- **RESTful API Endpoints** for generating lyrics/music, saving tracks, listing library, and streaming audio.
- **Unit Tests** verifying core data models and persistence logic.
- **Containerized Deployment** via Docker and Docker Compose for zero-configuration setup.

---

## Prerequisites

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- `.env` file with the following environment variables:

  ```shell
  OPENAI_API_KEY=<OpenAI API key>
  MUREKA_API_KEY=<Mureka AI API key>
  SECRET_KEY=<Flask secret key>
  DATABASE_URI=<optional, defaults to SQLite instance/rapbot.db>

---

## Installation & Startup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Create `.env`** at project root.

3. **Build & Run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

4. **Access the Application**

   * Web UI: [http://localhost:8000/](http://localhost:8000/)
   * Library Page: [http://localhost:8000/library](http://localhost:8000/library)

> **Alternative: Local Python Setup**

> ```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
> flask run --host=0.0.0.0 --port=8000
> ```

---

## API Endpoints

|      Endpoint       | Method | Description                                                                                                         |
|:-------------------:|--------|---------------------------------------------------------------------------------------------------------------------|
|     `/generate`     | POST   | Generate lyrics & music. JSON `{ artist, topic, additional_context, prompt? }` → `{ lyrics, audio (base64), mime }` |
|      `/songs`       | POST   | Save a track to the library. JSON payload → `{ id }`                                                                |
|    `/api/songs`     | GET    | Retrieve JSON list of saved tracks                                                                                  |
| `/songs/<id>/audio` | GET    | Stream saved track audio (MP3)                                                                                      |
|    `/songs/<id>`    | DELETE | Delete a track from the library                                                                                     |

---

## Project Structure

```
├── backend/                      # Flask application package
│   ├── app/
│   │   ├── __init__.py           # Application factory
│   │   ├── config.py             # Configuration (DB URI, secret)
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── routes.py             # Flask routes & API blueprints
│   │   ├── static/           
│   │   │    └── style.css        # Custom CSS
│   │   └── services/             # AI integration services
│   │       ├── generator.py      # Rap lyrics via OpenAI Chat
│   │       └── mureka_music.py   # Music via Mureka AI API
├── front_end/                    # Jinja2 templates & static assets
│   ├── app.py                    # Flask app
│   ├── templates/
│   │   ├── index.html
│   │   └── library.html
│   └── static/
│       └── style.css
├── instance/                     # SQLite database instance
│   └── rapbot.db                 # SQLite database file
├── test/                         # SQLite database instance
│   └── test.py                   # Unit tests
├── .env                          # Environment variables
├── docker-compose.yml            # Compose config for container
├── Dockerfile                    # Docker image build instructions
├── requirements.txt              # Python dependencies
└── README.md                     # This documentation
```

---

## Running Tests

You can run the full test suite either inside Docker or on your local machine.

### Inside Docker

Make sure your containers are up:

```bash
# Using unittest
docker compose exec rapbot python3 -m unittest discover -s test -p "test_*.py"
```

### Locally
From your project root:
```bash
# Using unittest
python3 -m unittest discover -s test -p "test_*.py"
```
You can also run the tests individually by running the test file directly.


---

## Report & Documentation

Please refer to the project write-up for details on design decisions, implementation challenges, and contributions.

---

*Happy rhyming!*
