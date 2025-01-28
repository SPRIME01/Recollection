#!/bin/bash

# Create the project structure
mkdir -p recollection/{backend,frontend,docker,scripts}

# Backend
mkdir -p recollection/backend/{services,repositories,use_cases,domain,utils}
touch recollection/backend/{__init__.py,main.py,config.py}
touch recollection/backend/services/{ocr_tpu.py,embedding.py,screenshot.py}
touch recollection/backend/repositories/{libsql_repo.py,minio_repo.py}
touch recollection/backend/use_cases/{capture.py,search.py}
touch recollection/backend/domain/{entities.py,commands.py,events.py}
touch recollection/backend/utils/{image_utils.py,time_utils.py}

# Frontend
mkdir -p recollection/frontend/{public,src/{components,hooks,services}}
touch recollection/frontend/public/{index.html,styles.css}
touch recollection/frontend/src/{App.jsx,main.js}
touch recollection/frontend/src/components/{Timeline.jsx,Search.jsx}
touch recollection/frontend/src/hooks/useOffline.js
touch recollection/frontend/src/services/{api.js,storage.js}
touch recollection/frontend/package.json

# Docker
touch recollection/docker/{Dockerfile,docker-compose.yml}

# Scripts
touch recollection/scripts/{init_minio.sh,build_tpu_models.sh}

# Environment file
touch recollection/.env

# Add content to backend files
cat <<EOL > recollection/backend/main.py
from fastapi import FastAPI, Depends
from backend.services.screenshot import ScreenshotService
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from backend.domain.commands import CaptureScreenshotCommand
from backend.domain.entities import Screenshot

app = FastAPI()

# Dependency injection
def get_screenshot_service():
    return ScreenshotService(
        db_repo=LibSQLRepository(),
        storage_repo=MinIORepository()
    )

@app.post("/capture")
async def capture_screenshot(service: ScreenshotService = Depends(get_screenshot_service)):
    command = CaptureScreenshotCommand()
    screenshot = await service.execute(command)
    return {"status": "success", "screenshot": screenshot}

@app.get("/timeline")
async def get_timeline(service: ScreenshotService = Depends(get_screenshot_service)):
    screenshots = await service.get_timeline()
    return {"screenshots": screenshots}
EOL

cat <<EOL > recollection/backend/config.py
import os
from libsql_client import Client
from minio import Minio

def get_libsql_client():
    return Client(
        url=os.getenv("LIBSQL_URL", "http://localhost:8080"),
        auth_token=os.getenv("LIBSQL_TOKEN", "")
    )

def get_minio_client():
    return Minio(
        os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )
EOL

cat <<EOL > recollection/backend/services/ocr_tpu.py
import numpy as np
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter

class CoralOCR:
    def __init__(self):
        self.interpreter = make_interpreter("backend/models/ocr_edgetpu.tflite")
        self.interpreter.allocate_tensors()

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        # Resize and normalize image for TPU
        return image

    def extract_text(self, image: np.ndarray) -> str:
        input_tensor = self.preprocess_image(image)
        common.set_input(self.interpreter, input_tensor)
        self.interpreter.invoke()
        return self.postprocess_output(
            common.output_tensor(self.interpreter, 0)
        )

    def postprocess_output(self, output: np.ndarray) -> str:
        # Convert model output to text
        return "extracted text"
EOL

cat <<EOL > recollection/backend/services/embedding.py
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def compute_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text)
EOL

cat <<EOL > recollection/backend/services/screenshot.py
import time
import numpy as np
from PIL import Image
from backend.domain.entities import Screenshot
from backend.repositories.libsql_repo import LibSQLRepository
from backend.repositories.minio_repo import MinIORepository
from backend.services.ocr_tpu import CoralOCR
from backend.services.embedding import EmbeddingService

