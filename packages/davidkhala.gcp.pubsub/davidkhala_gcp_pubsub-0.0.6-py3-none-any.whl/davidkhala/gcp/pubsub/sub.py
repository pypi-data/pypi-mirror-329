from typing import Callable, Any, Iterable

from davidkhala.gcp.auth import OptionsInterface
from google.api_core.exceptions import NotFound, AlreadyExists
from google.cloud.pubsub import SubscriberClient
from google.cloud.pubsub_v1.futures import Future
from google.cloud.pubsub_v1.subscriber.message import Message
from google.pubsub import Subscription

from davidkhala.gcp.pubsub import TopicAware


def show(message: Message, future: Future):
    print(message.data)
    message.ack()
    future.cancel()


class Sub(TopicAware):
    subscription: str

    def __init__(self, subscription: str, topic: str, auth: OptionsInterface):
        super().__init__(topic, auth)
        self.client = SubscriberClient(
            credentials=auth.credentials,
            client_options=auth.client_options,
        )
        self.subscription = subscription

    def disconnect(self):
        self.client.close()

    def create(self):
        try:
            self.client.create_subscription(
                name=self.subscription_path,
                topic=self.name,
            )
        except AlreadyExists as e:
            if f"409 Resource already exists in the project (resource={self.subscription})." != str(e):
                raise e

    def get(self) -> Subscription:
        return self.client.get_subscription(subscription=self.subscription_path)

    def delete(self):
        try:
            self.client.delete_subscription(subscription=self.subscription_path)
        except NotFound as e:
            if f"404 Resource not found (resource={self.subscription})." != str(e):
                raise e

    @property
    def messages(self):
        r = self.client.pull(subscription=self.subscription_path, max_messages=1000)
        return r.received_messages

    @property
    def ack_ids(self) -> list[str]:
        return list(_.ack_id for _ in self.messages)

    def purge(self):
        _snapshot = self.ack_ids
        if len(_snapshot) > 0:
            self.client.acknowledge(subscription=self.subscription_path, ack_ids=_snapshot)

    def reset(self):
        """
        make the message available for redelivery
        :return:
        """
        _snapshot = self.ack_ids
        if len(_snapshot) > 0:
            self.client.modify_ack_deadline(
                subscription=self.subscription_path,
                ack_ids=_snapshot,
                ack_deadline_seconds=0
            )

    @property
    def subscription_path(self):
        return SubscriberClient.subscription_path(self.project, self.subscription)

    def listen_async(self, callback: Callable[[Message, Future], Any]) -> Future:
        # Cancelling the future will signal the process to shut down gracefully and exit.
        future = self.client.subscribe(self.subscription_path, lambda message: callback(message, future))
        return future

    def listen(self, callback: Callable[[Message, Future], Any] = show):
        """
        Waiting on the future
        This will block forever or until a non-recoverable error is encountered (such as loss of network connectivity, cancelling the future)
        """
        future = self.listen_async(callback)
        future.result()
