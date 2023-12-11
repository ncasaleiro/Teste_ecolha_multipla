# Teste escolha multipla dinamico

Este é um projeto desenvolvido em Python por Nuno Casaleiro para preparar os alunos do básico para as provas de aferição.
Está construido de forma dinamica para o professor poder fazer vários testes sem ter de gerar executaveis de cada vez que pretende fazer um teste.

Pretende-se ainda adicionar segurança para poder ser usado como avaliação.
Pretende-se envio dinamico de configuração em vez ser por ficheiro para ficar ainda mais seguro e dinamico.
Pretende-se apartir do log recuperar o historico para caso indevidimente o fecho da aplicação. 

---

## Utilizador

### Estrutura de Pastas

O projeto está organizado da seguinte forma:

- **`conf/`**: Contém o ficheiro de configurações.
- **`img/`**: Armazena as imagens utilizadas no projeto.
- **`logs/`**:Armazena todas as insteraçoes com o utilizador.

### Configuração

Antes de utilizar o projeto, é necessário configurar o arquivo `config.json` localizado na pasta `src/`. Aqui está um exemplo de configuração e uma explicação de cada campo:

```json
{
    "AppName": "Ficha MAT Nuno Casaleiro",
    "Title": "FICHA DE MATEMÁTICA",
    "num_questions": 6,
    "questions": {
        "1": "A turma do 2A tem 24 alunos e vai fazer uma viagem à lua, claro que vai ter de ir num autocarro mágico.\n Mas há um problema, o autocarro tem apenas 6 lugares para passageiros.\n Quantas vezes vai o autocarro ter que repetir a viagem para levar toda a turma?\r\n",
        "2": "A fila tem quantos carros?",
        "3": "A Maria tem 2 notas de 10 euros",
        "4": "O João desenhou um triângulo ",
        "5": "Diz qual o valor em falta na sequência",
        "6": "Diz qual o valor em falta na sequência"
    },
    "images": {
        "1": "img/bus-magic-school-bus2.gif",
        "2": "img/homer.gif",
        "3": "img/bus-magic-school-bus2.gif",
        "4": "img/homer.gif",
        "5": "img/bus-magic-school-bus2.gif",
        "6": "img/homer.gif"
    },
    "answers": {
        "1": [3, 4, 5, 6],
        "2": [30, 40, 50, 60],
        "3": [300, 400, 500, 600],
        "4": [3000, 4000, 5000, 6000],
        "5": [30000, 40000, 50000, 60000],
        "6": [30, 40, 50, 60]
    },
    "Broker": {
        "url": "test.mosquitto.org",
        "port": 1883
    }
}
```

- **`AppName`**: Nome do aplicativo.
- **`Title`** : Título do projeto.
- **`num_questions`** : Número total de perguntas.
- **`questions`** : Perguntas associadas aos números.
* **`images`**: Caminho das imagens associadas às perguntas.
* **`answers`**: Respostas esperadas para cada pergunta.
* **`Broker`**: Configurações do serviço de broker.
<br/>
<br/>
---

## Professor
