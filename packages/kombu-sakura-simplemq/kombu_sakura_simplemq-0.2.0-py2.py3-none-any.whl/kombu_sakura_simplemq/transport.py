import base64
import requests
from queue import Empty

from kombu.log import get_logger
from kombu.transport import virtual
from kombu.utils.json import dumps, loads
from kombu.utils.objects import cached_property

logger = get_logger(__name__)


class Channel(virtual.Channel):
    """Sakura Cloud SimpleMQ Channel"""

    def __init__(self, connection, **kwargs):
        super().__init__(connection, **kwargs)
        self._active_messages = {}

    @property
    def transport_options(self):
        return self.connection.client.transport_options

    @cached_property
    def zone(self):
        return self.transport_options.get("zone") or "tk1b"

    @cached_property
    def api_host(self):
        return self.transport_options.get("api_host") or "simplemq.{}.api.sacloud.jp".format(self.zone)

    @cached_property
    def api_key(self):
        return self.connection.client.password or self.transport_options.get("api_key")

    def _get_queue_url(self, queue):
        return "https://{}/v1/queues/{}".format(self.api_host, queue)

    def _get_headers(self):
        return {
            "Authorization": "Bearer {}".format(self.api_key),
        }

    def _get(self, queue, timeout=None):
        """Get next message from `queue`."""
        url = self._get_queue_url(queue) + "/messages"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        payload = response.json()
        if not payload["messages"]:
            raise Empty()

        message = loads(base64.b64decode(payload["messages"][0]["content"]).decode())
        delivery_tag = payload["messages"][0]["id"]
        message["properties"]["delivery_tag"] = delivery_tag

        self._active_messages[delivery_tag] = {
            "queue": queue,
        }
        return message

    def _put(self, queue, message, **kwargs):
        """Put `message` onto `queue`."""
        content = base64.b64encode(dumps(message).encode()).decode()
        payload = {"content": content}
        url = self._get_queue_url(queue) + "/messages"
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()

    def _purge(self, queue):
        """Remove all messages from `queue`."""
        raise NotImplementedError("Virtual channels must implement _purge")

    def _size(self, queue):
        """Return the number of messages in `queue` as an :class:`int`."""
        return 0

    def basic_ack(self, delivery_tag, multiple=False):
        info = self._active_messages.pop(delivery_tag, None)
        if not info:
            super().basic_ack(delivery_tag)
            return

        url = self._get_queue_url(info["queue"]) + "/messages/{}".format(delivery_tag)
        response = requests.delete(url, headers=self._get_headers())
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            super().basic_reject(delivery_tag)
            raise
        else:
            super().basic_ack(delivery_tag)


class Transport(virtual.Transport):
    """Sakura Cloud SimpleMQ Transport.

    .. code-block:: python

        from kombu_sakura_simplemq.transport import Transport

        transport = Transport(
            ...,
            transport_options={
                'api_key': 'your-api-key',
                'zone': 'is1a',
            }
        )

    """  # noqa: E501

    Channel = Channel
    driver_type = "sakura-simplemq"
    driver_name = "sakura-simplemq"
