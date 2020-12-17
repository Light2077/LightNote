# demo.py
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="enter you name", type=str)
parser.add_argument("-a", "--age", help="enter you age", type=int)
args = parser.parse_args()
if not args.name or not args.age:
    print('do not know who you are')
else:
    print(f"hello {args.name}, you are {args.age} years old.")