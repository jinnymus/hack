package com.hack.validator.listener;

import org.springframework.cloud.stream.annotation.StreamListener;
import org.springframework.cloud.stream.messaging.Processor;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class FileConsumer {

    //@KafkaListener(topics = Processor.INPUT)
    @StreamListener(value = Processor.INPUT)
    public void consume(String file) {
        System.out.println("Received: " + file);
    }


}
