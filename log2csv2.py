import csv
import os
import json
import re
import sys
from collections.abc import Iterable
from io import StringIO

from pandas import DataFrame

FIELD_NAMES = {
    "train": [
        "episode_reward",
        "step",
        "episode",
        "duration",
        "actor_loss",
        "critic_loss",
        "alpha_loss",
        "alpha_value",
    ],
    "eval": [
        'episode_reward',
        'episode_reward_test_env',
        'step',
        'episode',
    ],
}

def log2csv(inputfilepath):
    filename = os.path.basename(inputfilepath)
    if "train" in filename:
        config = "train"
        outputfilepath = os.path.join(os.path.dirname(inputfilepath), "train.csv")  
    else:
        config = "eval"
        outputfilepath = os.path.join(os.path.dirname(inputfilepath), "eval.csv")
    

    if not os.path.isfile(inputfilepath):
        print("error message :", f"'{inputfilepath}' file does not exist")
        sys.exit(2)

    with open(inputfilepath) as  infile, open(outputfilepath, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=FIELD_NAMES[config])
        writer.writeheader()
        for line in infile:
            data = json.loads(line.strip())
            print("data:", data)
            writer.writerow(data)
        
    print("COMPLETE CONVERTING LOG TO CSV")


if __name__ == "__main__":
    inputfilepath = r'E:\Code\logs\ball_in_cup_catch\tlda\55\train.log'

    log2csv(inputfilepath)
