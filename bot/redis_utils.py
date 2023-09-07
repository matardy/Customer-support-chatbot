import redis

class ChatHistory:

    def __init__(self, host='localhost', port=6379, db=0, ttl = 120):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def save_chat(self, user_id, user_msg, ai_msg):
        self.client.rpush(user_id, f"User: {user_msg}", f"Customer Service: {ai_msg}")

    def get_chat_history(self, user_id):
        return [msg.decode('utf-8') for msg in self.client.lrange(user_id, 0, -1)]
