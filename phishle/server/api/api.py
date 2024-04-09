import openai

openai.api_key = 'your_openai_api_key_here'


def response(prompt: str):
    try:
        # ChatCompletion to hold onto chat history
        reponse = openai.ChatCompletion.create(
            model = "gpt-4t",
            prompt = prompt
        )

        # extract completed test
        completion_text = reponse["choices"][0]["message"]["content"]
        return completion_text
    
    except Exception as e:
        return {"error": str(e)}
    