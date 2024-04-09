import openai
#importing the lib to speak to openai

openai.api_key = ''


def response(prompt: str): #prompt string argument which would be the input text to generate...


    try:
        if not api_key:
            return {"error": "Please provide a valid API key."}

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
    