'''
Test Telegram Webhook.

Copyright (C) 2023 Dr. Sergey Kolevatov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

from telegram import Update

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    MessageHandler,
    filters,
    CommandHandler,
    ContextTypes,
    ExtBot,
    TypeHandler,
)

from dataclasses import dataclass
from flask import Flask, request, Response
import os
import telegram
import ssl
import config
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

application = ApplicationBuilder().token(config.TOKEN).build()

async def handle_echo( update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    await update.message.reply_text( update.message.text )

echo_handler = MessageHandler( filters.TEXT & (~filters.COMMAND), handle_echo )
application.add_handler( echo_handler )

@app.route('/', methods=['POST'])
async def webhook():
    if request.headers.get('content-type') == 'application/json':
        async with application:
            update = Update.de_json( request.get_json( force = True ),application.bot )
            await application.process_update( update )
            return ( '', 204 )
    else:
        return ( 'Bad request', 400 )

if __name__ == '__main__':
    if config.IS_PROD:
        http_server = WSGIServer(('', config.PORT), app, keyfile=config.PRIVATE_KEY_PATH, certfile=config.CERTIFICATE_PATH )
        http_server.serve_forever()
    else:
        context = ssl.SSLContext()
        context.load_cert_chain( config.CERTIFICATE_PATH, config.PRIVATE_KEY_PATH )
        app.run( debug=True, host=config.LISTEN_IP, port=config.PORT, ssl_context=context )
