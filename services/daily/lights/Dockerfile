# Python 3.10 image
FROM python:3.10

WORKDIR /app

# make it a NZ timezone
RUN ln -sf /usr/share/zoneinfo/Pacific/Auckland /etc/localtime

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY src/*.py .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
