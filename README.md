# blue-openai
## Pre-requisite:
Ensure the .env file is populated with secrets corresponding to OpenAI and Azure Cognitive Search resources.

## Run the application in Terminal:

cd PrivateDataAssistant/ \
pip install python-dotenv \
pip install openai==1.13.3 \
python private_data_asst.py

#### The above assistant only bases responses off of private data in Azure storage. We've also included an assistant to pull public data for your convenience:

cd PublicDataAssistant/ \
python public_data_asst.py

