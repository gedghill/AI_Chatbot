# Use Python 3.10 image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    supervisor \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK data
RUN python -m nltk.downloader punkt wordnet stopwords -d /root/nltk_data

# Copy app code
COPY ./app /app

# Create log directory
RUN mkdir -p /app/logs/fastapi

# Copy supervisord template configuration
COPY supervisord.template.conf /etc/supervisor/supervisord.template.conf

# Generate supervisord configuration
RUN NPROC=$(nproc) && sed "s/{NPROC}/$NPROC/g" /etc/supervisor/supervisord.template.conf > /etc/supervisor/supervisord.conf

# Expose the backend port
EXPOSE 5000

# Run supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
