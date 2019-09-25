package com.hack.validator.listener;

import com.hack.validator.model.File;
import org.springframework.cloud.stream.messaging.Processor;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class FileConsumer {

    @KafkaListener(topics = Processor.INPUT)
    public void consume(File file) {
        System.out.println("Received: " + file);
    }
}
