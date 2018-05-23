FROM python:2.7
ADD proccessing.py /
ADD proccessing_tho.py /
ADD patrones.json /
ADD patrones_tho.json /
RUN pip install pymongo
RUN pip install kafka-python
RUN pip install termcolor
CMD ["python", "proccessing_tho.py", "172.23.0.4:9092", "new", "172.23.0.5:27017", "patrones_tho.json"]