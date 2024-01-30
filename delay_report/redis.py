import redis
from django.conf import settings
import logging
import json


class Redis(object):
    def __init__(self):
        try:
            self.r = redis.from_url(settings.REDIS_URL)
        except Exception as e:
            logging.error(f"Failed to connect to Redis service! {e}")


class Hash(Redis):
    def __init__(self, namespace: str):
        super().__init__()
        self.namespace = namespace

    def hset(self, key, data):
        return self.r.hset(
            f"{self.namespace}:{key}",
            mapping={**data},
        )

    def hget(self, key, field):
        return self.r.hget(f"{self.namespace}:{key}", field)

    def hgetall(self, key):
        return self.r.hgetall(f"{self.namespace}:{key}")

    def exists(self, key):
        return self.r.exists(f"{self.namespace}:{key}")


class AgentHash(Hash):
    NAMESPACE = 'agent'
    ORDER_KEY = "order"

    def __init__(self, agent_id,):
        super().__init__(namespace=self.NAMESPACE)
        self.agent_id = agent_id

    def set_order(self, order):
        return self.hset(
            self.agent_id, {self.ORDER_KEY: order if order else 0}
        )

    def has_order(self):
        if not self.exists(self.agent_id):
            return False

        order = self.hget(self.agent_id, self.ORDER_KEY).decode('utf-8')
        if int(order):
            return True
        return False


class OrderHash(Hash):
    NAMESPACE = 'order'
    REVIEW_KEY = "reviewed"
    AGENT_KEY = "agent"

    def __init__(self, order_id):
        super().__init__(namespace=self.NAMESPACE)
        self.order_id = order_id

    def set_defaults(self):
        return self.hset(
            self.order_id, {self.AGENT_KEY: 0, self.REVIEW_KEY: 0}
        )

    def set_agent(self, agent):
        return self.hset(
            self.order_id, {self.AGENT_KEY: agent if agent else 0}
        )

    def set_review(self, status):
        return self.hset(self.order_id, {self.REVIEW_KEY: 1 if status else 0})

    def has_agent(self):
        agent = self.hget(self.order_id, self.AGENT_KEY).decode('utf-8')
        if int(agent):
            return True
        return False

    def is_reviewed(self):
        reviewed = self.hget(self.order_id, self.REVIEW_KEY).decode('utf-8')
        if int(reviewed):
            return True
        return False

    def add_check(self):
        if self.exists(self.order_id) and not self.is_reviewed():
            return False

        return True


class OrderQueue(Redis):
    NAMESPACE = 'orders'
    KEY = 'delay'

    def __init__(self):
        super().__init__()
        self.key = '%s:%s' % (self.NAMESPACE, self.KEY)

    def size(self):
        return self.r.llen(self.key)

    def is_empty(self):
        return self.size() == 0

    def push(self, item):
        self.r.rpush(self.key, json.dumps(item))

    def pop(self, timeout=None):
        item = self.r.blpop(self.key, timeout=timeout)

        if item:
            item = item[1]

        return item.decode('utf-8')
