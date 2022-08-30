# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . ./

# Port used by the API
EXPOSE 1993

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python3", "src/main.py"]