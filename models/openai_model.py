import openai

class OpenAIModel:
    def __init__(self, api_key="your-api-key"):
        openai.api_key = api_key

    def generate_response(self, prompt):
        # استدعاء API من OpenAI للحصول على الرد
        response = openai.Completion.create(
            engine="text-davinci-003",  # أو استخدم أي نموذج آخر تفضله
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
