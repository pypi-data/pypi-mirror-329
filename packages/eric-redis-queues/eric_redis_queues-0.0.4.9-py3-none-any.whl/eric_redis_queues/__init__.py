import json
from uuid import uuid4

from redis import Redis

from eric_sse.exception import NoMessagesException
from eric_sse.message import Message
from eric_sse.queue import Queue, AbstractMessageQueueFactory, RepositoryError

class RedisQueue(Queue):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.id = str(uuid4())
        self.__client = Redis(host=host, port=port, db=db)

    def pop(self) -> Message:
        try:
            raw_value = self.__client.lpop(self.id)
        except Exception as e:
            raise RepositoryError(e)

        if raw_value is None:
            raise NoMessagesException

        value = json.loads(raw_value.decode())
        return Message(msg_type=value['type'], msg_payload=value['payload'])

    def push(self, msg: Message) -> None:
        value = json.dumps({'type': msg.type, 'payload': msg.payload})
        try:
            self.__client.rpush(self.id, value)
        except Exception as e:
            raise RepositoryError(e)

    def delete(self) -> None:
        self.__client.delete(self.id)


class RedisQueueFactory(AbstractMessageQueueFactory):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.__host: str = host
        self.__port: int = port
        self.__db: int = db

    def create(self) -> Queue:
        return RedisQueue(host=self.__host, port=self.__port, db=self.__db)
