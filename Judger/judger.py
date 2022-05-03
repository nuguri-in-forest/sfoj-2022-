from os import system, getcwd,chdir
import subprocess
import base64

Judge_Path = getcwd()
Problem_path = f"{Judge_Path}/problem/%s"
c_compile_path = f"{Judge_Path}/runner/compile_c.sh"
c_runner_path = f"{Judge_Path}/runner/run_c.sh %s %s %d %d %d %d %s"
cxx_compile_path = f"{Judge_Path}/runner/compile_cxx.sh"
cxx_runner_path = f"{Judge_Path}/runner/run_cxx.sh %s %s %d %d %d %d %s"
# compiler_option = {
# 	"C":"gcc /tmp/%s.c -o /tmp/%s -ansi -fno-asm -O2 -Wall -lm --static",
# 	"CXX":"g++ /tmp/%s.cc -o /tmp/%s -ansi -fno-asm -O2 -Wall -lm --static"
# }

class RunningObject:
	def __init__(self, tmp_file_name):
		system("mkdir /tmp/%s"%(tmp_file_name))
		
	def compile(self, lang, source_code, tmp_file_name):
		chdir(Judge_Path)
		self.lang = lang
		self.source_code = source_code
		self.tmp_file_name = tmp_file_name
		if self.lang == 'C':
			TMP_DIR = "/tmp/%s/%s.c"%(tmp_file_name,tmp_file_name)
			CMD = "./runner/compile_c.sh %s"%(tmp_file_name)
			self.EXECFILE='/tmp/%s/%s'%(tmp_file_name, tmp_file_name)
		elif self.lang == 'CXX':
			TMP_DIR = "/tmp/%s/%s.cpp"%(tmp_file_name, tmp_file_name)
			CMD = "./runner/compile_cxx.sh %s"%(tmp_file_name)
			self.EXECFILE='/tmp/%s/%s'%(tmp_file_name, tmp_file_name)
		
		print(TMP_DIR)
		with open(TMP_DIR, "w") as f:
			f.write(self.source_code)

		# return system(compiler_option[self.lang]%(self.tmp_file_name, self.tmp_file_name))

		'''
		0 -> Compile OK
		1 -> Compile Error
		'''
		return system(CMD)

	def running(self, PROBLEM_ID, tmp_file_name, MEMORY_LIMIT, TIME_LIMIT, OUTPUT_LIMIT=10000, SPECIAL_JUDGE=0):
		
		print("[*] debug")
		print("MEMORY_LIMIT : ", MEMORY_LIMIT, type(MEMORY_LIMIT))
		print("TIME_LIMIT : ", TIME_LIMIT, type(TIME_LIMIT))
		print("OUTPUT_LIMIT : ", OUTPUT_LIMIT, type(OUTPUT_LIMIT))
		
		TC_CNT = 0
		with open(Problem_path%(PROBLEM_ID) + "/config", "r") as f:
			while True:
				data = f.readline().strip()
				print("data : ", data)
				if not data:
					print("No TC Cound!!")
					break
				elif "TC_CNT" in data:
					TC_CNT = int(data.split("=")[1])
					break

		print("TC COUNT : ", TC_CNT)

		self.input_dir = Problem_path%(PROBLEM_ID)
		print("[*] input_dir @" + self.input_dir)
		if self.lang == 'C':
			# ./run_c.sh /tmp/847184728471 /home/sfoj/problem/1000 1000 1 10000 1 /tmp/asdf/asdf
			CMD = c_runner_path%(
					"/tmp/" + tmp_file_name,
					self.input_dir,
					MEMORY_LIMIT,
					TIME_LIMIT,
					OUTPUT_LIMIT,
					TC_CNT,
					self.EXECFILE
				)
		elif self.lang == 'CXX':
			CMD = cxx_runner_path%(
					"/tmp/" + tmp_file_name,
					self.input_dir,
					MEMORY_LIMIT,
					TIME_LIMIT,
					OUTPUT_LIMIT,
					TC_CNT,
					self.EXECFILE
				)


		print("###################", CMD)
		proc = subprocess.run(CMD.split(), stdout=subprocess.PIPE)
		return proc.stdout.decode()

"""
C / gcc   gcc-9 -Wall -lm -static -DEVAL -o palindrome -O2 palindrome.c
C++ / g++   g++-9 -Wall -lm -static -DEVAL -o palindrome -O2 palindrome.cpp
C++11 / g++   g++-9 -Wall -lm -static -DEVAL -o palindrome -O2 palindrome.cpp -std=c++11
C++14 / g++   g++-9 -Wall -lm -static -DEVAL -o palindrome -O2 palindrome.cpp -std=c++14
Python 2 / Python 2   python2.7 -c "import py_compile; py_compile.compile(r'palindrome.py')"
Python 3 / Python 3   python3.9 -c "import py_compile; py_compile.compile(r'palindrome.py')"
PyPy / PyPy   pypy -c "import py_compile; py_compile.compile(r'palindrome.py')"
C++17 / g++   g++-9 -Wall -lm -static -DEVAL -o palindrome -O2 palindrome.cpp -std=c++17
Java 11 / Java   javac -J-Xms128m -J-Xmx512m -encoding UTF-8 palindrome.java
Kotlin / Kotlin 1.4   kotlinc-jvm -include-runtime -d palindrome.jar palindrome.kt
"""