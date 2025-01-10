# for each image on the ./images folder, we need to extract the text from the image and save it to a text file with the same name as the image but with the extension .txt.
# The text files should be saved in the folder ./text.
# The text should be extracted via GPT-4o-mini
# The text should be saved in the same order as the images.


# create a function to extract text from an image
import os
import openai
import base64
from openai import OpenAI
from openai import AzureOpenAI

from dotenv import load_dotenv
load_dotenv()
client = AzureOpenAI( azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
         azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
         api_key=os.getenv("AZURE_OPENAI_KEY"), 
         api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        timeout=1000  
    )


def extract_text(image_path): 

    base64_image = base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
    
    response = client.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {
                
                "role": "system",
                "content": "You are a helpful assistant and your job is to convert to text the images sent on each user request. Convert exactly the text you see. Do not fabricate facts or change the tone. You don't need to create any new ending message for every response like: If you need more assistance feel free to ask. Just convert the text.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "content": "Convert following image to text"},
                    {"type": "image_url", "image_url": { "url":  f"data:image/jpeg;base64,{base64_image}" , "detail": "low" }}
                ] 
            },
        ],
    )
    # Extract text from the response.choices
    #print(response.choices[0].message.content)

    text_content = str(response.choices[0].message.content)
    return text_content


# create the main function
def main():
    text_location = "./text"
    image_location= "./images"
    text_content = ""
    # run the code for each pdf file located on ./document folder

    
    
    for pdf_file in  [f for f in os.listdir("./document") if f.endswith(".pdf")]:
        pdf_name = pdf_file.split(".")[0]
        # Process each image in the ./images folder and store the text in the ./text folder starting with the pdf name
        # create the ./text directory if it doesn't exist
        if not os.path.exists(text_location):
            os.makedirs(text_location)
   
        for image_file in os.listdir(image_location):
            if image_file.endswith(".jpg") and image_file.startswith(pdf_name):
                text_content = text_content + extract_text(os.path.join(image_location, image_file))
        

            # Save the text content to a text file
            # outputfile will be the name of the pdf file found on the current folder with the extension .txt
            output_file = text_location +  f"/{pdf_name}.txt"
            with open(output_file, "w") as text_file:
                text_file.write(str(text_content.encode('utf-8')))


# call the main function
if __name__ == "__main__":
    main()
