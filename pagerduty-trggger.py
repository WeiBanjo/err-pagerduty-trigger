import json
import logging

import requests
from errbot import BotPlugin, botcmd


class PagerDutyTrigger(BotPlugin):

    def activate(self):
        """
        Triggers on plugin activation
        You should delete it if you're not using it to override any default behaviour
        """
        super(BotPlugin, self).activate()

    def deactivate(self):
        """
        Triggers on plugin deactivation
        You should delete it if you're not using it to override any default behaviour
        """
        super(BotPlugin, self).deactivate()

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        You should delete it if your plugin doesn't use any configuration like this
        """
        return { 'SERVICE_API_KEY': 'SECRET' }

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation
        You should delete it if you're not using it to override any default behaviour
        """
        super(BotPlugin, self).check_configuration()

    def callback_connect(self):
        """
        Triggers when bot is connected
        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself
        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot itself
        You should delete it if you're not using it to override any default behaviour
        """
        pass

    @botcmd(split_args_with=None)
    def pager_register(self, mess, args):
        if not self.config:
            return "PagerDuty is not configured"

        PAGERDUTY_API = "https://events.pagerduty.com/generic/2010-04-15/create_event.json"
        body = {
            'service_key': self.config['SERVICE_API_KEY'],
            'event_type': 'trigger',
            'description': 'Page via chat',
            'details': {
                'requestor': mess.frm.person,
                'message': " ".join(args)
            }
        }
        response = requests.post(PAGERDUTY_API, data=json.dumps(body))
        if response.status_code in (200,):
            return "Triggered incident %s" % (response.json()['incident_key'],)
        else:
            logging.error("[PagerDuty] Non-200 response: %s" % response.status_code)
            logging.error("[PagerDuty] Body: %s" % response.json())
            return "Something went wrong."
