import os
import json
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



def read_page(page_file: str, history: dict) -> dict:
    # Read the content of the text file "classification_prompt.txt" and store it in the variable classification_prompt
    base64_image = base64.b64encode(open(page_file, "rb").read()).decode("utf-8")
    r = []
 
    # Create a list of messages to send to the OpenAI API
    # remove any unsupported characters from the classification_prompt    
    message = [ {
                
                "role": "system",
                "content": """You are a geologist, working for an oil company your job is to analyze document pages from a number of different types.
                Convert exactly the text you see. Do not fabricate facts or change the tone. Respond with the same language of the document page you read.
                You don"t need to create any new ending message for every response like: If you need more assistance feel free to ask.
                Use the context of the conversation history make a context and reason with the document page image provided in the end.
                Try to reason with the documents and generate a response that means what is the type of geological data you can interpret from the content.""",
            },
        ]
    # Add the history to the message if the history is provided
    for h in history:
        message.append(h)
    
    message.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "content": "You should read"},
                        {"type": "image_url", "image_url": { "url":  f"data:image/jpeg;base64,{base64_image}" , "detail": "low" }}
                    ] 
                })
    # print(json.dumps(message))
    response = client.chat.completions.create(
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=message,
    )
    # Send the messages to the OpenAI API
    # history.append(f"{"role": "assistant", "content":  {json.dumps(response.choices[0].message.content)}}")   
    # Return the response from the OpenAI API
    # print the content of the message
    # print(json.dumps(message))
    # 
    # print(f"{response.choices[0].message.role}: {response.choices[0].message.content}")
    r = []
    r.append( {'role': response.choices[0].message.role , 'content': response.choices[0].message.content})
    return(r[0])
 
 


def summarize_content(history: dict) -> str:

    # Create a list of messages to send to the OpenAI API
    message = []
    message =[
        {
            "role": "user",
            "content": "You are a geologist, working for an oil company your job is to analyze and summarize data. Do not fabricate facts or change the tone. Respond with the same language of the document page you read. You dont need to create any new ending message for every response like: If you need more assistance feel free to ask. Use the context of the conversation history make a context and reason with the document page image provided in the end.",
        }
     ]
    for h in history:
        message.append(h)
    message.append({
            "role": "user",
            "content": "You should summarize the content from all the responses provided by the assistant",
        }
    )
    # Add the history to the message if the history is provided
    # print(json.dumps(message))  
    response = client.chat.completions.create(
          model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
          messages=message,
     )
    # Send the messages to the OpenAI API
    # Return the response from the OpenAI API
    #return response.choices[0].message.content
    return json.dumps(message)

# Create a function that will reason with the content of the document and generate a response that means what is the type of geological data you can interpret from the content


# create the main function

def main():
    text_location = "./text"
    image_location= "./images"
    text_content: json
    # run the read_page function for each image from a given pdf file
    # set the current directory to document_enriching folder
    # print("Current Directory:", os.getcwd())
    # os.chdir("./document-enriching")
    



    for pdf_file in  [f for f in os.listdir("./document") if f.endswith(".pdf")]:
        # clear the history for every new file handled    
        history = []
        pdf_name = pdf_file.split(".")[0]
        # Process each image in the ./images folder and store the text in the ./text folder starting with the pdf name
        # create the ./text directory if it doesn"t exist
        if not os.path.exists(text_location):
            os.makedirs(text_location)
   
        for image_file in os.listdir(image_location):
            if image_file.endswith(".png") and image_file.startswith(pdf_name):
                # concatenate the results of read_page with text_content as a json
                text_content = read_page(os.path.join(image_location, image_file), history)
                history.append(text_content)

            # Save the text content to a text file
            # outputfile will be the name of the pdf file found on the current folder with the extension .txt
            output_file = os.path.join(text_location, f"{pdf_name}.txt")
            #content = json.dumps(history,indent=4)
            #print(content)
            # write the content of the result to the output file
        with open(output_file, "w") as f:
            f.write(summarize_content(history))
            print(f"Text content saved to {output_file}")            
            # print(f"Summarized Content:{summarize_content(history)}")
           
           

# call the main function
if __name__ == "__main__":
    main()

