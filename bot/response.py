import gpt_2_simple as gpt2
from .redis_utils import ChatHistory

chat_store = ChatHistory()

def extract_after_last_occurrence(input_string):
    keyword = "Customer Service: "
    parts = input_string.split(keyword)
    if len(parts) > 1:
        return parts[-1]
    else:
        return None

def get_response(user_id, prompt, sess):
    # Tomamos el historial de mensajes anterior
    chat_history = "\n".join(chat_store.get_chat_history(user_id))

    
    

    prompt_format = f"{chat_history}\nUser: {prompt}\nCustomer Service:"

    response = gpt2.generate(sess,
              length=250,
              temperature=0.7,
              prefix=prompt_format,
              top_k = 1,
              top_p=0.9,
              include_prefix=True,
              truncate='',
              return_as_list=True
              )[0]

    format_response = extract_after_last_occurrence(response)
    return format_response
