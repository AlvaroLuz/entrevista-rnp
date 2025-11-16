#!/bin/sh
set -e

# Carregando a variavel de ambiente INFLUX_TOKEN a partir do arquivo de segredo
# usado no datasources.yaml do grafana para conectar no InfluxDB
export INFLUX_TOKEN=$(cat $INFLUX_TOKEN_FILE)

exec /run.sh
