# Entrevista-RNP - Questão 1
Este repositório armazena a resolução das questões da entrevista para DevOps da RNP.
O código aqui presente implementa a resolução para a questão 1, que solicita uma aplicação dockerizada que realize uma série de consultas de latência, tempo de resposta e status HTTP da resposta.  

Os dados obtidos são armazenados em um banco de dados InfluxDB, que então são acessados via pelo Grafana para a montagem dos dashboards.

## Prerequisitos:
Ter o Docker instalado e Docker Compose

## Execução 
Primeiramente clone o repositório e acesse a pasta do projeto:

    git clone https://github.com/AlvaroLuz/entrevista-rnp
    cd entrevista-rnp


após isso, simplesmente suba os containers
    
    docker compose up -d

