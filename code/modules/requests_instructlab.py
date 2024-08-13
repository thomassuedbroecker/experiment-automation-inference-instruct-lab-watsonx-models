import requests 
from .load_env import load_instructlab_env

def instruct_prompt(question):
    instructlab_env, verification = load_instructlab_env()
    print(f"***LOG: {instructlab_env} : {verification}")

    prompt_question_replace_template="<<QUESTION>>"
    input_txt=""
     
    if ( verification == True):

        url=instructlab_env["INSTRUCTLAB_URL"]
        prompt_file = instructlab_env["INSTRUCTLAB_PROMPT_FILE"]
        max_tokens = instructlab_env["INSTRUCTLAB_MAX_NEW_TOKENS"]
        with open(prompt_file, "r") as f:
                prompt = f.read()
     
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        input_txt = prompt.replace(prompt_question_replace_template,question)   
        #print(f"***LOG: - Prompt input: \n{input_txt}\n\n")
        
        json_data = {
            "prompt": input_txt,
            "max_tokens": max_tokens,
            "stop": [ ] 
        }
     
        # 6. Invoke REST API
        response = requests.post(
            url,
            headers=headers,
            json=json_data
        )

        print(f"***LOG: Response: \n{response.text}\n\n")
                
        # 7. Verify result and extract answer from the return vaule
        if (response.status_code == 200):
                    results=response.json()
                    if "model_version" not in results:
                        results["model_version"] = "no model version"

                    data = {
                        "question": question,
                        "prompt": input_txt,
                        "generated_text": results["choices"][0]["text"],
                        "model_id": results["model"],
                        "model_version": results["model_version"],
                        "generated_token_count": results["usage"]["completion_tokens"],
                        "input_token_count": results["usage"]["prompt_tokens"],
                        "stop_reason": results["choices"][0]["finish_reason"]
                    }
                    verification = True
        else:
                    verification = False
                    data=response.json()
    else:
        verification = False
        data="no missing environment"

    return { "result": data} , {"status":verification} 

