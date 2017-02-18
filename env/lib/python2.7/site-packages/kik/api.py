import base64
import hashlib
import hmac
import json

import requests

from kik.code import Code
from kik.configuration import Configuration
from kik.error import KikError
from kik.user import User

ROOT_URL = 'https://api.kik.com{}'


class KikApi(object):
    """
    Generic API Client for all Kik API features.

    :param bot: Your bot's username
    :type bot: str
    :param api_key: Your bot's API key
    :type api_key: str
    """
    def __init__(self, bot, api_key):
        super(KikApi, self).__init__()
        self.bot = bot
        self.api_key = api_key

    def send_messages(self, messages):
        """
        Sends a batch of messages.

        :param messages: List of :class:`Message <kik.messages.Message>` to be sent.
        :type messages: list[kik.messages.Message]
        :returns: A dict containing the response from the API
        :rtype: dict

        .. note:: Subject to limits on the number of messages sent, documented at
            `<https://dev.kik.com/#/docs/messaging#sending-messages>`_.

        Usage:

        >>> from kik import KikApi
        >>> from kik.messages import TextMessage
        >>> kik = KikApi(BOT_USERNAME, BOT_API_KEY)
        >>> kik.send_messages([
        >>>     TextMessage(
        >>>         to='ausername',
        >>>         chat_id='2e566cf66b07d9622053b2f0e44dd14926d89a6d61adf496844781876d62cca6',
        >>>         body='Some Text'
        >>>     )
        >>> ])
        {}
        """
        response = requests.post(
            ROOT_URL.format('/v1/message'),
            auth=(self.bot, self.api_key),
            timeout=60,
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps({'messages': [m.to_json() for m in messages]})
        )

        if response.status_code != 200:
            raise KikError(response.text)

        return response.json()

    def send_broadcast(self, messages):
        """
        Sends a batch of messages though the broadcast API.

        :param messages: List of :class:`Message <kik.messages.message.Message>` to be sent.
        :type messages: list[kik.messages.Message]
        :returns: A dict containing the response from the API.
        :rtype: dict

        .. note:: Subject to limits on the number of messages sent, documented at
            `<https://dev.kik.com/#/docs/messaging#broadcasting>`_.

        Usage:

        >>> from kik import KikApi
        >>> from kik.messages import TextMessage
        >>> kik = KikApi(BOT_USERNAME, BOT_API_KEY)
        >>> kik.send_broadcast([
        >>>     TextMessage(
        >>>         to='ausername',
        >>>         chat_id='2e566cf66b07d9622053b2f0e44dd14926d89a6d61adf496844781876d62cca6',
        >>>         body='Some Text'
        >>>     )
        >>> ])
        {}
        """
        response = requests.post(
            ROOT_URL.format('/v1/broadcast'),
            auth=(self.bot, self.api_key),
            timeout=60,
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps({'messages': [m.to_json() for m in messages]})
        )

        if response.status_code != 200:
            raise KikError(response.text)

        return response.json()

    def get_user(self, username):
        """
        Gets a user's profile data.

        :param username: List of :class:`Message <kik.messages.Message>` to be sent.
        :type username: str
        :returns: A :class:`User <kik.User>` containing the user's profile data.
        :rtype: kik.User

        .. note:: In order to fetch a user's profile, the user must be a subscriber to your bot

        Usage:

        >>> from kik import KikApi
        >>> kik = KikApi(BOT_USERNAME, BOT_API_KEY)
        >>> kik.get_user('aleem')
        <kik.User>
        """
        response = requests.get(
            ROOT_URL.format('/v1/user/{}'.format(username)),
            auth=(self.bot, self.api_key),
            timeout=60
        )

        if response.status_code != 200:
            raise KikError(response.text)

        content = response.json()

        return User.from_json(content)

    def create_code(self, data=None):
        """
        Creates a Kik Code for your bot.

        :param data: (optional) Data to embed in the code, which will be returned in a `scan-data` message when the
            code is scanned.
        :type data: dict, str
        :returns: A :class:`Code <kik.Code>` representing the code.
        :rtype: kik.Code

        Usage:

        >>> from kik import KikApi
        >>> kik = KikApi(BOT_USERNAME, BOT_API_KEY)
        >>> kik.create_code(data='somedata')
        <kik.Code>
        """
        if data is not None:
            payload = json.dumps({'data': json.dumps(data) if isinstance(data, dict) else data})
        else:
            payload = json.dumps({})

        response = requests.post(
            ROOT_URL.format('/v1/code'),
            auth=(self.bot, self.api_key),
            headers={
                'Content-Type': 'application/json'
            },
            data=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise KikError(response.text)

        content = response.json()

        return Code.from_json(content)

    def get_configuration(self):
        """
        Retrieves your bot's configuration

        :returns: A :class:`Configuration <kik.Configuration>` representing the configuration data.
        :rtype: kik.Configuration

        Usage:

        >>> from kik import KikApi
        >>> kik = KikApi(BOT_USERNAME, BOT_API_KEY)
        >>> kik.get_configuration()
        <kik.Configuration>
        """
        response = requests.get(
            ROOT_URL.format('/v1/config'),
            auth=(self.bot, self.api_key),
            timeout=60
        )

        if response.status_code != 200:
            raise KikError(response.text)

        content = response.json()

        return Configuration.from_json(content)

    def set_configuration(self, config):
        """
        Sets your bot's configuration

        :param config: A :class:`Configuration<kik.Configuration>` containing your bot's new configuration
        :type config: kik.Configuration
        :returns: A :class:`Configuration<kik.Configuration>` containing your bot's new configuration, as confirmed by
        the server
        :rtype: kik.Configuration

        Usage:

        >>> from kik import KikApi, Configuration
        >>> kik = KikApi(BOT_USERNAME, BOT_API_KEY)
        >>> config = Configuration(webhook='https://example.com/incoming')
        >>> kik.set_configuration(config)
        <kik.Configuration>
        """
        response = requests.post(
            ROOT_URL.format('/v1/config'),
            auth=(self.bot, self.api_key),
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(config.to_json()),
            timeout=60
        )

        if response.status_code != 200:
            raise KikError(response.text)

        return Configuration.from_json(response.json())

    def verify_signature(self, signature, body):
        """
        Verifies that a request body correctly matches the header signature.
        For more on signatures see `<https://dev.kik.com/#/docs/messaging#receiving-messages>`_.

        In Python 3, `body` must be a bytestring
        """

        expected = base64.b16encode(hmac.new(self.api_key.encode('utf-8'), body, hashlib.sha1).digest()).decode('utf-8')

        return signature == expected
