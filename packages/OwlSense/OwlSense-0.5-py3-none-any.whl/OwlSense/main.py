import openai

def OwlSense():
    print("Owl")
    
def gpt(OPENAI_API_KEY , models , promopt):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=models,
        messages=[{"role": "user", "content": f"{promopt}"}]
    )
    return(response.choices[0].message.content)
    