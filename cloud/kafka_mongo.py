from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# ====== CONFIGURAÇÕES ======

# Kafka
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'sensor_temperatura'

# MongoDB
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'COMP_NUVEM'
COLLECTION_NAME = 'dadosTempTopico'

# ====== CONEXÃO COM MONGODB ======
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
colecao = db[COLLECTION_NAME]

# ====== CONEXÃO COM KAFKA ======
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='grupo_teste',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"✅ Conectado ao Kafka no tópico '{KAFKA_TOPIC}'")
print("🟢 Aguardando mensagens...\n")

# ====== CONSUMO E INSERÇÃO ======
try:
    for mensagem in consumer:
        dados = mensagem.value
        print(f"📥 Mensagem Kafka: {dados}")

        # Insere no MongoDB
        colecao.insert_one(dados)
        print("✅ Inserido no MongoDB com sucesso\n")

except KeyboardInterrupt:
    print("⛔ Interrompido pelo usuário.")
finally:
    consumer.close()
    mongo_client.close()
    print("🛑 Conexões encerradas.")
