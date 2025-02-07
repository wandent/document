import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("AZURE_DEEPSEEK_API_KEY", '')
if not api_key:
  raise Exception("A key should be provided to invoke the endpoint")

client = ChatCompletionsClient(
    endpoint=os.getenv("AZURE_DEEPSEEK_ENDPOINT", ''),
    credential=AzureKeyCredential(api_key)
)

# create a function to classify the docucuments, receiving a string parameter with the content and returning the classification
def classify_document(content):
    # convert content to UTF-8

    payload = {
        "messages": [
        {
        "role": "user",
        "content": """You work as a geoglogist, and you need to read the content of geoglogical documents of an oil industry and tell me how to you classify it.
            Choose one of the following options:
            1. The document is about the geological formation of oil.
            2. The document is about the geological exploration of oil.
            3. The document is about the geological extraction of oil.
            4. The document is about the geological refining of oil.
            5. The document is about the geological distribution of oil.
            6. The document is about the geological consumption of oil.
            7. The document is about the geological impact of oil.
            
            Use the following context to classify the document:
            {content}
            """
        
    },
    
  ],
  "max_tokens": 2048
}

    response = client.complete(payload)
    print("Response:", response.choices[0].message.content)
    print("Model:", response.model)
    print("Usage:")
    print("	Prompt tokens:", response.usage.prompt_tokens)
    print("	Total tokens:", response.usage.total_tokens)
    print("	Completion tokens:", response.usage.completion_tokens)
    return response.choices[0].message.content


# create the main function
def main():
    # read the content of the file
    # read each file in the directory ./text and run the classification
    for filename in os.listdir('./text'):
        with open(f'./text/{filename}', 'rb') as file:
            content = file.read().decode("utf-8",errors="ignore")
            classification = classify_document(content)
            print(f'The document {filename} was classified as {classification}')



# call the main function
if __name__ == '__main__':
    main()

    