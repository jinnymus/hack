import redis
import xxhash
import logging
from datetime import datetime as dt
from kafka import KafkaConsumer, KafkaProducer, KafkaClient, TopicPartition
import json
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
from confluent_kafka.avro.serializer import (SerializerError,  # noqa
                                             KeySerializerError,
                                             ValueSerializerError)
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
import time
import os
import datetime

config = {
    'kafka_server': 'kafka1',
    'kafka_port': '9092',
    'kafka_schema': 'kafka-schema-registry',
    'kafka_schema_port': '8081',
    'kafka_zoo': 'zoo1',
    'db_host': 'redis',
    'db_port': 6379,
    'db_id' : 1,
    'db_pwd': 'redis123',
    'topic' : 'ru.nis.idg.terminal.validData.smartFarm',
}

schemaSF = '''{
              "type":"record",
              "name":"Farming",
              "namespace":"nis.dev.validator.avro",
              "fields":[
                {
                  "name": "term_id",
                  "type": "long", 
                  "default" : "NONE"
                },
                {
                  "name": "time_platform",
                  "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                  }, 
                  "default" : "NONE"
                },
                {
                  "name": "time_device",
                  "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                  }, 
                  "default" : "NONE"
                },
                {
                  "name": "activity_info",
                  "type": "int", 
                  "default" : "NONE"
                },
                {
                  "name": "image",
                  "type": "string", 
                  "default" : "NONE"
                }
              ]
            }'''

rawData2 = {"term_id": 101, "time_platform": 1527685363267, "time_device": 1527685363266, "activity_info": 300 }


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('kafkaTest')
r = redis.StrictRedis(host=config.get('db_host'), port=config.get('db_port'), db=config.get('db_id'), password=config.get('db_pwd'))
consumer = KafkaConsumer(bootstrap_servers=config.get('kafka_server') + ":" + config.get('kafka_port'),
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=1000)
schema_registry = CachedSchemaRegistryClient(url='http://' + config.get('kafka_schema') + ':' + config.get('kafka_schema_port'))
serializer = MessageSerializer(schema_registry)
value_schema = avro.loads(schemaSF)
avroProducer = AvroProducer({
    'bootstrap.servers': config.get('kafka_server'),
    'schema.registry.url': 'http://' + config.get('kafka_schema') + ':' + config.get('kafka_schema_port'),
    'message.max.bytes': 15000000
}, default_value_schema=value_schema)

start_time = time.time()
#device_time_device = 1530523171000
#device_time_device_utc = datetime.fromtimestamp(int(device_time_device / 1000)).strftime('%Y-%m-%dT%H:%M:%SZ')




def insertValue(value):
    digest = xxhash.xxh64(str(value)).hexdigest()
    datet = dt.utcnow().strftime("%s")
    #print ("[insertValue] digest: " + str(digest) + " date: " + str(datet))
    r.set(digest,datet)

def getValue(value):
    digest = xxhash.xxh64(value).hexdigest()
    print ("[getValue] digest: " + str(digest) + " value: " + str(r.get(digest)))

def checkValue(value):
    digest = xxhash.xxh64(value).hexdigest()
    result = r.exists("av")
    print ("[checkValue] digest: " + str(digest) + " result: " + str(result))
    return result

def checkInsert(value):
    #print ("[checkInsert] value: " + str(value))
    digest = xxhash.xxh64(str(value)).hexdigest()
    result = r.exists(digest)
    if (result == 0):
        #print ("[checkInsert] digest: " + str(digest) + " not exist")
        insertValue(value)

def keys():
    keys = r.keys()
    vals = r.mget(keys)
    kv = zip(keys, vals)
    print (kv)

def keysCount():
    le = len(r.keys())
    print ("[keysCount] " + str(le))

def flush():
    r.flushdb()

def bgsave():
    r.bgsave()

def deleteKey(value):
    digest = xxhash.xxh64(value).hexdigest()
    r.delete(digest)