class ScreenshotService:
    def __init__(self, db_repo: LibSQLRepository, storage_repo: MinIORepository):
        self.db_repo = db_repo
        self.storage_repo = storage_repo
        self.ocr = CoralOCR()
        self.embedding = EmbeddingService()

    async def capture(self) -> Screenshot:
        # Simulate screenshot capture
        image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        timestamp = int(time.time())
        text = self.ocr.extract_text(image)
        embedding = self.embedding.compute_embedding(text)

        # Save to storage
        image_path = f"{timestamp}.webp"
        self.storage_repo.save_image(image_path, image)

        # Save to database
        screenshot = Screenshot(
            timestamp=timestamp,
            text=text,
            embedding=embedding,
            image_path=image_path
        )
        await self.db_repo.save_screenshot(screenshot)
        return screenshot

    async def get_timeline(self) -> list[Screenshot]:
        return await self.db_repo.get_timeline()
EOL

cat <<EOL > recollection/backend/repositories/libsql_repo.py
from libsql_client import Client
from backend.domain.entities import Screenshot

class LibSQLRepository:
    def __init__(self):
        self.client = Client(url=os.getenv("LIBSQL_URL"))

    async def save_screenshot(self, screenshot: Screenshot) -> None:
        await self.client.execute(
            "INSERT INTO screenshots (timestamp, text, embedding, image_path) VALUES (?, ?, ?, ?)",
            [screenshot.timestamp, screenshot.text, screenshot.embedding.tobytes(), screenshot.image_path]
        )

    async def get_timeline(self) -> list[Screenshot]:
        result = await self.client.execute("SELECT * FROM screenshots ORDER BY timestamp DESC")
        return [Screenshot(**row) for row in result.rows]
EOL

cat <<EOL > recollection/backend/repositories/minio_repo.py
from minio import Minio
import numpy as np
from PIL import Image

class MinIORepository:
    def __init__(self):
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )

    def save_image(self, image_path: str, image: np.ndarray) -> None:
        image_pil = Image.fromarray(image)
        image_pil.save(image_path, format="WEBP")
        self.client.fput_object("screenshots", image_path, image_path)
EOL

cat <<EOL > recollection/backend/domain/entities.py
from dataclasses import dataclass
import numpy as np

@dataclass
class Screenshot:
    timestamp: int
    text: str
    embedding: np.ndarray
    image_path: str

@dataclass
class SearchResult:
    screenshot: Screenshot
    similarity_score: float
EOL

cat <<EOL > recollection/backend/domain/commands.py
from dataclasses import dataclass

@dataclass
class CaptureScreenshotCommand:
    pass

@dataclass
class SearchCommand:
    query: str
    threshold: float = 0.7
EOL

cat <<EOL > recollection/backend/domain/events.py
from dataclasses import dataclass
from backend.domain.entities import Screenshot, SearchResult

@dataclass
class ScreenshotCapturedEvent:
    screenshot: Screenshot

@dataclass
class SearchPerformedEvent:
    query: str
    results: list[SearchResult]
EOL

cat <<EOL > recollection/backend/utils/image_utils.py
import numpy as np

def preprocess_image(image: np.ndarray) -> np.ndarray:
    # Add preprocessing logic (e.g., resizing, normalization)
    return image
EOL

cat <<EOL > recollection/backend/utils/time_utils.py
import time

def get_current_timestamp() -> int:
    return int(time.time())
EOL

# Add content to frontend files
cat <<EOL > recollection/frontend/public/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>recollection</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <div id="root"></div>
  <script src="/src/main.js" type="module"></script>
</body>
</html>
EOL

cat <<EOL > recollection/frontend/public/styles.css
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}

