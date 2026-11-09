import pandas as pd
import os
import csv 
import io

# Folder containing the generator's full text responses
output_folder = 'results/generated_responses/'
template_folder = 'template_files/'

columns = [
    'Tutor name', 'Problem number', 'Problem',
    'Delivered', 'Importable', 'Order of Path',
    'Language', 'Hint Accuracy', 'Success Messages',
    'Buggy Links', 'Column Count', 'Labels Matching',
    'Constant rows', 'Hint Structure', 'Answers Correct',
    '(Same, Concept)', '(Same, Complexity)',
    '(Different, Scenario)', '(Different, Values)',
    '(Directly usable, Realism)',
    '(Directly usable, Question Still in Story)',
    "(Same, Doesn't Over-Scaffold)",
    'Comments', 'Response File', 'TSV Extraction'
]

def extract_tsv(text):
    start = text.find("```tsv\n")
    if start == -1:
        raise ValueError("No TSV block found")
    start += len("```tsv\n")
    end = text.find("```",start)

    if end == -1:
        raise ValueError("Closing TSV not found")
    return text[start:end]


all_response_files = [
    f for f in os.listdir(output_folder)
    if f.endswith('.txt')
]

all_evaluations = []

for file in all_response_files:
    file_path = os.path.join(output_folder, file)

    try:
        with open(file_path, encoding='utf-8') as response_file:
            response_text = response_file.read()

        tsv_text = extract_tsv(response_text)
        generated_rows = list(csv.reader(
            io.StringIO(tsv_text),
            delimiter='\t'
        ))

        #Load the corresponding template file
        template_name = file.rsplit('_prompt', 1)[0] + '.tsv'
        template_path = os.path.join(template_folder, template_name)

        with open(template_path, encoding='utf-8-sig', newline='') as template_file:
            template_rows = list(csv.reader(
                template_file,
                delimiter='\t'
            ))

        # Compare Labels Matching
        generated_labels = []
        template_labels = []

        for row in generated_rows:
            if len(row) > 0:
                generated_labels.append(row[0])
            else:
                generated_labels.append(None)

        for row in template_rows:
            if len(row) > 0:
                template_labels.append(row[0])
            else:
                template_labels.append(None)

        labels_matching = generated_labels == template_labels

        #Column count check
        column_count_correct = True 

        if len(generated_rows) == 0:
            column_count_correct = False 

        for row in generated_rows:
            if len(row) != 2:
                column_count_correct =False 
                break
        
        all_evaluations.append({
            'Response File': file,
            'TSV Extraction': 'Pass',
            'Column Count': 'Pass' if column_count_correct else 'Fail',
            'Labels Matching': 'Pass' if labels_matching else 'Fail',
            'Comments': ''
        })

    except ValueError as e:
        all_evaluations.append({
            'Response File': file,
            'TSV Extraction': 'Fail',
            'Comments': str(e)
        })

# Creates a DataFrame with all metrics
all_evaluations_df = pd.DataFrame(all_evaluations).reindex(
    columns=columns,
    fill_value='Not evaluated'
)

# Saves evaluation table
all_evaluations_df.to_csv('results/evaluations.csv', index=False)
