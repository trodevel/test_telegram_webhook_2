#!/bin/bash

HOST_URL=$1
HOST_PORT=$2
CERT=$3

[[ -z $HOST_URL ]]  && echo "ERROR: HOST_URL is not given" && exit 1
[[ -z $HOST_PORT ]] && echo "ERROR: HOST_PORT is not given" && exit 1
[[ -z $BOT_TOKEN ]] && echo "ERROR: BOT_TOKEN is not found in evironment" && exit 1

API="https://api.telegram.org/bot${BOT_TOKEN}/setWebhook"

P1="-F url=https://${HOST_URL}:${HOST_PORT}"

if [[ -n $CERT ]]
then
    P2="-F certificate=@$CERT"
fi

curl -v $P1 $P2 "$API"
