# Stage 1: Build Vue/Vite frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Run Python/Streamlit with the built frontend
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    dumb-init \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built frontend from stage 1
COPY --from=frontend-builder /app/dist ./dist

# Copy all application files
COPY . .

ENV STREAMLIT_RELEASE=1

EXPOSE 8501

ENTRYPOINT ["dumb-init", "--"]
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
