#takes in tsv -> API calls to models -> saves full response as a text file for evaluator
import openai
import pandas as pd
import os

# Specify the relative folder paths for original files and output
original_folder = 'template_files/'
output_folder = 'results/generated_responses/'
model_name = "gpt-4"

# Set the API key for openai
openai.api_key = ' Enter you API key'  

# Reads prompts from a CSV file
try:
    prompt_df = pd.read_csv('Prompts.csv', encoding='utf-8')
except Exception as e:
    print("Error reading prompts.csv:", str(e))
    exit()

# Creates the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Constructs full path using the current working directory
original_folder_path = os.path.join(os.getcwd(), original_folder)

def api_call(post_text, prompt):
    try:
        message_content = f'{prompt}\n{post_text}'
        response_check = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message_content}
            ],
            max_tokens=1000
        )
        return response_check["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"API call error for post_text: {post_text[:50]}", str(e))
        return "API_ERROR"

try:
    original_files = os.listdir(original_folder_path)
except Exception as e:
    print(f"Error reading from directory {original_folder_path}:", str(e))
    exit()

for original_file in original_files:
    if original_file.endswith('.tsv'):
        try:
            # Reads the entire TSV instead of individual forum posts
            with open(os.path.join(original_folder_path, original_file), encoding='utf-8') as file:
                original_text = file.read()

            # Iterates for each prompt
            for index, row in prompt_df.iterrows():
                prompt = row['prompt']
                response = api_call(original_text, prompt)

                if response == "API_ERROR":
                    continue

                # Saves the full model response for the current prompt
                response_filename = f'{original_file.replace(".tsv", "")}_prompt{index+1}_openai_{model_name}.txt'
                output_file_path = os.path.join(output_folder, response_filename)

                with open(output_file_path, 'w', encoding='utf-8', newline='') as file:
                    file.write(response)

                print(f"Saved file {output_file_path}")

        except Exception as e:
            print(f"Error processing file {original_file}:", str(e))
