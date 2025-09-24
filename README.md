# Synthesis
#### Video Demo: https://youtu.be/TfRSwuQVl2U
#### Description:
Synthesis is a tool designed to ease the process of making many mutations to a single DNA sequence. With my prior lab experience, one of the tasks for my projects was to substitute sequences from one protein into another and I had in the end over 100 different models. Back then, I wished there was a tool that could automate much of the work for me. I was able to complete the substitutions by using Microsoft Excel; however, so much of my time was actually spent debugging my formulas in Microsoft Excel instead of actually performing the substitutions. In addition, Microsoft Excel does not output into a .fasta format which is a widely used file format for DNA/Protein sequences.

### To get help with Synthesis, users run:
_python project.py -h_

### To use Synthesis, users run:
_python project.py -f (or --file) [path to .fasta file]_

1. **Ranges of Sequences to be Mutated**
After running Synthesis, that command loads the sequence contained inside the FASTA source file into the program. Note: I limited the functionality to only use the first sequence in the FASTA file (if unfamiliar, FASTA files can contain multiple sequences, separated by the > character on a new line) because a many-to-many mutation system did not make sense. The goal of this program is to take a one-to-many approach, with one source sequence producing many mutated sequences of that source. Next, users are prompted with a welcome page that indicates what file has been opened and how many base pairs the sequence contains. Users are expected to have predetermined ranges in mind for where in the source sequence they want to mutate and insert a new sequence inside. For example, if my sequence is 350 bp long, and I know I want to mutate the 30-54, 30-81, and 30-105 regions, I would enter each in the “n-n” format and press enter after each one. When done with ranges, type “q” and press enter.

2. **Mutation Insert Sequences**
Secondly, users are then prompted to enter insert sequences. I want each of those regions above to contain these sequences: ATGCAGCTGACTGAC, ATGCAGCTGACTGACATG, and “ATGCAGCTGACTGACATGCAG. Click enter after typing each sequence, and type “q” then press enter when done with sequences. If you notice, the sequences above vary minimally – this tool is specifically for use cases where high-throughput screening of mutations are needed to identify changes in biomolecular function (such as WT vs mutated proteins). As with my prior lab, my mutations were sometimes many more base pairs longer than these, but I hope that showcases the use for this program effectively.

3. **Output**
Now that both inputs are finished, the user is shown a confirmation for the output file. This is a FASTA file and contains every single mutated sequence based off of those conditions, using the source FASTA file sequence as a basis. The file is saved to the current directory. Each sequence will follow chronological order as with how the user inputted the data: for example, the first sequence will be the first range and first mutant sequence insert. The format of the sequence header of the FASTA is: >{#} Mutated WT Range {range} with {sequence_insert}.

The Synthesis Project Folder Contains:

**project.py**
-	This is the main file and can be thought of as the application’s “executable.” It orchestrates calls to functions written in setup.py and mutation.py to make a working program. In detail, analyzes the command line argument for input file, parses through the source FASTA file, handles calls to get input from the user, calls for all the mutations to get made, and finally exports of all those new sequences into one output file. Mutation logic includes the broad loops for iterating through each range with a nested loop through each mutation sequence insert. From there, it calls for the actual mutation to occur which generates a new sequence, adds it to a growing sequence object list, and ultimately returns the list to the main function.

**test_project.py**
-	This file contains broad unit tests for many of the functions in setup.py and mutations.py. It can be used by running: python test_synthesis.py

**requirements.txt**
-	Lists all the Python libraries for the program

_sampledata_ (folder)
-	**atpsynthasef1subunitalpha.fasta** > sample DNA sequence data for one of my favorite proteins, ATP Synthase! Retrieved from _https://www.ncbi.nlm.nih.gov/gene/498_
-	**first350atpsynthase.fasta** > smaller subsection of the above file, easier to see if program worked!

**README.md**
-	This file!

#### Note: I had to refactor everything back into project.py for submit50 as I originally made this project with separate python files such as "mutation.py" and "setup.py" seen in my video.
