package org.liba2;

import net.openhft.hashing.LongHashFunction;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import java.util.Set;

public class Duplicator {

    // todo: redis
    // statistic : start, end, latency


    private static String redisHost;// = "localhost";
    private static Integer redisPort;// = 6379;

    //the jedis connection pool..
    private static JedisPool pool = null;

    public Duplicator() {
        try (InputStream is = getClass().getClassLoader().getResourceAsStream("property.properties")) {
            if (is == null) {
                throw new RuntimeException("Cannot find property file.");
            }
            Properties properties = new Properties();
            properties.load(is);

            redisHost = properties.getProperty("redis.host");
            redisPort = Integer.valueOf(properties.getProperty("redis.port"));
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }

        //configure our pool connection
        pool = new JedisPool(redisHost, redisPort);
    }


    public boolean isDuplicated(String message) {
        long startTime = System.nanoTime();
        long hash = getHash(message);
        long endTime = System.nanoTime();

        System.out.println("Time spend to hash calculating: " + getMicroSec(endTime - startTime));

        Jedis resource = pool.getResource();

        startTime = System.nanoTime();
        boolean bdIsEmpty = bdIsEmpty(hash, resource);
        endTime = System.nanoTime();

        System.out.println("Check duplicate in db: " + getMicroSec(endTime - startTime));

        if (bdIsEmpty) {
            startTime = System.nanoTime();
            writeInDb(hash, resource);
            endTime = System.nanoTime();
            System.out.println("Writing in db time: " + getMicroSec(endTime - startTime));

            resource.close();

            return true;
        }

        resource.close();
        return false;
    }

    private void writeInDb(long hash, Jedis resource) {
        resource.sadd(String.valueOf(hash), ".");
    }

    private boolean bdIsEmpty(long hash, Jedis resource) {
        Set<String> smembers = resource.smembers(String.valueOf(hash));
        return smembers.isEmpty();
    }

    private String getMicroSec(long diff) {
        return diff / 1000 + " microsecs";
    }

    private long getHash(String message) {
        return LongHashFunction.xx().hashChars(message);
    }
}
