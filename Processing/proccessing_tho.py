#/usr/bin/env python
# -*- coding:utf-8 -*

#dependencies
import pymongo
import re
from pymongo import MongoClient
from kafka import KafkaConsumer
import json
import sys
from termcolor import colored
import time

#ensure number parameters
if len(sys.argv)!=5:
        print(colored('Number of parameters does not fit $PROGRAMA $KAFKA_IP $KA
FKA_TOPIC $MONGO_IP $FICHERO_JSON','red'))
        exit(1)

print(colored(sys.argv[1],'green'))
print(colored(sys.argv[2],'green'))
print(colored(sys.argv[3],'green'))
print(colored(sys.argv[4],'green'))

#Kafka connection
consumer = KafkaConsumer(bootstrap_servers=sys.argv[1])
consumer.subscribe([sys.argv[2]])

#Mongo connection
client=MongoClient('mongodb://'+sys.argv[3])
db=client.tho.completemessages
db2 = client.tho.processed

#Open Json file (patrones)
with open (sys.argv[4]) as json_data:
        d=json.load(json_data)

print(len(d['patron']))
#reading messages and processing
while True:
        for message in consumer:
#               print ("Arriving messages")
#               print(message.value)
                #K = numero de patron evaluado
                k=0
                match=False
                while k<len(d['patron']) and match==False:
                        #Process message, clean and gather
                        elements=[]
                        m=re.match(r'%s' % d['patron'][k] , message.value, re.I
| re.M)

                        if m:
                                #Gather information in collection
                                print ("Patron matched")
                                match=True
                                i=0  #Element in array
                                #Si queremos guardar un elemento que no sea mape
ado el numero de mapeos sera menor que el numero de elementos en matching y en e
lements
                                j=0
                                #info = d['matching']
                                while i<len(d['matching'][k]):
                                        if d['elements'][k][i]=="0":
#                                               print(d['matching'][k][i])
#                                               print(m.group(j))
                                                elem = {d['matching'][k][i]:m.gr
oup(j)}
                                                j=j+1
                                        else:
                                                elem = {d['matching'][k][i]:d['e
lements'][k][i]}
                                        elements = elem.items() + elements
                                        i=i+1
                                db2.insert(dict(elements))
                        #Leemos el siguiente patron (si lo hay)
                        k=k+1

                db.insert({"message":message})
