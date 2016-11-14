Antonio Rafael Umali
CS 534 HW2

To run HW:
	In Terminal: 
	Type "python (filename) (inputfile)"
	example:
	python sim_anneal.py input.txt

	To run seperate configuration checker:
		python checker.py (input file)

	To run simulated annealing:
		python sim_anneal.py (input file)

	To run A*:
		python a_star.py (input file)

	To run CSP:
		python CSP.py (input file)

	After running a file, you will be given options in the form
	of letters, which are case-sensitive.
	Simply type in the letter corresponding to which option you
	want to take and then press enter

	There are 13 test files included in the folder:
		5 for 4x4, 5 for 9x9, and 3 for 16x6
	They are named in the convention:
		(dim)x(dim)_(n).txt
	Where dim is either 4, 9, or 16 and n is in the range
	[1,5] for 4x4 and 9x9 and in [1,3] for 16x16
