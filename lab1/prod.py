from confluent_kafka import Producer
import asyncio
import numpy as np
import datetime

TOPIC_NAME = "some_topic"

PARAMS = [{'type':'temp','name':'temp1','time':4,'start':10,'dist':'normal','mu':0,'sigma':2},
          {'type':'press','name':'press1','time':2,'start':740,'dist':'poisson','lambda':2},
          {'type':'temp','name':'temp2','time':3,'start':15,'dist':'uni','scale':5}]

producer = Producer({
        "bootstrap.servers": "localhost:9092"
    })

def get_new(x):
    if x['dist']=='normal':
        return x['start']+ np.random.normal(x['mu'],x['sigma'],1)
    elif x['dist']=='poisson':
        return x['start']+ np.random.poisson(x['lambda'],1)
    elif x['dist']=='uni':
        return x['start']+ np.random.random(1)*x['scale'] - x['scale']/2
    else:
        raise Exception('Unknown distribution %s' %x['dist'])


def pringls(x):
    s = get_new(x)
    producer.produce(TOPIC_NAME, value="%s %s %s %d" %(str(datetime.datetime.now()),x['type'],x['name'],s))
    return s
    

async def gg(x):
    while True:
        await asyncio.sleep(x['time'])
        x['start']=pringls(x)

async def main():
    await asyncio.gather(*map(gg,PARAMS))

asyncio.run(main())