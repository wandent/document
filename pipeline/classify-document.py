import os
import openai
import base64
from openai import OpenAI
from openai import AzureOpenAI
from dotenv import load_dotenv
import tiktoken as TikToken 
load_dotenv()

client = AzureOpenAI( azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
         azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
         api_key=os.getenv("AZURE_OPENAI_KEY"), 
         api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
         
    )


def adjust_text(text_content: str):
    # remove double quotes from the text content
    text_content = text_content.replace('"', "")
    # remove the new line characters from the text content
    text_content = text_content.replace("\n", " ")
    # remove the tab characters from the text content
    text_content = text_content.replace("\t", " ")
    # remove the carriage return characters from the text content
    text_content = text_content.replace("\r", " ")
    # remove the sequence ---------------------------------------------------------- from the text
    text_content = text_content.replace("-" * 10, " ")
    # remove the sequence ********** from the text
    text_content = text_content.replace("*" * 10, " ")
    # remove the | character from the text
    text_content = text_content.replace("|", " ")
    # remove any non utf-8 characters from the text content
    text_content = text_content.encode("utf-8",errors="ignore").decode()
    print(len(text_content))
    return text_content

def classify_content(text_content: any):
    text_content = adjust_text(text_content)

    # Read the content of the text file "classification_prompt.txt" and store it in the variable classification_prompt
    with open("classification_prompt.txt", "r", encoding="utf-8") as file:
        classification_prompt = file.read()
    # Create a list of messages to send to the OpenAI API
    # remove any unsupported characters from the classification_prompt
    classification_prompt = adjust_text(classification_prompt)

    # compress the classification_prompt to using LLMLingua

    msg = [
            {
                "role": "system", "content": f"""You are a helpful assistant. Based on the instructions, pay attention that the instructions are in spanish:{classification_prompt}""" 
                 """If the text does not fit any of the categories, classify as Other.
                Provide the response as a json object with the category as the key, the confidence, and the explanation why the text was put on this category.,
                  # Very Important Instruction: The following text is the one you should review and classify."""
                , "name": "instructions"
            },
            {
                "role": "user", "content": f"The text is very long, read the text entirely before reaching any conclusion. classify the following text: {text_content}", "name": "text"
            },
        ] 

  
    response = client.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages= msg
    )
    return response.choices[0].message.content


def read_trascript(text_file):
    with open(text_file, "r") as file:
        return file.read()

def estimate_tokens(text):
    # Initialize the tokenizer
    #tokenizer = TikToken.get_encoding("gpt2")
    tokennizer = TikToken.get_encoding("cl100k_base")
    # Tokenize the input text
    tokens = tokennizer.encode(text)    
    # Estimate the number of tokens
    num_tokens = len(tokens)    
    return num_tokens

def extract_text(textcontent):
    text_content = adjust_text(textcontent)
    # estimate the token count of text_content using tokenizer



    response = client.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Your job is to extract parts of the content sent as a context and search to extract specific fields",
            },
            
                {"role": "user", "content": """You should return the content as a json feed with the following fields: title, author, dates, abstract, and a summary of the document.
                 # Additional instructions
                 - The date column might have multiple values trhough the document, make sure to extract all the dates and present them as a list in the json.
                 - The abstract is an initial set of conclusions of the study, the content of the abstract is supported by the rest of the document itself. 
                 - The title and author are always present in the document.
                 - The date is not always present in the document. If the date is not present, return an empty string.
                 - For the summary you should read the document entirely and generate a summary of the whole content.
                 -  Keep the tone technical and professional.
                 -  Make sure you keep the language as the document is written, do not translate.               
                 
                 """, "name": "instructions"},
                {"role": "user", "content": f"""The text is very long, read the text entirely before reaching any conclusion. 
                 Extract the requested json from the following text: {text_content}""" , "name": "text" }
        ],
    )
    return response.choices[0].message.content

def main():
    # get the name of the txt files located on the ./text folder
    
    # read all .txt files on .text folder

    for f in os.listdir("./text"):
        if f.endswith(".txt"):
            text_file = f
            text_content = read_trascript(os.path.join("./text", text_file))     
            if estimate_tokens(text_content) > 128000:
                print(f"The text is too long to be processed: {text_file}")
                print(f"Tokens: {estimate_tokens(text_content)}")
                continue
            classific = classify_content(text_content)
            extract = extract_text(text_content)
            print(classific)
            print(extract)

# call the main function
if __name__ == "__main__":
    main()


