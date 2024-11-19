# base python image
FROM python:3.11.10-slim

# Upgrade Pip before installing requirements
RUN python -m pip install --upgrade pip

# Install Requirements
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy Source Files
COPY . .

# Exposing the port
EXPOSE 8000:8000

# start app with
# python -m uvicorn main:root --reload
CMD [ "fastapi", "run"]

# build with:
#   docker build . -t python-api-gcp
# run with:
#   docker run python-api-gcp