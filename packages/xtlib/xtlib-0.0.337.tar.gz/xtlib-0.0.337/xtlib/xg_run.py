# xg_run.py: main entry point for the xg program
import os
import sys
import openai
from xtlib import utils
from xtlib import constants
from xtlib.helpers.xt_config import get_merged_config

prompt_prefix = '''We are going to generate command lines for a CLI tool called "xt" that help users launch jobs and generate reports and plots.  Here are some sample English commands and their XT equivalents: 

list the top 15 runs from job235 -> xt list runs job235 --sort=metrics.dev-seq_acc --last=15 
show the last 5 jobs launched -> xt list jobs --last=5 
show any errors from job271 -> xt @error_report --job=job271 
show exploratory report job281 -> xt @explore_report --job=job281 
run train.py on singularity  for 500 epochs with lr=.001 -> xt run --target=singularity  train.py --epochs=500 --lr=.001
show the metrics logged by job555 -> xt list run job555 --avail=metrics
where can I run jobs -> xt list targets
'''

def main(user_text=None):
    if not user_text:
        user_text = " ".join(sys.argv[1:])

    if not user_text:
        print("xg is a command line program for controlling the XT app thru natural language (English)")
        print("xg {}".format(constants.BUILD))
        print()

        print("xg usage: xg <description of what you want XT to do>")
        print("for example: xg show the runs from job123")
    
    else:
        #model_name = "curie:ft-roland-s-personal-gpt-3-account:xg-2023-02-06-05-44-25"
        model_name = "text-davinci-003"

        config = get_merged_config()
        utils.set_openai_key(config, "xt-openai")

        prompt = prompt_prefix + user_text + " ->"
        try:
            response = openai.Completion.create(engine=model_name, prompt=prompt, max_tokens=512, temperature=0)
        except Exception as ex:
            try:
                utils.set_openai_key(config, "xt-openai2")
                response = openai.Completion.create(engine=model_name, prompt=prompt, max_tokens=512, temperature=0)
            except Exception as ex:  
                print("Error: {}".format(ex))
                exit(1)

        xt_cmd = response["choices"][0]["text"].strip()
        if "\n" in xt_cmd:
            xt_cmd = xt_cmd.split("\n")[-1]

        if not xt_cmd.startswith("xt "):
            print("Error: invalid XT command not found in openai response: {}".format(xt_cmd))
            exit(1)

        print("[{}]".format(xt_cmd))
        os.system(xt_cmd)

if __name__ == "__main__":
    # test xg 
    main("run miniMnist.py on singularity for 50 epochs with lr=.001")




