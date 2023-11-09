import json
from paho.mqtt import client as mqtt_client
import time

#parametros de conexão TCP
host = 'test.mosquitto.org'
#host = 'localhost'
port = 1883
topic = 'Liberato/iotTro/44xx/data'
#topic = 'teste'
client_id = '20000216'
topic_ack = 'Liberato/iotTro/44xx/rply/20000216'
#topic_ack = 'teste/ack'

def is_json(str):
    try:
        json.loads(str)
    except ValueError as e:
        return False
    return True

# função pra construir a resposta em JSON
def ack(mesg):
    mesg['seq'] = int(mesg['seq']) + 800000
    mesg['nome'] = "Enzo Immig"
    mesg['turma'] = 4411
    if mesg['tempExt']['valor'] > mesg['tempExt']['valor']:
        mesg['climatizado'] = "SIM"
    else:
        mesg['climatizado'] = "NAO"
    del mesg['tempExt']
    del mesg['tempInt']
    del mesg['umidade']

    print("Resposta enviada!")
    return json.dumps(mesg)

#função para estabelecer conexao com o broker
def connect_mqtt():
    # sobrecarga (n lembro se é esse o nome, mas é reescrita de uma função da biblioteca)
    # é o callback da conexao do cliente com o broke, rc é o código de status
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Cria o objeto do cliente
    client = mqtt_client.Client(client_id)

    # atribuindo a função de callback criada ao objeto
    client.on_connect = on_connect

    # faz a conexão com o broker
    client.connect(host, port)

    return client

# funcao para fazer uma inscrição no broker
def subscribe(client: mqtt_client):
    # redefinição da função de callback de quando recebe uma mensagem
    def on_message(client, userdata, msg):
        if(is_json(msg.payload.decode())): # verifica se a string recebida é um JSON
            #print(json.loads(msg.payload.decode()))
            msg_dicpy = json.loads(msg.payload.decode()) # decode from binary e converte para dicionario python
            print(f"Matricula recebida é ({msg_dicpy['matricula']})")

            if(msg_dicpy['matricula'] == 20000216):
            #   print(f"Minha matricula foi recebida ({msg_dicpy['matricula']})")
                # ack
                client.publish(topic_ack, ack(msg_dicpy))
            else:
                print("Nao é minha vez!")

    # faz efetivamente a inscrição no tópico
    client.subscribe(topic)
    # define que a função de callback a ser utilizada é a criada acima
    client.on_message = on_message

def run():
    # criar um objeto de cliente
    client = connect_mqtt()

    subscribe(client) # publica 
    client.loop_forever()

if __name__ == '__main__':
    run()