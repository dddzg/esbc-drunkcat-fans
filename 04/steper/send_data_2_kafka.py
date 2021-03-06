# -*- coding: utf-8 -*-


from kafka import KafkaProducer
from kafka.errors import KafkaError

import random 
from datetime import datetime

from hdfs.client import Client
client = Client("http://master:50070")
hdfs_path = "/test/jcn.dat"

user_per_second = 20000

def random_index(rate):
    """随机变量的概率函数"""
    start = 0
    randnum = random.randint(1, sum(rate))
    for index, item in enumerate(rate):
        start += item
        if randnum <= start:
            break
    return index

producer = KafkaProducer(bootstrap_servers='116.56.136.57:9092')

def on_send_success(record_metadata):
    print('Send successfully!!!!')
    print('topic: ',record_metadata.topic)
    print('partition: ',record_metadata.partition)
    print('offset: ',record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)
    # handle exception
    
nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(nowtime)

while(1):
    if( nowtime != datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rate = random.uniform(0, 100)
        for i in range(0,user_per_second):
        	data = bytes(nowtime+";"+"{:0>8d}".format(random.randint(0,1000000))+";"+str(random_index([rate,100-rate])))
        	producer.send('dzg', data).add_callback(on_send_success).add_errback(on_send_error)
        	client.write(hdfs_path, data,overwrite=False,append=True)
