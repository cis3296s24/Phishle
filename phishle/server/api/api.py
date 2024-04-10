import openai

openai.api_key = 'your_openai_api_key_here'


def get_response(prompt: str):
    try:
        # ChatCompletion to hold onto chat history
        response = openai.ChatCompletion.create(
            model = "gpt-4t",
            messages = [
                {   "role": "system", 
                    "content": "You are a cybersecurity specialist, with a focus on phishing emails."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )

        # extract completed test
        completion_text = response["choices"][0]["message"]["content"]
        return completion_text
    
    except Exception as e:
        return {"error": str(e)}
    