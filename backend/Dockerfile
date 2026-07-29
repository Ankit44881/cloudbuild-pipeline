FROM python:3.10-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy requirements first (for efficient Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ONLY necessary application files (Avoids "COPY . ." security warning)
COPY app.py .

# Ownership change & switch user
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]