import requests 
from .load_env import load_watson_x_env
from .requests_ibmcloud_token import get_token

def watsonx_prompt(question):
    watsonx_env, verification = load_watson_x_env()
    print(f"***LOG: {watsonx_env} : {verification}")

    prompt_question_replace_template="<<QUESTION>>"
    input_txt=""
    
    if (verification):

        # 1. Load environment variables
        url = watsonx_env["WATSONX_URL"]
        # print(f"***LOG: watsonx_simple_prompt - url: {url}")

        # 2. Get access token
        token, verification = get_token()
        apikey = "Bearer " + token["result"]
        #print(f"***LOG:\n - API KEY: {apikey} \n")
        #print(f"***LOG:\n - Verification: {verification}")

        if ( verification["status"] == True):
            apikey = "Bearer " + token["result"]
            model_id = watsonx_env["WATSONX_LLM_NAME"]
            #print(f"***LOG: - Url: {model_id}")
            min_tokens = watsonx_env["WATSONX_MIN_NEW_TOKENS"]
            #print(f"***LOG: - Min_tokens: {min_tokens}")
            max_tokens = watsonx_env["WATSONX_MAX_NEW_TOKENS"]
            #print(f"***LOG: - Max_tokens: {max_tokens}")
            prompt_file = watsonx_env["WATSONX_PROMPT_FILE"]
            with open(prompt_file, "r") as f:
                 prompt = f.read()
            print(f"***LOG: - Prompt: {prompt}")
            project_id = watsonx_env["WATSONX_PROJECT_ID"]
            #print(f"***LOG: - Project_id: {project_id}")
            version = watsonx_env["WATSONX_VERSION"]
            #print(f"***LOG: - Version: {version}")

            # 3. Build the header with authenication       
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": apikey
            }

            # 4. Build the params
            params = {
                 "version": version
            }
        
            # 5. Build the prompt with context documents and question
            input_txt = prompt.replace(prompt_question_replace_template,question)
    
            print(f"***LOG: - Prompt input: \n{input_txt}\n\n")
        
            # 6. Create payload
            json_data = {
                    "model_id": model_id,
                    "input": input_txt,
                    "parameters":{
                        "decoding_method": "greedy",
                        "min_new_tokens": int(min_tokens),
                        "max_new_tokens": int(max_tokens),
                        "beam_width": 1 
                    },
                     "project_id": project_id      
            }
     
            # 6. Invoke REST API
            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=json_data
            )

            print(f"***LOG: Response: \n{response.text}\n\n")
                
            # 7. Verify result and extract answer from the return vaule
            if (response.status_code == 200):
                    data_all=response.json()
                    results = data_all["results"]
                    
                    if "model_version" not in data_all:
                        data_all["model_version"] = "no model version"
                    
                    data = {
                        "question": question,
                        "prompt": input_txt,
                        "generated_text": results[0]["generated_text"],
                        "model_id": data_all["model_id"],
                        "model_version": data_all["model_version"],
                        "generated_token_count": results[0]["generated_token_count"],
                        "input_token_count": results[0]["input_token_count"],
                        "stop_reason": results[0]["stop_reason"],
                    }
                    verification = True
            else:
                    verification = False
                    data=response.json()
    else:
        verification = False
        data="no access token available"

    return { "result": data} , {"status":verification} 

