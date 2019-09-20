#!/usr/bin/env bash

curl -X POST -H "Content-Type: application/json" --data '{"name": "test54", "config": {"connector.class":"io.confluent.connect.jdbc.JdbcSinkConnector", "tasks.max":"1", "topics":"ru.nis.idg.terminal.validData.smartFarm","connection.url": "jdbc:postgresql://sql:5432/sodmtd?user=postgres&password=pg123QWEasd", "auto.create":"true", "table.name.format": "tbl_smart_farm"}}' http://kafka-connect:8083/connectors
