from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/blenderbot-400M-distill"

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

conversation_history = []
# history_string = "\n".join(conversation_history)
# input_text ="hello, how are you doing?"
# inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")
# print(inputs)

# print(tokenizer.pretrained_vocab_files_map)

# outputs = model.generate(**inputs)
# print(outputs)

# response = tokenizer.decode(outputs[0], max_new_tokens = 50, skip_special_tokens=True).strip()
# print(response)

while True:
    history_string = "\n".join(conversation_history)

    input_text = input("> ")
    inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")
    outputs = model.generate(**inputs)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    print(response)

    conversation_history.append(input_text)
    conversation_history.append(response)
