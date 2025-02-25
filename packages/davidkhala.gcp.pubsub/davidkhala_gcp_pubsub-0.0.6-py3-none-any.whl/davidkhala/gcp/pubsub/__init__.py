import re
from typing import Dict

from davidkhala.gcp.auth import OptionsInterface


class TopicAware:
    topic: str
    project: str

    def __init__(self, topic: str, auth: OptionsInterface):
        self.topic = topic
        self.project = auth.project

    @staticmethod
    def topic_path(
            project: str,
            topic: str,
    ) -> str:
        """Returns a fully-qualified topic string."""
        return "projects/{project}/topics/{topic}".format(
            project=project,
            topic=topic,
        )

    @property
    def name(self):
        return TopicAware.topic_path(self.project, self.topic)

    @staticmethod
    def parse_topic_path(path: str) -> Dict[str, str]:
        """Parses a topic path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/topics/(?P<topic>.+?)$", path)
        return m.groupdict() if m else {}
