#!/bin/bash

[[ -z $BOT_TOKEN ]] && echo "ERROR: BOT_TOKEN is not found in evironment" && exit 1

API="https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"

curl "$API"
