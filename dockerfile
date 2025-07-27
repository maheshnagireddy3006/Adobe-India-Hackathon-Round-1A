FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install PyMuPDF (fitz) and any other dependencies
RUN pip install --no-cache-dir pymupdf

# Copy all project files into the container
COPY . .

# Set the default command to run your main script
CMD ["python", "python.py"]