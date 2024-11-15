from redis import StrictRedis

from core.models import Text
from config import REDIS_HOST, REDIS_PORT


class TextManager:
    def __init__(self):
        self.client = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

    def load_all_text_from_db(self):
        with self.client.pipeline() as pipe:
            for record in Text.objects.all():
                if record.is_button:
                    pipe.hset("buttons", record.title, record.text)
                else:
                    pipe.hset("messages", record.title, record.text)
                pipe.execute()
            pipe.close()

    def get_message_text(self, _title: str, **kwargs) -> str:
        text = self.client.hget("messages", _title) or "empty"
        for key in kwargs:
            text = text.replace(
                key.upper(),
                f"{kwargs[key]:,}" if isinstance(kwargs[key], int) else str(kwargs[key])
            )
        return text

    def get_button_text(self, _title: str, **kwargs) -> str:
        text = self.client.hget("buttons", _title) or "empty"
        for key in kwargs:
            text = text.replace(
                key.upper(),
                f"{kwargs[key]:,}" if isinstance(kwargs[key], int) else str(kwargs[key])
            )
        return text

    def update_text(self, text: Text):
        if text.is_button:
            self.client.hset("buttons", text.title, text.text)
        else:
            self.client.hset("messages", text.title, text.text)

    def delete_text(self, text: Text):
        if text.is_button:
            self.client.hdel("buttons", text.title)
        else:
            self.client.hdel("messages", text.title)


manager = TextManager()
get_message_text = manager.get_message_text
get_button_text = manager.get_button_text

__all__ = ["TextManager", "manager", "get_message_text", "get_button_text"]

