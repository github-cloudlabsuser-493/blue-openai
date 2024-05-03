import os
import json
from dotenv import load_dotenv

# Add OpenAI import
from openai import AzureOpenAI

# Create a system message
default_system = """I am a helpful AI chatbot named Blue for a company called BlueAirCo that builds airplanes. I specialize in providing information on engineering documents about airplanes. 
        I will attempt to give references as often as possible.
        I will include page numbers or other locations for figures, tables, charts, or other embedded facts when available. 
        """
system_message = default_system

def update_role():
    global system_message
    #Wipe current message
    system_message = default_system
    while True:
        user_role = input("""\nPlease enter the number corresponding to your role.\n
            1: Engineer\n
            2: Manager\n
            3: Executive\n
            4: Public Relations\n
            5: Other\n""")
        
        if user_role == '1':
            system_message += " I will tailor my messages to an engineer who is highly technical and cares about safety concerns."
            break
        elif user_role == '2':
            system_message += " I will tailor my messages to a manager who wants a high level overview especially where timelines are applicable and who is not overly technical."
            break
        elif user_role == '3':
            system_message += " I will tailor my messages to an executive who cares about the big picture and has an eye on the future of aviation. "
            break
        elif user_role == '4':
            system_message += " I will tailor my messages to a public relations employee who needs to communicate to the general public in a positive and reassuring manner. "
            break
        elif user_role == '5':
            system_message = default_system
            break
        else: 
            print("Invalid input\n")

def check_for_exit(input_text):
    if input_text.lower() == "x":
        exit(1)

def no_input(input_text):
    return len(input_text) == 0

def role_change(input_text):
    if input_text.lower() == "r":
        update_role()
        print("Role updated.\n")
        return True
    return False

def valid_prompt_input(input_text):
    if no_input(input_text):
        print("Please enter valid input.\n")
        return False
    check_for_exit(input_text)
    return True

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


        print("\nHello, I'm Blue, your personal assistant for BlueAirCo.\n")
        
        update_role()

        while True:
            # Get the prompt
            input_text = input("\nPlease enter a prompt, 'R' to change role, or 'X' to exit:\n")

            if not valid_prompt_input(input_text):
                continue
            if role_change(input_text):
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


