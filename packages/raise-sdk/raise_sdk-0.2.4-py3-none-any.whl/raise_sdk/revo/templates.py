# -*- coding: utf-8 -*-
"""
    RAISE - RAI Certified Node API

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

PYTHON_3_8_DOCKERFILE_TEMPLATE = """
### Specify the base image, which is an official Python 3.8 image from Docker Hub.    
FROM python:3.8

### Copy files and directories to support the execution).
COPY ./ /tmp/

### Install the Python packages listed in the requirements.txt file.
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

### Create a new user named code_runner with a user ID of 9097.
RUN useradd -u 9097 code_runner

### Switch to the code_runner user.
USER code_runner:code_runner

### Set the working directory to /tmp.
WORKDIR /tmp

### Specify the command to run when the container starts.
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""