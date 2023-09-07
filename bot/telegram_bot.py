import telebot
from .response import get_response
from .redis_utils import ChatHistory
import gpt_2_simple as gpt2
import tensorflow as tf


def extract_after_last_occurrence(text, delimiter="Customer Service:"):
    parts = text.split(delimiter)
    if len(parts) > 1:
        return parts[-1].strip()
    return ""


def start_bot(api_key):
    bot = telebot.TeleBot(api_key)
    chat_store = ChatHistory()

    # Create a new TensorFlow graph
    graph = tf.Graph()
    # Use the graph to create a new session
    with graph.as_default():
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, run_name='run1')

        @bot.message_handler(commands=['start'])
        def enviar(message):
            bot.reply_to(message, "Hi, this is Bank of America Customer Service, how can I help you? :)")

        @bot.message_handler(func=lambda message: True)
        def mensaje(message):
            user_message = message.text
            chat_history = "\n".join(chat_store.get_chat_history(str(message.from_user.id)))
            print(chat_history)
            prompt_format = f"{chat_history}\nUser: {user_message}\nCustomer Service:"
            # Use the session and graph defined above
            with graph.as_default():
                response = gpt2.generate(sess,
                                         length=250,
                                         temperature=0.7,
                                         prefix=prompt_format,
                                         top_k=1,
                                         top_p=0.9,
                                         include_prefix=True,
                                         truncate='',
                                         return_as_list=True)[0]

            ai_response = extract_after_last_occurrence(response)
            chat_store.save_chat(str(message.from_user.id), user_message, ai_response)
            bot.reply_to(message, ai_response)

        bot.polling()