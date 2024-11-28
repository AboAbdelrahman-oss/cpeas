import torch
from transformers import LlamaTokenizer, LlamaForCausalLM

class LlamaModel:
    def __init__(self, model_name="huggingface/llama"):
        # تحميل النموذج
        self.model = LlamaForCausalLM.from_pretrained(model_name)
        self.tokenizer = LlamaTokenizer.from_pretrained(model_name)

    def generate_response(self, prompt):
        # تحويل المدخلات إلى تنسيق يمكن أن يفهمه النموذج
        inputs = self.tokenizer(prompt, return_tensors="pt")
        output = self.model.generate(inputs['input_ids'], max_length=100, num_return_sequences=1)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response
