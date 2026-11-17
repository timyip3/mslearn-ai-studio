import os
import subprocess
from dotenv import load_dotenv

# import namespaces
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI


def main(): 
    # Clear the console
    subprocess.run('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
        openai_client = OpenAI(
            api_key=token_provider,
            base_url=azure_openai_endpoint
        )

        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Get a response
            # completion = openai_client.chat.completions.create(
            #     model=model_deployment,
            #     messages=[
            #         {"role": "system", "content": "You are a helpful AI assistant that answers questions and provides information."},
            #         {"role": "user", "content": input_text}
            #     ]
            # )

            # print("\nAI Response:")
            # print(completion.choices[0].message.content)

            ## Using response API

            # response = openai_client.responses.create(
            #     model=model_deployment,
            #     instructions="You are a helpful AI assistant that answers questions and provides information.",
            #     input=input_text,
            #     previous_response_id=last_response_id
            # )

            # print("\nAI Response (using response API):")
            # print(response.output_text)
            # last_response_id = response.id

            # Stream response
            stream = openai_client.responses.create(
                model=model_deployment,
                instructions="You are a helpful AI assistant that answers questions and provides information.",
                input=input_text,
                previous_response_id=last_response_id,
                stream=True
            )

            print("\nAI Response (streaming):")

            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="")
                elif event.type == "response.completed":
                    print("\nResponse completed.")
                    last_response_id = event.response.id


    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
