---
Prerequisites:

1. Install 'Python' (version 3.8.5 or higher) (https://www.python.org/)
2. Add it to 'PATH'
3. Check if it is working by running 'python' command in the console

---
Running program:

1. Open console
2. Write 'python path_to_algorithm.py path_to_input_file' and run exact algorithm, for example if you open console in the main diretory, algorithm is in the file 'algorithm.py' in the 'EXE' diretory and input file is 'file2.txt' in the 'Examples' directory, the command is 'python ./EXE/algorithm.py ./Examples/file2.txt'
3. If you want to run approximate version, add '-a' flag at the end, so for the example above it will be 'python ./EXE/algorithm.py ./Examples/file2.txt -a'
4. Two files will be created in the folder where you have opened your console - 'answer.txt' and 'answer_named.txt'. 'answer_named.txt' contains: information about type of algorithm (approximate/exact), number of common edges (we assumed graph can be directed so if it is not, all edges are counted twice - in both directions), mapping sequence - which vertex of bigger graph correspons to the n-th vetex of smaller one with all excessive vertices added to the end of the sequence, both original graphs, "Mapped Sequence on the Larger Graph" - larger graph where vertices are in the same order as in the mapping sequence, "Common subgraph/supergraph on larger graph" - larger graph with additional edges. Two last graphs are the smallest common supergraph found by the algorithm. If you read only edges marked with '2' and remove all marked with '1' - you will receive the biggest common subgraph found by the algorithm. The file 'answer.txt' contains the same information but ommits original graphs and labels.

---
On laboratory computers:

Preferably RUN ON LINUX, where Python 3.9.7 is installed, so you can go directly to the 'running' part
On Windows Python is present, but not added to PATH - so you have to either use full path to python execuable instead of just 'python' in the command, or open the algorithm file with IDE present there (we do not remember if it is IDLE or Spyder) and run it from there providing arguments (input file and possibly -a flag) in the IDE