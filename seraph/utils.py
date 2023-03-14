# THE ACCOMPANYING PROGRAM IS PROVIDED UNDER THE TERMS OF THIS ECLIPSE
# PUBLIC LICENSE ("AGREEMENT"). ANY USE, REPRODUCTION OR DISTRIBUTION
# OF THE PROGRAM CONSTITUTES RECIPIENT'S ACCEPTANCE OF THIS AGREEMENT.

import threading
import blessed
import sys
import time

class Process:
    busy = False
    paused = False

    def __enter__(self) -> object:
        self.busy = True
        threading.Thread(target=self._task).start()
        return self

    def __exit__(self, exc: Exception or object, tb: str, value, int) -> None or False:
        self.busy = False
        if exc is not None:
            return False

    def _task(self) -> None:
        while self.busy:
            if not self.paused:
                self.task()
            else:
                time.sleep(0.1)

    def pause(self) -> None:
        self.paused = True

    def unpause(self) -> None:
        self.paused = False

class Contexts:
    def __init__(self, *ctxs):
        self.ctxs = ctxs

    def __enter__(self):
        for ctx in self.ctxs:
            ctx.__enter__()

    def __exit__(self, exc, tb, value):
        for ctx in self.ctxs:
            ctx.__exit__(exc, tb, value)

        if exc is not None:
            return False

term = blessed.Terminal()

def cls():
	print(term.clear())

class Spinner:
	busy = False
	delay = 0.1

	@staticmethod
	def spinning_cursor():
		while 1: 
			for cursor in '|/-\\': yield cursor

	def __init__(self, text="", delay=0.05):
		self.text = text
		self.spinner_generator = self.spinning_cursor()
		if delay and float(delay): self.delay = delay

	def spinner_task(self):
		with term.cbreak(), term.hidden_cursor():
			while self.busy:
				sys.stdout.write(self.text + " " + next(self.spinner_generator))
				sys.stdout.flush()
				time.sleep(self.delay)
				sys.stdout.write("\r")
				sys.stdout.flush()

	def __enter__(self):
		self.busy = True
		threading.Thread(target=self.spinner_task).start()

	def __exit__(self, exception, value, tb):
		self.busy = False
		time.sleep(self.delay)
		print(self.text + " - done.")
		if exception is not None:
			return False
		
Pinwheel = Spinner
		
class Ellipsis:
	busy = False
	delay = 0.1

	@staticmethod
	def spinning_cursor():
		while 1: 
			for cursor in ["   ", ".  ", ".. ", "..."]: yield cursor

	def __init__(self, text="", delay=0.1):
		self.text = text
		self.spinner_generator = self.spinning_cursor()
		if delay and float(delay): self.delay = delay

	def spinner_task(self):
		with term.cbreak(), term.hidden_cursor():
			while self.busy:
				sys.stdout.write(self.text + " " + next(self.spinner_generator))
				sys.stdout.flush()
				time.sleep(self.delay)
				sys.stdout.write("\r")
				sys.stdout.flush()

	def __enter__(self):
		self.busy = True
		threading.Thread(target=self.spinner_task).start()

	def __exit__(self, exception, value, tb):
		self.busy = False
		time.sleep(self.delay)
		print(self.text + " ...done.")
		if exception is not None:
			return False
		
class Indent:
	def __init__(self, text="  "):
		self.lastStdoutWrite = sys.stdout.write
		self.text = text

	def __enter__(self):
		def wrt(string):
			self.lastStdoutWrite(self.text + string)
		sys.stdout.write = wrt

	def __exit__(self, exception, value, tb):
		sys.stdout.write = self.lastStdoutWrite
		if exception is not None:
			return False
		
def waitForKeypress(text="Press any key to continue ..."):
	with term.cbreak(), term.hidden_cursor():
		print(text)
		term.inkey()

def normalizeStringLength(string, size, placeholder=" "):
	l = len(string)
	if l < size:
		return string + "".join([placeholder for _ in range(size - l)])
	elif l > size:
		return string[0:size]
	else:
		return string
	
def slowprint(string, delay=0.01):
	for i in range(len(string)):
		print("\r" + string[0:i + 1] + term.white_on_black("█"), end="")
		
		time.sleep(delay)
	print("\r" + string + " ")

def blink(string, delay=0.25, count=4):
	with term.cbreak(), term.hidden_cursor():
		for x in range(count):
			print("\r" + string, end="")
			time.sleep(delay / 2)
			print("\r" + "".join([" " for x in range(len(string))]), end="")
			time.sleep(delay / 2)
			
class Suppressor:
	def __init__(self):
		self.lastStdoutWrite = sys.stdout.write

	def __enter__(self):
		def wrt(string):
			pass
		sys.stdout.write = wrt

	def __exit__(self, exception, value, tb):
		sys.stdout.write = self.lastStdoutWrite
		if exception is not None:
			return False
		
class Transcript:
	def __init__(self):
		self.lastStdoutWrite = sys.stdout.write
		self.content = []
		
	def __enter__(self):
		def wrt(string):
			self.lastStdoutWrite(string)
			self.content.append(string.strip())
		sys.stdout.write = wrt

	def __exit__(self, exception, value, tb):
		sys.stdout.write = self.lastStdoutWrite
		if exception is not None:
			return False
		
	def read(self):
		return self.content

def combineLists(l1: list[any], l2: list[any]) -> list[tuple[any, any]]:
    output = []
    for x in range(len(l1)):
	    output.append((l1[x], l2[x]))
	    
class Summarizable:
	def summarize(self) -> str:
		print(self.summary())

class Makeable:
	@classmethod
	def make(cls, *args: list, **kwargs: dict) -> object:
		return cls(*args, **kwargs)
	
function = type(combineLists)

class Manufacturable:
	@classmethod
	def manufacture(cls, *args):
		return tuple([cls(x) for x in args])