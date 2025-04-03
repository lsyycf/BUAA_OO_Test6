import argparse
import os
from tqdm import tqdm
from runner import *
from generate import *
from test import *


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str)
    parser.add_argument("--epoch", type=int)
    parser.add_argument("--instruction", type=int)
    parser.add_argument("--os", type=str)
    args0 = parser.parse_args()
    return args0


if __name__ == "__main__":
    args = parse_args()
    for _ in tqdm(range(args.epoch)):
        make(args.instruction)
        stderr = runner(args.name, args.os)
        stderr += judge_output_valid()
        stderr += judge_person_request()
        if len(stderr) != 0:
            print(stderr)
            err_path = "../Test/ERROR"
            os.makedirs(err_path, exist_ok=True)
            with open(err_path + rf"/{args.name}.txt", "a") as f:
                with open("stdin.txt", 'r') as f1:
                    stdin = f1.read()
                with open("stdout.txt", 'r') as f2:
                    stdout = f2.read()
                f.write("input:\n" + stdin + '\n' + "output:\n" + stdout + '\n' + "error:\n" + stderr + '\n')
