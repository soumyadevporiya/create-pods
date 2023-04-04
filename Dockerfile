FROM python:3.9
WORKDIR ./
COPY ./requirement.txt ./requirement.txt
RUN pip install -r requirement.txt
COPY ./create_pod.py ./create_pod.py
CMD ["python3","./create_pod.py"]