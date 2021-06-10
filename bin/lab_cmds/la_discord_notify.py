from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import site
import sys

site.addsitedir('/opt/opencue/CURRENT/cuegui/venv/lib/python2.7/site-packages')
os.environ['PATH'] = '/opt/opencue/CURRENT/cuegui/venv/bin' + os.pathsep + os.environ['PATH']

from discord_webhook import DiscordWebhook

webhook = 'https://discord.com/api/webhooks/852533533020389406/mjLWCudOguVlLh0oDHuY1xyFGwuzQnHHPArIBkBHR7ZrXCWMNPxlyJVsmvAloGZlaVAU'

list_of_ids = {
    'neill' : '<@!278447205722095616>',
    'christophe' : '<@!278442049651474432>',
}

user    = sys.argv[1]
message = sys.argv[2]

try:
    user = list_of_ids.get(user)
except:
    pass

message = '%s - %s.' % (user, message)

webhook = DiscordWebhook(url=webhook, content=message)
response = webhook.execute()
