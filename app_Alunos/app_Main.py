import threading
import time
import json
import uuid
import sys
import paho.mqtt.client as mqtt
from interface import window , sg


# Carregar configurações do arquivo JSON
with open("conf/config.json", "r") as config_file:
    config_data = json.load(config_file)

num_questions = config_data["num_questions"]
images_load = config_data["images"]
questions_config=config_data["questions"]
answers_config = config_data["answers"]
appName = config_data["AppName"]
appTitle = config_data['Title']
brokerURL = config_data['Broker']['url']
brokerPort = config_data['Broker']['port']
response = [None] * (num_questions+1)

logIndex=0
# Criar dicionário de respostas
resp_dict = {"Name": []}
for i in range(1, num_questions + 1):
    resp_dict[f"Question_{i}"] = []
    resp_dict[f"Answer_{i}"] = []

question = 0


window.TKroot.title(appName)
window['-text-Title'].update(appTitle)

     

def salvar_log_json(dados, nome_arquivo='log/log.json'):
    global brokerPort, brokerURL
    timestamp = int(time.time())
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
    dados['Timestamp'] = timestamp
    dados['MAC_Address'] = mac_address
    with open(nome_arquivo, 'a+') as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)
    try:
    # Publish data to MQTT broker
        if 'FinalAnswer' in dados :
            topic = "Turma2A/Solum/Responses"
        else :
            topic = "Turma2A/Solum/logs"


        client = mqtt.Client(mac_address)
        client.connect(brokerURL, brokerPort)
        # comment after dev end
        print(json.dumps(dados,ensure_ascii=False))
        
        client.publish(topic, json.dumps(dados,ensure_ascii=False))
        client.disconnect()

    except (TypeError, IndexError) as e:
        print(f"Error ligar MQTT :  {e}")



