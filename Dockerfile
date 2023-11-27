# Standard Dockerfile to build image of the webapp

## complete build based on clean python (slower)
FROM python:3.11.6

## build based on python with dependencies (quicker)
# FROM thesis:0.1.6-base

# install dependencies and copy files
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install fastapi uvicorn
COPY . .

RUN ls --recursive .

# setting config and run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# build and run commands
## docker build -t thesis:0.1.6 -f Dockerfile-Light .
## docker run -d --name thesis -p 8080:8080 thesis:0.1.6-small