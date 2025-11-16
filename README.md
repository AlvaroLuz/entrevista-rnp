# Entrevista-RNP - Questão 1
Este repositório armazena a resolução das questões da entrevista para DevOps da RNP.
O código aqui presente implementa a resolução para a questão 1, que solicita uma aplicação dockerizada que realize uma série de consultas de latência, tempo de resposta e status HTTP da resposta. O código em questão foi elaborado em um sistema Linux Ubuntu 22.04.

## Estrutura básica do código 
A estrutura básica do código consiste das seguintes partes:

    agent/
        agent.py            --> script principal de consulta
        Dockerfile          --> montagem do container
        requirements.txt    --> requisitos da aplicação
    secrets/                --> credenciais das plataformas
    grafana/                --> configurações customizadas de consulta e dashboard
    docker-compose.yml      --> preparação de ambiente e containers

Ao executar o docker compose, serão criados três containers executando: 
- InfluxDB (banco de dados escolhido)
- Grafana (para realizar a montagem dos dashboards)
- um agente python (quem realiza os pings e envia os dados ao InfluxDB)

Abaixo pode-se observar um fluxograma básico do funcionamento do código. Nele, **agent.py**, realiza as consultas aos sites e grava os resultados relevantes no **InfluxDB**. Esses dados então são consultados pelo **Grafana** para exibir o Dashboard.

```mermaid
flowchart TD

    subgraph Agent["🟦 agent.py"]
        A1["ping_host(host)"]
        A2["check_http(host)"]
        A3["Latência, Status Code, Tempo de resposta"]
    end

    subgraph InfluxDB["🟩 InfluxDB 2.x"]
        B1["Bucket: home"]
        B2["Measurement: network_metrics"]
        B3["Fields: ping_latency_ms, http_response_time_ms, http_status_code"]
        B4["Tags: host"]
    end

    subgraph Grafana["🟧 Grafana"]
        C1["Realiza uma query 
        em Flux"]
        C2["Dashboard"]
        C3["Painel de Timeline do HTTP Status Code"]
        C4["Painéis de Série Temporal"]
        C5["Latência"]
        C6["RTT"]

    end
    subgraph Hosts["Internet"]
        D1["rnp.br"]
        D2["youtube.com"] 
        D3["google.com "]
    end
    Agent -->|Escreve os dados obtidos nas consultas no InfluxDB via client| InfluxDB
    Grafana -->|Lê via Flux| InfluxDB
    Hosts -->|Resposta| A3

    A1 -->|Ping| Hosts
    A2 -->|Consulta HTTP| Hosts


    C1 --> C2
    C2 --> C3
    C2 --> C4
    C4 --> C5
    C4 --> C6
```


## Execução 
### Prerequisitos:
Ter o Docker instalado e Docker Compose
### Subindo os serviços
Primeiramente clone o repositório e acesse o diretório do projeto:

    git clone https://github.com/AlvaroLuz/entrevista-rnp
    cd entrevista-rnp

e inicialize o diretório *secrets/* com o *init_secrets.sh*

    sudo chmod +x init_secrets.sh #garantindo a permissao de execucao se nao houver
    sudo ./init_secrets.sh

após isso, simplesmente suba os containers
    
    docker compose up -d

## Visualizando o Dashboard no Grafana
Após subir os containers, é esperado que o Grafana esteja rodando na porta 3000, portanto é apenas necessário acessar o link http://localhost:3000
    
**O perfil de Administrador do Grafana já estará configurado**, assim, as credenciais são definidas automaticamente e a senha é armazenada na pasta secrets usando o script de inicialização. 

> **username padrão: admin**

**para visualizar a senha**, apenas execute dentro da pasta do projeto:

    cat ./secrets/grafana_admin_password

uma vez logado no Grafana, entre na aba de **Dashboards**, nela estará configurado um Dashboard por padrão exibindo os dados coletados e armazenados no InfluxDB.

**OBS: na primeira vez que o Dashboard for carregado, será necessário clicar em editar e dar refresh em cada uma das consultas individualmente, devido a um bug do Grafana.**