def main():
    global question, response, questions_config, answers_config , images_load , num_questions

    while True:
        event, values = window.read(timeout=25)

        # ... (restante do loop de eventos)

        if event == sg.WIN_CLOSED or event == '-button-entregar':
        # Preencher o dicionário de respostas de acordo com as configurações
            resp_dict["Name"].append(values[0])
            resp_dict["FinalAnswer"]=True
            for i in range(1, num_questions + 1):
                try:
                    selected_option = response[i]
                    if selected_option is not None:                        
                        resp_dict[f"Question_{i}"].append((questions_config[str(i)]))
                        resp_dict[f"Answer_{i}"].append(answers_config[str(i)][selected_option - 1])
                    else:
                        resp_dict[f"Question_{i}"].append((questions_config[str(i)]))
                        resp_dict[f"Answer_{i}"]=None
                except (TypeError, IndexError) as e:
                    print(f"Erro ao processar resposta da questão {i}: {e}")
                    resp_dict[f"Question_{i}"].append((questions_config[str(i)]))
                    resp_dict[f"Answer_{i}"]=None
            salvar_log_json(resp_dict)
            # print(resp_dict)
            break
        elif  event == '-button-ok':       
            # print('You entered name :', values[0])
            # print('Start ')
            question=1
            window['-text-Title'].update(f"Pergunta {question}:")
            logAppend={"Question":1, "Name":[]}
            logAppend["Name"].append(values[0])
            salvar_log_json(logAppend)  
            window['-text-body'].update(questions_config[str(question)], visible=True)
            window['-button-ok'].update(visible=False)
            window['-button-Next1'].update(visible=True)
            window['-button-resp1'].update(text=str(answers_config[str(question)][0]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp2'].update(text=str(answers_config[str(question)][1]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp3'].update(text=str(answers_config[str(question)][2]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp4'].update(text=str(answers_config[str(question)][3]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released 

        elif  event == '-button-Next1' : 
            question=question+1 
            if question == num_questions:
                window['-text-End'].update(visible=True)
                window['-button-entregar'].update(visible=True)
            if question > num_questions:
                question=1
            
            window['-text-Title'].update(f"Pergunta {question}:")
            logAppend={"Question":question, "Name":[]}
            logAppend["Name"].append(values[0])
            salvar_log_json(logAppend)   
            window['-text-body'].update(questions_config[str(question)], visible=True)
            window['-button-Next1'].update(visible=True)
            match  response[question]:
                case 1:                
                    window['-button-resp1'].update(text=str(answers_config[str(question)][0]), visible=True, button_color=('#8c8c8c', 'white'))  # Restore button color when released
                    window['-button-resp2'].update(text=str(answers_config[str(question)][1]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp3'].update(text=str(answers_config[str(question)][2]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp4'].update(text=str(answers_config[str(question)][3]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-text-End'].update(visible=True)
                    window['-button-entregar'].update(visible=True)
                case 2:
                    window['-button-resp1'].update(text=str(answers_config[str(question)][0]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp2'].update(text=str(answers_config[str(question)][1]), visible=True, button_color=('#8c8c8c', 'white'))  # Restore button color when released
                    window['-button-resp3'].update(text=str(answers_config[str(question)][2]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp4'].update(text=str(answers_config[str(question)][3]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released 

                case 3:
                    window['-button-resp1'].update(text=str(answers_config[str(question)][0]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp2'].update(text=str(answers_config[str(question)][1]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp3'].update(text=str(answers_config[str(question)][2]), visible=True, button_color=('#8c8c8c', 'white'))  # Restore button color when released
                    window['-button-resp4'].update(text=str(answers_config[str(question)][3]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released 

                case 4:
                    window['-button-resp1'].update(text=str(answers_config[str(question)][0]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp2'].update(text=str(answers_config[str(question)][1]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp3'].update(text=str(answers_config[str(question)][2]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp4'].update(text=str(answers_config[str(question)][3]), visible=True, button_color=('#8c8c8c', 'white'))  # Restore button color when released 

                case _:
                    window['-button-resp1'].update(text=str(answers_config[str(question)][0]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp2'].update(text=str(answers_config[str(question)][1]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp3'].update(text=str(answers_config[str(question)][2]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released
                    window['-button-resp4'].update(text=str(answers_config[str(question)][3]), visible=True, button_color=('white', '#672f2f'))  # Restore button color when released 




        elif event == '-button-resp1' :
            response[question]=1
            value= (answers_config[str(question)][1 - 1])                      
            # print("question: ",question ," ; response: 1 ; value:",value)
            logAppend={"Question":question, "Response":value, "Name":[]}
            logAppend["Name"].append(values[0])
            salvar_log_json(logAppend)      
            window['-button-resp1'].update(button_color=('#8c8c8c', 'white'))  # Restore button color when released
            window['-button-resp2'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp3'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp4'].update(button_color=('white', '#672f2f'))   # Restore button color when released

        elif event == '-button-resp2'  :
            response[question]=2
            value= (answers_config[str(question)][2 - 1])                      
            # print("question: ",question ," ; response: 2 ; value:",value)
            logAppend={"Question":question, "Response":value, "Name":[]}
            logAppend["Name"].append(values[0])
            salvar_log_json(logAppend)      
            window['-button-resp1'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp2'].update(button_color=('#8c8c8c', 'white'))  # Restore button color when released
            window['-button-resp3'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp4'].update(button_color=('white', '#672f2f'))   # Restore button color when released

        elif event == '-button-resp3'  :
            response[question]=3   
            value= (answers_config[str(question)][3 - 1])                      
            # print("question: ",question ," ; response: 3 ; value:",value)
            logAppend={"Question":question, "Response":value, "Name":[]}
            logAppend["Name"].append(values[0])
            salvar_log_json(logAppend)      
            window['-button-resp1'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp2'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp3'].update(button_color=('#8c8c8c', 'white'))  # Restore button color when released
            window['-button-resp4'].update(button_color=('white', '#672f2f'))   # Restore button color when released

        elif event == '-button-resp4'  :
            response[question]=4     
            value= (answers_config[str(question)][4 - 1])                      
            # print("question: ",question ," ; response: 4 ; value:",value)
            logAppend={"Question":question, "Response":value, "Name":[]}
            logAppend["Name"].append(values[0])
            salvar_log_json(logAppend)      
            window['-button-resp1'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp2'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp3'].update(button_color=('white', '#672f2f'))  # Restore button color when released
            window['-button-resp4'].update(button_color=('#8c8c8c', 'white'))  # Restore button color when released

        if question ==0:
            window.Element('-image').UpdateAnimation(r'img/bus-magic-school-bus.gif',  time_between_frames= 150)
        else:        
            window.Element('-image').UpdateAnimation(images_load[str(question)],  time_between_frames= 150)






if __name__ == "__main__":
    main()

