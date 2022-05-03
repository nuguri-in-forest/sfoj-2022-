import random

last = 2
for i in range(last+1, last+10):
	n1 = random.randint(-10000, 10000)
	n2 = random.randint(-10000, 10000)
	_IN = ""
	_IN += str(n1) + " " + str(n2) + "\n"

	_OUT = str(n1+n2) + "\n"

	with open(f"{i}.in", "w") as f:
		f.write(_IN)

	with open(f"{i}.out", "w") as f:
		f.write(_OUT)

	