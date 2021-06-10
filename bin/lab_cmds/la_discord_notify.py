from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import site
import sys
import json

site.addsitedir('/opt/opencue/CURRENT/cuegui/venv/lib/python2.7/site-packages')
os.environ['PATH'] = '/opt/opencue/CURRENT/cuegui/venv/bin' + os.pathsep + os.environ['PATH']

from discord_webhook import DiscordWebhook

json_file = open('/opt/opencue/discord_data.json', 'r')
json_data = json.load(json_file)
json_file.close()

webhook = json_data['webhook']

user    = sys.argv[1]
message = sys.argv[2]

try:
    user = json_data['users'][user]
except:
    pass

message = '%s - %s.' % (user, message)

webhook = DiscordWebhook(url=webhook, content=message)
response = webhook.execute()
