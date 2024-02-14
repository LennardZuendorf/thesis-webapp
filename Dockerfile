# standard Dockerfile to build a complete, working image of the webapp

# complete build based on clean python (slower)
FROM python:3.11.6

# build based on thesis base with dependencies (quicker) - for dev
#FROM thesis-base:0.2.0

# install dependencies and copy files into image folder
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install fastapi uvicorn
COPY . .

# display files in image folder (for debugging)
RUN ls --recursive .

# setting config and run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# build and run commands:
## docker build -t thesis:1.3.1 -f Dockerfile .
## docker run -d --name thesis -e HOSTING=local -p 8080:8080 thesis:1.3.1
