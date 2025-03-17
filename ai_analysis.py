import os
import re
import argparse
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Analyze code or logs using Azure OpenAI.")
    parser.add_argument("--input", required=True, help="Path to the file containing content to analyze.")
    args = parser.parse_args()

    try:
        with open(args.input, "r") as file:
            input_content = file.read()
    except Exception as e:
        raise Exception(f"Error reading input file: {e}")

    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_content},
        ]
    )

    output_text = response.choices[0].message.content

    print("Overall AI Response:")
    print(output_text)

    code_blocks = re.findall(r"```(?:python)?\n(.*?)\n```", output_text, re.DOTALL)
    if code_blocks:
        revised_code = code_blocks[0].strip()
    else:
        revised_code = output_text.strip()

    print("Extracted Revised Code:")
    print(revised_code)

    with open("revised_code.py", "w") as f:
        f.write(revised_code)

if __name__ == "__main__":
    main()
