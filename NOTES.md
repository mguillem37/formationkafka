

https://cloud.contentraven.com/confluent/landing
password2020

PS# TOOLS

kafkahq : monitoring cluster kafka

# TIPS

ATTENTION : 
   - si plusieurs producer sur le même TOPIC pas de garantie de l'ordre d'arrivée des messages (un des producer a pu faire un retry par exemple en cas de pb)

 un producer écrit toujours sur un leader / pas les followers
 un consumer lit toujours sur le leader / pas les followers
 ON NE LIT jAMAIS SUR LES REPLICATIONS

3 partitions à minima de replica => 3 brokers
1 leader et au moins un in-Sync (min in-synck à deux : le leader + une partition in-sync)
in-synck doit être à jour avec le leader au cas où...si pb les producers recevront des exceptions pour qu'il y en ai au moins deux partitions à jours


lors de la création d'un topic, les partitions sont réparties sur les différents brokers selon un round robin (une partition leader par broker pour un topic)

# CONFIG DOCKER docker-compose.yml

config à adapter pour ouvrir le port 9092 de kafka sur localhost avec le port 9093

  kafka:
    image: "confluentinc/cp-enterprise-kafka:5.3.0"
    hostname: kafka
    networks:
      - confluent
    ports:
      - 9092:9092
      - 9093:9093
    environment:
      KAFKA_BROKER_ID: 101
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka:9092, EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT, EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "false"
      KAFKA_DELETE_TOPIC_ENABLE: "true"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_METRIC_REPORTERS: "io.confluent.metrics.reporter.ConfluentMetricsReporter"
      CONFLUENT_METRICS_REPORTER_BOOTSTRAP_SERVERS: "kafka:9092"


# DOCKER command

$> docker-compose up -d
$> docker-compose ps
$> docker-compose logs kafka 
$> docker-compose exec tools bin/bash
root@tools:/# zookeeper-shell zookeeper:2181 ls /brokers/ids

$> docker-compose down -v


# KAFKA

 kafka-console-producer --broker-list kafka:9092 --topic vehicle-positions

 kafka-console-consumer \
 --bootstrap-server kafka:9092 \
 --from-beginning \
 --topic vehicle-positions


 kafka-console-producer \
 --broker-list kafka:9092 \
 --topic vehicle-positions
	



partitions
[TopicPartition{topic...rror=None}, TopicPartition{topic...rror=None}, TopicPartition{topic...rror=None}, TopicPartition{topic...rror=None}, TopicPartition{topic...rror=None}, TopicPartition{topic...rror=None}]
0:TopicPartition{topic=vehicle-positions,partition=0,offset=-1001,error=None}
error:None
offset:-1001
partition:0
topic:'vehicle-positions'
1:TopicPartition{topic=vehicle-positions,partition=1,offset=-1001,error=None}
2:TopicPartition{topic=vehicle-positions,partition=2,offset=-1001,error=None}
3:TopicPartition{topic=vehicle-positions,partition=3,offset=-1001,error=None}
4:TopicPartition{topic=vehicle-positions,partition=4,offset=-1001,error=None}
5:TopicPartition{topic=vehicle-positions,partition=5,offset=-1001,error=None}

# Registry

 kafka-avro-console-producer \
  --broker-list kafka:9092\
  --property schema.registry.url=schemaregistry1:8081 \
  --topic vehicle-positions-avro \
  --property value.schema="{\"namespace\": \"formation.kafka\",\"name\": \"value\",\"type\": \"record\",\"fields\" : [{\"name\" : \"name\",\"type\" : \"string\"}]}"

 curl -X GET -H "Content-Type: application/vnd.schemaregistry.v1+json" localhost:8081/subjects                                     
["vehicle-positions-avro-key","vehicle-positions-avro-value"]%      

curl -X GET -H "Content-Type: application/vnd.schemaregistry.v1+json" localhost:8081/subjects/vehicle-positions-avro-value/versions


curl -X POST \
 -H "Content-Type: application/vnd.schemaregistry.v1+json" \
 --data @avro-v1.json \
 localhost:8081/subjects/vehicle-positions-avro-value/versions

 avec avro-v1.json :
{
    "schema": "{\"type\":\"record\",\"namespace\":\"solution.model\", \"name\":\"foo\", \"fields\":[{\"name\":\"bar\",\"type\":\"string\"},{\"name\":\"baz\",\"type\":\"string\",\"default\":\"\"}]}"
}