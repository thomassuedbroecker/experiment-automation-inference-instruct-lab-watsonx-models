echo "##########################"
echo "# 0. Load environments"
source ./venv/bin/activate
source .env

echo "##########################"
echo "# 1. Set input and output path."
export OUTPUT_PATH=$(pwd)/output
export INPUT_PATH=$(pwd)/input

echo "##########################"
echo "# 2. Set input and output filename."
export RUN_OUTPUT_FILENAME=${OUTPUT_PATH}/"experiment_instructlab_clean_$(date +%Y-%m-%d_%H-%M-%S).xlsx"
export RUN_INPUT_FILENAME=${INPUT_PATH}/"questions.xlsx"

echo "##########################"
echo "# 3. Set inference."
export RUN_INFERENCE="instructlab"

echo "##########################"
echo "# 4. Run experiment"
python3 run_experiment.py --inputfile ${RUN_INPUT_FILENAME} --outputfile ${RUN_OUTPUT_FILENAME} --inference ${RUN_INFERENCE}