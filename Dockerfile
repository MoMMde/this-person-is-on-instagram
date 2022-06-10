FROM python:latest
ADD src /
ADD requirements.txt /
RUN python3 -m pip install -r requirements.txt
CMD [ "python", "src/main.py" ]
