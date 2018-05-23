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
	print(colored('El numero de parametros no coincide $PROGRAMA $KAFKA_IP $KAFKA_TOPIC $MONGO_IP $FICHERO_JSON','red'))
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
db=client.tfg.pruebas

#JSON file open
with open (sys.argv[4]) as json_data:
	d=json.load(json_data)

k=0
while k < len(d['patron']):
	print(d['patron'][k])
	k=k+1

#reading messages and processing
while True: 
	for message in consumer:
		print ("Llegan mensajes")
		k=0
		match=False
		while k <len(d['patron']) and match==False:
			#Process message, clean and gather
			elements=[]
			m=re.match(r'%s' % d['patron'][k] , message.value, re.I | re.M)

			if m: 
				#Gather information in collection
				match=True
				i=0
				j=1
				#info = d['matching]
				while i <len(d['matching'][k]):
					if d['elements'][k][i]=="0":
						if d['matching'][k][i]=='status':
							elem={d['matching'][k][i]:int(m.group(j))}
						else:
							if d['matching'][k][i]=='UnixTimeStamp':
								fecha = time.ctime(int(m.group(j))/1000)
								separate = fecha.split()
								dia = separate[2]
								mes = separate[1]
								ano = separate[4]
								hora = separate[3]
								data = dia + mes + ano
								elem = {d['matching'][k][i]:m.group(j),"dia":dia, "mes":mes, "ano":ano, "hora":hora, "date":data}
							else:
								elem = {d['matching'][k][i]:m.group(j)}
						elements = elem.items() + elements
						j=j+1
					else:
						if d['matching'][k][i]=='status':
							elem={d['matching'][k][i]:int(m.group(j))}
						else:
							if d['matching'][k][i]=='UnixTimeStamp':
								fecha = time.ctime(int(m.group(j))/1000)
								separate=fecha.split()
								dia = separate[2]
								mes = separate[1]
								ano = separate[4]
								hora = separate[3]
								data = dia + mes + ano
								elem = {d['matching'][k][i]:m.group(j),"dia":dia, "mes":mes, "ano":ano, "hora":hora, "date":data}
							else:
								elem = {d['matching'][k][i]:d['elements'][1][i]}
						elements=elem.items() + elements
					i=i+1
				print(elements)
				db.insert(dict(elements))
			k=k+1