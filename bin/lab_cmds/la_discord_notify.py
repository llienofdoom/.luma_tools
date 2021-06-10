from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import site
import sys

site.addsitedir('/opt/opencue/CURRENT/cuegui/venv/lib/python2.7/site-packages')
os.environ['PATH'] = '/opt/opencue/CURRENT/cuegui/venv/bin' + os.pathsep + os.environ['PATH']

from discord_webhook import DiscordWebhook




user    = sys.argv[1]
message = sys.argv[2]

try:
    user = list_of_ids.get(user)
except:
    pass

message = '%s - %s.' % (user, message)

webhook = DiscordWebhook(url=webhook, content=message)
response = webhook.execute()
