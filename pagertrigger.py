import json
import logging

import requests
from errbot import BotPlugin, botcmd


class PagerDutyTrigger(BotPlugin):

    def activate(self):
        super(PagerDutyTrigger, self).activate()

    def deactivate(self):
        super(PagerDutyTrigger, self).deactivate()

    def get_configuration_template(self):
        return { 'SERVICE_API_KEY': 'SECRET' }

    def check_configuration(self, configuration):
        pass

    def callback_connect(self):
        pass

    def callback_message(self, message):
        pass

    def callback_botmessage(self, message):
        pass

    def get_requestor_name(self, frm):
        if frm.fullname is not None:
            return frm.fullname
        elif frm.nick is not None:
            return frm.nick
        else:
            return frm.person

    @botcmd(split_args_with=None)
    def pager_trigger(self, mess, args):
        if not self.config:
            return "PagerDuty is not configured"

        PAGERDUTY_API = "https://events.pagerduty.com/generic/2010-04-15/create_event.json"
        body = {
            'service_key': self.config['SERVICE_API_KEY'],
            'event_type': 'trigger',
            'description': 'Page via chat',
            'details': {
                'requestor': self.get_requestor_name(mess.frm),
                'message': " ".join(args)
            }
        }
        return json.dumps(body)
        # response = requests.post(PAGERDUTY_API, data=json.dumps(body))
        # if response.status_code in (200,):
        #     return "Triggered incident %s" % (response.json()['incident_key'],)
        # else:
        #     logging.error("[PagerDuty] Non-200 response: %s" % response.status_code)
        #     logging.error("[PagerDuty] Body: %s" % response.json())
        #     return "Something went wrong."
