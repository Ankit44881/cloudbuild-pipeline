FROM python:3.10-slim

WORKDIR /app

# Non-root user create karo for Least-Privilege Security Principle
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ownership change to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]