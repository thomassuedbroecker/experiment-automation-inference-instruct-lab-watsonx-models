# Setup

## Prerequisites 

You have a [watsonx instance](https://www.ibm.com/products/watsonx-ai) on IBM Cloud, and the InstructLab installed and configured on your local machine.

## Step 1: Python Environment

```sh
cd code
python3 -m venv --upgrade-deps venv
source venv/bin/activate
```

```sh
python3 -m pip install requests
python3 -m pip install openpyxl
```

## Step 2: Python test application configuration 

* Environment Variables

```sh
cat env_template > .env
```

* Content

```txt
# IBM Cloud
export IBMCLOUD_APIKEY=YOUR API KEY
export IBMCLOUD_URL="https://iam.cloud.ibm.com/identity/token"

# Watsonx
export WATSONX_URL="https://us-south.ml.cloud.ibm.com/ml/v1/text/generation"
export WATSONX_VERSION=2023-05-29
export WATSONX_PROJECT_ID=f158173c-d8d4-4eb5-b846-eff2365d4c56

export WATSONX_MIN_NEW_TOKENS=1
export WATSONX_MAX_NEW_TOKENS=300

export WATSONX_LLM_NAME=ibm/granite-13b-chat-v2
export WATSONX_PROMPT_FILE="$(pwd)/prompts/prompt-granite.txt"

# InstructLab
export INSTRUCTLAB_URL="http://127.0.0.1:8000/v1/completions"
export INSTRUCTLAB_PROMPT_FILE="$(pwd)/prompts/prompt-clean.txt"
export INSTRUCTLAB_MAX_NEW_TOKENS=300
```

## Step 3: Shell execution for `watsonx` test automation

```sh
sh run_wx_experiment.sh
```

## Step 4: Shell execution for `instructlab` test automation

You need to open two terminals.

* First terminal

```sh
export MODEL_PATH="YOUR_PATH/YOUR_MODEL.gguf"
cd instructlab
source ./venv/bin/activate
ilab model serve --model-path ${MODEL_PATH}
```

* Second terminal

```sh
sh run_instlab_experiment.sh
```