def generateMessagesBig():
    log.info("[generateMessagesBig] start")
    for i in xrange(10000):
        with open('file2.json') as f:
            data = json.load(f)
            data['term_id'] = i
            sendKafka(data)
        #sendKafka(rawData2)
    log.info("[generateMessagesBig] end")
    print("[generateMessagesBig] flush --- %s seconds ---" % (time.time() - start_time))
    avroProducer.flush()
    print("[generateMessagesBig] --- %s seconds ---" % (time.time() - start_time))

def create_topic(topic):

    '''

    Create topic

    '''
    import kafka

    client = kafka.KafkaClient(hosts=config.get('kafka_server') + ':' + config.get('kafka_port'))
    res = client.ensure_topic_exists(topic)
    return res

def list():

    '''

    Kafka list topics

    List exist topics

    '''
    log.debug("[KafkaDriver][list] list start")
    list = consumer.topics()
    for topic in list:
        log.debug("[KafkaDriver][list] topic: " + str(topic))
    log.debug("[KafkaDriver][list] topic: " + str(topic))

def generateMessagesSmall():
    '''

    Generate small messages

    '''
    log.info("[generateMessagesSmall] start")
    for i in xrange(10000):
        rawData2['term_id'] = i
        sendKafka(rawData2)
    log.info("[generateMessagesSmall] end")
    print("[generateMessagesSmall] flush --- %s seconds ---" % (time.time() - start_time))
    avroProducer.flush()
    print("[generateMessagesSmall] --- %s seconds ---" % (time.time() - start_time))


def sendKafka(msg):
    '''

    Send message to topic

    '''
    res = avroProducer.produce(topic=config.get('topic'), value=msg)
    log.debug("[KafkaDriver][send] produce result: " + str(res))
    #time.sleep(1)

def getMessages():
    '''

    Get messages from topic and send to redis

    '''
    log.info("[getMessages] start")

    partition = TopicPartition(config.get('topic'), 0)
    log.info("[getMessages] assign")
    consumer.assign([partition])
    consumer.seek_to_beginning(partition)
    log.info("[getMessages] seek_to_beginning")

    for msg in consumer:
        #message = serializer.decode_message(msg.value)
        #message = json.dumps(message, indent=4, sort_keys=True, default=outputJSON)
        #del message['term_id']
        #log.info("[KafkaDriver][read_from_offset] avro message: " + str(message))
        #ret = message
        #log.info("[getMessages] msg.serialized_value_size: " + str(msg.serialized_value_size) + " msg.offset: " + str(msg.offset) + " msg.checksum: " + str(msg.checksum))
        checkInsert(msg.value)
        #checkInsert(message)
    log.info('[getMessages] end')

def delete_topic(topic=None, server='zoo1'):

    '''

    Delete topic

    '''

    cmd = '/nis-test/bin/kafka_2.12-1.1.0/bin/kafka-topics.sh --delete --topic ' + topic + ' --zookeeper ' + server
    logging.debug('[KafkaDriver][delete_topic] cmd: ' + str(cmd))
    ret = os.system(cmd)
    logging.debug('[KafkaDriver][delete_topic] ret: ' + str(ret))
    #assert ret == 0
    return ret

def get_last_offset():

    '''

    Kafka get last offset

    Get last message offset

    '''

    tp = TopicPartition(config.get('topic'), 0)
    consumer.assign([tp])
    consumer.seek_to_end(tp)
    last_offset = consumer.position(tp)
    logging.info("[KafkaDriver][get_last_offset] last_offset: " + str(last_offset))
    #consumer.close(autocommit=False)

def testGetMessages():
    '''

    Testing get messages

    '''
    flush()
    getMessages()
    log.info("get keys")
    print("--- %s seconds ---" % (time.time() - start_time))
    keysCount()
    print("--- %s seconds ---" % (time.time() - start_time))
    get_last_offset()
    consumer.close()

def testGenerateMessages():
    '''

    Testing generating messages

    '''
    delete_topic(config.get('topic'))
    print("[generateMessagesSmall] --- %s seconds ---" % (time.time() - start_time))
    generateMessagesBig()
    print("[get_last_offset] --- %s seconds ---" % (time.time() - start_time))
    get_last_offset()


testGenerateMessages()
testGetMessages()
