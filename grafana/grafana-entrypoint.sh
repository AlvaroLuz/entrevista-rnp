#!/bin/sh
set -e

export INFLUX_TOKEN=$(cat ${INFLUX_TOKEN_FILE})

exec /run.sh
