# Recollection

Recollection is a screenshot OCR and storage service that captures screenshots, extracts text using OCR, computes embeddings, and stores the data in a database and object storage. This project uses FastAPI for the backend, MinIO for object storage, and a libSQL server for the database.

## Prerequisites

* Docker and Docker Compose installed on your machine
* Python 3.11 or higher
* Node.js 18 or higher

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd recollection
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the Python dependencies:
   ```sh
   pip install -r backend/requirements.txt
   ```

4. Install the Node.js dependencies:
   ```sh
   cd frontend
   npm install
   cd ..
   ```

5. Build the Docker images and start the services:
   ```sh
   docker-compose -f docker/docker-compose.yml up --build
   ```

## Configuration

The configuration is managed using environment variables. Create a `.env` file in the root directory with the following content:

```sh
LIBSQL_URL=http://libsql-server:8080
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=recollection
MINIO_SECRET_KEY=strongpassword
CLIP_MODEL_PATH=/path/to/clip-tiny-model
```

## Usage

### Backend

The backend is built using FastAPI and provides several endpoints:

* `POST /capture`: Captures a screenshot, extracts text, computes embeddings, and stores the data.
* `GET /timeline`: Retrieves the timeline of captured screenshots.
* `POST /settings`: Updates the capture settings.
* `POST /search`: Searches for screenshots based on a query and threshold.

### Frontend

The frontend is built using React and Vite. It provides a user interface to interact with the backend services.

1. Start the frontend development server:
   ```sh
   cd frontend
   npm start
   ```

2. Open your browser and navigate to `http://localhost:3000`.

## Directory structure

* `backend/`: Contains the backend code.
  * `backend/config.py`: Configuration settings for the backend.
  * `backend/main.py`: Main entry point for the FastAPI application.
  * `backend/repositories/`: Contains repository classes for interacting with the database and object storage.
    * `backend/repositories/libsql_repo.py`: Repository for interacting with the libSQL database.
    * `backend/repositories/minio_repo.py`: Repository for interacting with MinIO object storage.
  * `backend/services/`: Contains service classes for various functionalities.
    * `backend/services/embedding.py`: Service for computing text and image embeddings.
    * `backend/services/ocr_tpu.py`: Service for extracting text using OCR and TPU.
    * `backend/services/screenshot.py`: Service for capturing screenshots and managing related operations.
  * `backend/use_cases/`: Contains use case classes for various operations.
    * `backend/use_cases/capture.py`: Use case for capturing screenshots.
    * `backend/use_cases/search.py`: Use case for searching screenshots.
* `frontend/`: Contains the frontend code.
  * `frontend/src/`: Source code for the frontend.
    * `frontend/src/App.jsx`: Main application component.
    * `frontend/src/components/`: Contains React components.
      * `frontend/src/components/Timeline.jsx`: Component for displaying the timeline of screenshots.
    * `frontend/src/services/`: Contains service classes for interacting with the backend API.
      * `frontend/src/services/api.js`: Service for making API requests to the backend.
* `docker/`: Contains Docker-related files.
  * `docker/docker-compose.yml`: Docker Compose configuration file.
  * `docker/Dockerfile`: Dockerfile for building the backend and frontend images.
* `scripts/`: Contains utility scripts.
  * `scripts/build_tpu_models.sh`: Script for downloading and setting up TPU models.
* `pyproject.toml`: Project configuration file for Python dependencies and tools.
