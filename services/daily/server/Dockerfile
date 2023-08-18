# Python 3.10 image
FROM python:3.10

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY *.py ./server/

# Run the application
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
