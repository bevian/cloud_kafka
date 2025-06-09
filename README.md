# Projeto de Plataforma de Fluxo de Dados Integrada

## Visão Geral
Sistema completo de monitoramento ambiental com ESP32, sensor DHT22, Mosquitto, Kafka e MongoDB. Coleta dados de temperatura/umidade, transmite via MQTT, processa com Kafka e armazena no MongoDB para visualização.

## Hardware Necessário
- **ESP32-WROOM-32**
- **Sensor DHT22**
- Protoboard e jumpers
- Fonte USB 5V

## Conexões Físicas
| Pino ESP32 | Conexão DHT22 |
|------------|---------------|
| 3.3V       | VCC           |
| GND        | GND           |
| GPIO4      | DATA          |

## Software
- Arduino IDE (para ESP32)
- Mosquitto MQTT Broker
- Apache Kafka
- MongoDB
- Python 3.8+ (para consumidor Kafka)

## Fluxo de Dados

![Diagrama de Fluxo](Diagrama.png)

```plaintext
ESP32 (simula temperatura e umidade)
       ↓ MQTT
Mosquitto Broker local (localhost:1883)
       ↓
Tópico MQTT: sensor_temperatura
       ↓
Python (MQTT → Kafka)
       ↓
Kafka local (localhost:9092)
       ↓
Python Consumer Kafka
       ↓
MongoDB local (localhost:27017 → banco: COMP_NUVEM, coleção: dadosTempTopico)
```

## Como Executar o Projeto

1. **ESP32:**
   - Suba o código `configesp32.ino` na sua placa
   - Utilize as credenciais de conexão para a sua rede
   - Verifique o Serial Monitor para confirmar a publicação MQTT

2. **Mosquitto Broker:**
   - Instale o Mosquitto localmente:
     ```bash
     sudo apt install mosquitto mosquitto-clients
     ```
   - Configure o Mosquitto por meio do arquivo `mosquitto.conf` presente no repositório `mosquitto/config/mosquitto.conf` da instalação.
   - Inicie o serviço:
     ```bash
     mosquitto
     ```

3. **Kafka Local:**
   - Instale e inicie o Kafka e o Zookeeper localmente
   - Crie o tópico:
     ```bash
     kafka-topics.sh --create --topic sensor_temperatura --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
     ```

4. **MQTT → Kafka:**
   - Execute o script Python que lê do MQTT e publica no Kafka:
     ```bash
     python mqtt_kafka.py
     ```

5. **Kafka → MongoDB:**
   - Execute o script que consome do Kafka e insere no MongoDB:
     ```bash
     python kafka_mongo.py
     ```

6. **MongoDB:**
   - Verifique se o MongoDB está rodando localmente:
     ```bash
     mongod
     ```
   - Use `mongosh` ou MongoDB Compass para visualizar os dados

---

## Autores

- Beatriz Vieira – vieira.beatriz@usp.br
- Eduardo Garcia de Gaspari Valdejão – eduardo.gdgv@usp.br
- Gabriel Vasconcelos de Arruda – gabrielvascoarruda@usp.br
