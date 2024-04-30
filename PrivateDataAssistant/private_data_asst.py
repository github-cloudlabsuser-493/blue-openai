import os
import json
from dotenv import load_dotenv

# Add OpenAI import
from openai import AzureOpenAI

def main(): 
        
    try:
        # Flag to show citations
        show_citations = False

        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        azure_search_key = os.getenv("AZURE_SEARCH_KEY")
        azure_search_index = os.getenv("AZURE_SEARCH_INDEX")
        
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            base_url=f"{azure_oai_endpoint}/openai/deployments/{azure_oai_deployment}/extensions",
            api_key=azure_oai_key,
            api_version="2023-09-01-preview")

        # Create a system message
        system_message = """I am a helpful AI chatbot named Blue. I specialize in providing information on engineering documents about airplanes. 
                I will attempt to give references as often as possible.
                I will include page numbers or other locations for figures, tables, charts, or other embedded facts when available. 
                """

        # Configure your data source
        extension_config = dict(dataSources = [  
        { 
            "type": "AzureCognitiveSearch", 
            "parameters": { 
                "endpoint":azure_search_endpoint, 
                "key": azure_search_key, 
                "indexName": azure_search_index,
            }
        }]
        )

        while True:
            # Get the prompt
            input_text = input("\nPlease enter a prompt or 'X' to exit:\n")
            if input_text.lower() == "x":
                break
            if len(input_text) == 0:
                print("Please submit a question.")
                continue

            # Send request to Azure OpenAI model
            print("...Sending the following request to Azure OpenAI endpoint...")
            print("Request: " + input_text + "\n")

            response = client.chat.completions.create(
                model = azure_oai_deployment,
                temperature = 0.7,
                max_tokens = 1000,
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": input_text}
                ],
                extra_body = extension_config
            )

            # Print response
            print("Response: " + response.choices[0].message.content + "\n")

            if (show_citations):
                # Print citations
                print("Citations:")
                citations = response.choices[0].message.context["messages"][0]["content"]
                citation_json = json.loads(citations)
                for c in citation_json["citations"]:
                    print("  Title: " + c['title'] + "\n    URL: " + c['url'])


        
    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()


