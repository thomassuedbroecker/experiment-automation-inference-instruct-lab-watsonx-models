# Experiment automation of running models in inferences in InstructLab or  watsonx

## Objective

The objective is to run tests against models running in the inference of the InstructLab and watsonx using the REST APIs.

This repository is related to the two blog posts related to the InstructLab.

* Setup of the [InstructLab for fine-tuning](https://suedbroecker.net/2024/06/20/fine-tune-llm-foundation-models-with-the-instructlab-an-open-source-project-introduced-by-ibm-and-red-hat/)
* Fine-tune a model with the [InstructLab](https://suedbroecker.net/2024/06/21/instructlab-and-taxonomy-tree-llm-foundation-model-fine-tuning-guide-musician-example/)

The repository contains automation for a question-answering use case with LLM models.

The input questions will provided by the users in an Excel file, and the automation will generate an Excel output file with various information from the run.

Questions are input parameters to use the models in a question-answering use case. The LLM models run in the local InstructLab and on watsonx.ai in the IBM Cloud.

> Note: You can find the currently supported foundation models for InstructLab on the [InstructLab-compatible foundation models page](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-instructlab.html?context=wx&locale=tr).

## Setup and Architecture

Here is a simplified overview of the input, output, and configuration of the text framework:

* We use a Phyton application with command line parameters to invoke the REST API for watsonx and InstructLab to send all questions.
* We use shell scripts to save various configurations to invoke the Python application.

### 1. Python application

* Input: Excel file with a `question` column 
* Output: Excel file with the columns.

The following table contains the columns for the output Excel file.

| question | prompt | generated_text | model_id | model_version | generated_token_count | input_token_count | stop_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| question | prompt | generated_text | model_id | model_version | generated_token_count | input_token_count | stop_reason |

* Environment variables in the `.env` file for the Python application

```sh
# IBM Cloud
export IBMCLOUD_APIKEY=
export IBMCLOUD_URL="https://iam.cloud.ibm.com/identity/token"

# Watsonx
export WATSONX_URL="https://us-south.ml.cloud.ibm.com/ml/v1/text/generation"
export WATSONX_VERSION=2023-05-29
export WATSONX_PROJECT_ID=XXXXXX

export WATSONX_MIN_NEW_TOKENS=1
export WATSONX_MAX_NEW_TOKENS=300

export WATSONX_LLM_NAME=ibm/granite-13b-chat-v2
export WATSONX_PROMPT_FILE="$(pwd)/prompts/prompt-granite.txt"

# InstructLab
export INSTRUCTLAB_URL="http://127.0.0.1:8000/v1/completions"
export INSTRUCTLAB_PROMPT_FILE="$(pwd)/prompts/prompt-clean.txt"
export INSTRUCTLAB_MAX_NEW_TOKENS=300
```

### 1. Shell automation

The following code is the content for a shell script to run the test against a model on watsonx. We define the model and the prompt file, set the proper input parameters, and specify the output location and file name.

```sh
echo "##########################"
echo "# 0. Load environments"
source ./venv/bin/activate
source .env

export WATSONX_LLM_NAME=ibm/granite-13b-chat-v2
export WATSONX_PROMPT_FILE="$(pwd)/prompts/prompt-clean.txt"

echo "##########################"
echo "# 1. Set input and output path."
export OUTPUT_PATH=$(pwd)/output
export INPUT_PATH=$(pwd)/input

echo "##########################"
echo "# 2. Set input and output filename."
export RUN_OUTPUT_FILENAME=${OUTPUT_PATH}/"experiment_granite_clean_$(date +%Y-%m-%d_%H-%M-%S).xlsx"
export RUN_INPUT_FILENAME=${INPUT_PATH}/"questions.xlsx"

echo "##########################"
echo "# 3. Set inference."
export RUN_INFERENCE="watsonx"

echo "##########################"
echo "# 4. Run experiment"
python3 run_experiment.py --inputfile ${RUN_INPUT_FILENAME} --outputfile ${RUN_OUTPUT_FILENAME} --inference ${RUN_INFERENCE}
```

### 2. [Setup README](/code/README.md)
