#!/usr/bin/env python
import threading, logging, time
import multiprocessing
import sys
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka import SimpleClient
from kafka.protocol.offset import OffsetRequest, OffsetResetStrategy
from kafka.common import OffsetRequestPayload

logging.basicConfig(
    #filename='/app/logs/consumer.log',
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.DEBUG
)
log = logging.getLogger("consumer")
log.debug("consumer start")


if __name__ == "__main__":
    log.debug("----------------------> consumer")
    topic = sys.argv[2]
    kafka = sys.argv[1]
    log.debug("topic: " + str(topic))
    log.debug("kafka: " + str(kafka))
    #main(topic,kafka)

    consumer = KafkaConsumer(bootstrap_servers=kafka + ':9092',
                             auto_offset_reset='earliest',
                             consumer_timeout_ms=1000)
    consumer.subscribe([topic])
    for message in consumer:
        log.debug("message: " + str(message.value))
    consumer.close()
    log.debug("<---------------------- consumer")
