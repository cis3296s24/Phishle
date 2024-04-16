import openai

openai.api_key = ''


def get_response(prompt: str):
    try:
        # ChatCompletion to hold onto chat history
        response = openai.ChatCompletion.create(
            model = "gpt-4-turbo",
            messages = [
                {   "role": "system", 
                    "content": "You are a cybersecurity specialist, with a focus on phishing emails."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=550,
            temperature = 1
        )

        # extract completed text
        completion_text = response["choices"][0]["message"]["content"]
        return completion_text
    
    except Exception as e:
        return {"error": str(e)}
    