#root {
  padding: 20px;
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.screenshot {
  background: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
EOL

cat <<EOL > recollection/frontend/src/App.jsx
import React, { useState, useEffect } from "react";
import Timeline from "./components/Timeline";
import { fetchTimeline } from "./services/api";

export default function App() {
  const [screenshots, setScreenshots] = useState([]);

  useEffect(() => {
    fetchTimeline().then(data => setScreenshots(data.screenshots));
  }, []);

  return (
    <div>
      <h1>recollection</h1>
      <Timeline screenshots={screenshots} />
    </div>
  );
}
EOL

cat <<EOL > recollection/frontend/src/components/Timeline.jsx
import React from "react";

export default function Timeline({ screenshots }) {
  return (
    <div className="timeline">
      {screenshots.map((screenshot, index) => (
        <div key={index} className="screenshot">
          <img src={`/images/${screenshot.image_path}`} alt="Screenshot" />
          <p>{screenshot.text}</p>
        </div>
      ))}
    </div>
  );
}
EOL

cat <<EOL > recollection/frontend/src/services/api.js
export async function fetchTimeline() {
  const response = await fetch("/timeline");
  return await response.json();
}

export async function captureScreenshot() {
  const response = await fetch("/capture", { method: "POST" });
  return await response.json();
}
EOL

cat <<EOL > recollection/frontend/src/services/storage.js
export async function saveToIndexedDB(key, data) {
  const db = await openDB("recollection", 1, {
    upgrade(db) {
      db.createObjectStore("screenshots");
    },
  });
  await db.put("screenshots", data, key);
}

export async function getFromIndexedDB(key) {
  const db = await openDB("recollection", 1);
  return await db.get("screenshots", key);
}
EOL

cat <<EOL > recollection/frontend/src/hooks/useOffline.js
import { useEffect, useState } from "react";

export function useOffline() {
  const [isOffline, setIsOffline] = useState(!navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return isOffline;
}
EOL

cat <<EOL > recollection/frontend/src/main.js
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

ReactDOM.render(<App />, document.getElementById("root"));
EOL

cat <<EOL > recollection/frontend/package.json
{
  "name": "recollection-frontend",
  "version": "1.0.0",
  "scripts": {
    "start": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "vite": "^4.0.0"
  }
}
EOL

# Add content to Docker files
cat <<EOL > recollection/docker/Dockerfile
# Backend
FROM python:3.11-slim-bookworm AS backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM node:18 AS frontend
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Final image
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /app/dist /app/frontend/dist
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

cat <<EOL > recollection/docker/docker-compose.yml
version: "3.8"
services:
  libsql-server:
    image: libsql/server:v0.24.0
    ports:
      - "8080:8080"
    volumes:
      - libsql-data:/data

  minio:
    image: minio/minio:RELEASE.2024-02-16T01-53-20Z
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: recollection
      MINIO_ROOT_PASSWORD: strongpassword
    volumes:
      - minio-data:/data

  recollection:
    build: .
    ports:
      - "8000:8000"
    devices:
      - "/dev/bus/usb:/dev/bus/usb"
    environment:
      - LIBSQL_URL=http://libsql-server:8080
      - MINIO_ENDPOINT=http://minio:9000
      - MINIO_ACCESS_KEY=recollection
      - MINIO_SECRET_KEY=strongpassword

volumes:
  libsql-data:
  minio-data:
EOL

# Add content to scripts
cat <<EOL > recollection/scripts/init_minio.sh
#!/bin/bash
mc alias set local http://localhost:9000 recollection strongpassword
mc mb local/screenshots
EOL

cat <<EOL > recollection/scripts/build_tpu_models.sh
#!/bin/bash
curl -LO https://github.com/google-coral/test_data/raw/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite
mv mobilenet_v2_1.0_224_quant_edgetpu.tflite backend/models/ocr_edgetpu.tflite
EOL

# Add content to .env
cat <<EOL > recollection/.env
LIBSQL_URL=http://libsql-server:8080
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=recollection
MINIO_SECRET_KEY=strongpassword
EOL

# Make scripts executable
chmod +x recollection/scripts/init_minio.sh
chmod +x recollection/scripts/build_tpu_models.sh

echo "Project structure and files created successfully!"
