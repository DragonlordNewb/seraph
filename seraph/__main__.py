import sys

from seraph import utils
from seraph import tests

def processCommand(args):
	if args[0] in ["exit", "q", "quit"]:
		exit()
	if args[0] in ["test", "runtest"]:
		f = getattr(tests, "test_" + args[1])
		print("Executing test #" + str(args[1]) + " ...")
		f(*args[2:])

if __name__ == "__main__":
	try:
		print("Seraph Artificial Intelligence System initialized.")
		
		if len(sys.argv) != 1:
			with utils.Indent():
				processCommand(sys.argv[1:])
		else:
			print("Type any command to continue, or Ctrl-C to exit.")
			while True:
				processCommand(input(" $ ").split(" "))
	except KeyboardInterrupt:
		exit()