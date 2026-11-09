# CTAT Auto-Eval

## Generator

`autoeval_generator.py` reads each example TSV in `template_files/` and sends the entire table with each prompt from `prompts.csv` to the configured OpenAI model.

Full responses are saved as `.txt` files in `results/generated_responses/`. Filenames identify the template, prompt number, and model. The evaluator will later extract the generated TSV from each response.

### Usage

1. Place example TSVs in `template_files/`.
2. Add generation prompts to the `prompt` column in `prompts.csv`.
3. Configure `model_name` and API credentials. Do not commit your API key.
4. Run `autoeval_generator.py`.

API compatibility and output-token limits still need to be addressed before testing.