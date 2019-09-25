package com.hack.validator;

import com.hack.validator.model.File;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.test.EmbeddedKafkaBroker;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.kafka.test.utils.KafkaTestUtils;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;

import java.util.Date;
import java.util.Map;

@ExtendWith(SpringExtension.class)
@EmbeddedKafka(topics = "file_topic")
class FileTopicTest {

    @Autowired
    private EmbeddedKafkaBroker embeddedKafkaBroker;
//    @Autowired
//    private KafkaTemplate<String, File> template;

    @Test
    void test() {
        Map<String, Object> params = KafkaTestUtils.senderProps(embeddedKafkaBroker.getBrokersAsString());
        KafkaTemplate<String, File> template = new KafkaTemplate<>(new DefaultKafkaProducerFactory<>(params));

        File data = new File();
        data.setTimeDevice(new Date().getTime());

        template.setDefaultTopic("file_topic");
        template.sendDefault(data);
    }
}
