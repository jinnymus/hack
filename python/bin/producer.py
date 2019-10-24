#!/usr/bin/env python
import threading, logging, time
import multiprocessing
import sys
from kafka import KafkaConsumer, KafkaProducer, KafkaClient

logging.basicConfig(
    #filename='/app/logs/consumer.log',
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.DEBUG
)
log = logging.getLogger("producer")
log.debug("producer start")


if __name__ == "__main__":
    logging.basicConfig(
        #filename='/app/logs/producer.log',
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.DEBUG
    )
    logging.debug("----------------------> producer")
    topic = sys.argv[2]
    kafka = sys.argv[1]
    logging.debug("topic: " + str(topic))
    logging.debug("kafka: " + str(kafka))
    #main(topic,kafka)
    #producer = KafkaProducer(bootstrap_servers=kafka + ':9092')
    producer = KafkaProducer()
    # i = 1
    producer.send(topic, b"{'string2':'string'}")
    producer.close()
    logging.debug("<---------------------- producer")


