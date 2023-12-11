import json
import time
import csv
import os
from datetime import datetime
import paho.mqtt.client as mqtt

# Carregar configurações do arquivo JSON
with open("conf/config.json", "r", encoding="utf-8") as config_file:
    config_data = json.load(config_file)

num_questions = config_data["num_questions"]
correct_answers = config_data["answers"]
ResultFileName = config_data["ResultFileName"]
brokerURL = config_data['Broker']['url']
brokerPort = config_data['Broker']['port']
nome_arquivo='results/'+ResultFileName+'.csv'

max_retries = 5


def saveResult(Name,date,questions,totalRes,data):
    global nome_arquivo , max_retries

    folderName = "results"

    for _ in range(max_retries):   
        try:
            if not os.path.exists(folderName):
                os.makedirs(folderName)
        except Exception as e:
            print(f"Error Folder: {e}")
        
        try:
            if not os.path.isfile(nome_arquivo):
                with open(nome_arquivo, 'w', newline='') as arquivo:
                    writer = csv.writer(arquivo)
                    header = ["Nome", "Data", "Resultado"] + [f"Pergunta_{i+1}" for i in range(num_questions)]
                    writer.writerow(header)
        except Exception as e:
            print(f"Error FIlE HEADER : {e}")
        
        try:
            with open(nome_arquivo, 'a', newline='') as arquivo:
                writer = csv.writer(arquivo)
                row_data = [Name, date, round(totalRes, 2)] + [round(q, 2) for q in questions]
                writer.writerow(row_data)
                print(row_data)
                print("Dados escritos com sucesso!")
                nome_arquivo2='results/'+Name+date+'.txt'
                try:
                    with open(nome_arquivo2, 'w') as arquivo2:
                        json.dump(data, arquivo2, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"Erro: {e}")
                break  # Se chegou aqui, a escrita foi bem-sucedida, então
            
        except Exception as e:
            print(f"Erro ao escrever no CSV: {e}")
            time.sleep(1)  # Aguarda 1 segundo antes de tentar novamente

        


    else:
        print(f"Atenção: Não foi possível escrever no CSV após {max_retries} tentativas.")



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Turma2A/Solum/Responses")
    client.subscribe("Turma2A/Solum/logs")

def on_message_result(client, userdata, msg):
    global correct_answers, num_questions
    questions= []
    
    try:
        # Decodificar a mensagem JSON
        data = json.loads(msg.payload.decode('utf-8'))
        # print(data)
        Name=data['Name'][0]
        current_time = time.time()
        current_datetime = datetime.fromtimestamp(current_time)
        date = current_datetime.strftime("%Y-%m-%d__%H_%M_%S")
        # Comparar as respostas com as soluções
        questions=[]
        for i in range(1, num_questions+1):
            question_key = f"Question_{i}"
            answer_key = f"Answer_{i}"

           

            if question_key in data and answer_key in data:
                question = data[question_key][0]
                if data[answer_key] != None: 
                    user_answer = data[answer_key][0]

                    if user_answer == (correct_answers[str(i)][0]) :
                        questions.append((100/num_questions))
                    else :
                        questions.append(0)
                else :
                    questions.append(0)


        
        totalRes=sum(questions)

        saveResult(Name,date,questions,totalRes,data)

  

    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")


def on_message_logs(client, userdata, msg):
    print(msg.payload.decode('utf-8'))



client = mqtt.Client("professor1235")
client.on_connect = on_connect
topic1 = "Turma2A/Solum/Responses"
topic2 = "Turma2A/Solum/logs"
client.message_callback_add(topic1, on_message_result)
client.message_callback_add(topic2, on_message_logs)

# Substitua 'localhost' pelo endereço do seu broker MQTT
client.connect(brokerURL, brokerPort,60)

# Mantenha o programa em execução
client.loop_forever()