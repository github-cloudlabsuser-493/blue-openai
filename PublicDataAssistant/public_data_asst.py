#Labfiles/02-azure-openai-api/Python/test-openai-model.py
#https://github.com/MicrosoftLearning/mslearn-openai/blob/main/Instructions/Exercises/02-natural-language-azure-openai.md
import os
from dotenv import load_dotenv

# Add Azure OpenAI package
from openai import AzureOpenAI

def main(): 
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint, 
            api_key=azure_oai_key,  
            api_version="2024-02-15-preview"
        )
    
        # Initialize messages array
        messages_array = [{"role": "system", "content":  "I am a helpful assistant."}]
        
        while True:
            # Get input text
            input_text = input("Please enter a prompt or 'X' to exit: ")
            if input_text.lower() == "x":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            print("\nSending request for summary to Azure OpenAI endpoint...\n\n")
            
            # Send request to Azure OpenAI model
            messages_array.append({"role": "user", "content": input_text})

            response = client.chat.completions.create(
                model=azure_oai_deployment,
                temperature=1.0,
                max_tokens=1200,
                messages=messages_array
            )
            generated_text = response.choices[0].message.content

            # Add generated text to messages array
            messages_array.append({"role": "system", "content": generated_text})

            # Print generated text
            print("Summary: " + generated_text + "\n")
            

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()