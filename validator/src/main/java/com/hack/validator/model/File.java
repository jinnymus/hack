package com.hack.validator.model;

import org.apache.avro.Schema;
import org.apache.avro.specific.SpecificRecordBase;

public class File extends SpecificRecordBase {

    private Long timePlatform;
    private Long timeDevice;
    private int activityInfo;
    private byte[] image;

    public Long getTimePlatform() {
        return timePlatform;
    }

    public File setTimePlatform(Long timePlatform) {
        this.timePlatform = timePlatform;
        return this;
    }

    public Long getTimeDevice() {
        return timeDevice;
    }

    public File setTimeDevice(Long timeDevice) {
        this.timeDevice = timeDevice;
        return this;
    }

    public int getActivityInfo() {
        return activityInfo;
    }

    public File setActivityInfo(int activityInfo) {
        this.activityInfo = activityInfo;
        return this;
    }

    public byte[] getImage() {
        return image;
    }

    public File setImage(byte[] image) {
        this.image = image;
        return this;
    }

    @Override
    public Schema getSchema() {
        return null;
    }

    @Override
    public Object get(int i) {
        return null;
    }

    @Override
    public void put(int i, Object o) {

    }

}