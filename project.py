import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os


def main():
    """
    Given an input sequence, the user specifies ranges of the sequence they would like to be replaced.
    Then, they input the specific sequences they would like to insert in each of those ranges
    Outputs a FASTA file with all the sequences.
    """

    # Get FASTA input file from command line argument
    input_FASTA_path = handle_commandline_file_input()

    # Parse FASTA input file for first sequence (only supports one sequence from input file)
    sequence = next(SeqIO.parse(input_FASTA_path, "fasta"))
    seq_length = len(sequence.seq)

    # Retrieve input file name + extension
    input_FASTA_file = os.path.basename(input_FASTA_path)

    # Print info for user
    print_info(input_FASTA_file, seq_length)

    # Get ranges from user
    range_prompt = "-------------- Input Sequence Ranges to be Mutated (q to exit) --------------\nExample Usage: 300-550"
    wt_ranges = get_user_input("Range", range_prompt, seq_length=seq_length)

    # Get insert sequences
    sequence_prompt = "------------- Input Insert Sequences to Mutate With (q to exit) -------------\nExample Usage: ATGTAA"
    insert_sequences = get_user_input("Sequence", sequence_prompt)

    # Perform mutation operations
    final_sequence_records = mutate_sequences(sequence.seq, wt_ranges, insert_sequences)

    # Output all new sequences into one FASTA file
    with open(f"mutated_{input_FASTA_file.replace(".fasta", "")}.fasta", "w") as output_FASTA:
        SeqIO.write(final_sequence_records, output_FASTA, "fasta")

    # Indicate successful output
    print(f"SUCCESS: mutated_{input_FASTA_file}")


def handle_commandline_file_input():
    """ Returns file input str from command line """
    parser = argparse.ArgumentParser(description="Quickly mutate DNA sequences in batches")
    parser.add_argument("-f", "--file", type=str, required=True, help="Path to FASTA file (.fasta)")

    args = parser.parse_args()

    return args.file


def mutate_sequences(full_sequence, wt_ranges, mutated_sequences):
    """ Returns list of all mutated sequences """
    new_sequences = []

    # Loop through each inputted wild-type sequence
    for wt_range in wt_ranges:
        # Loop through each mutated sequence and insert into full sequence
        for count, mutated_sequence in enumerate(mutated_sequences, start=1):
            new_sequence = generate_mutated_sequence(full_sequence, wt_range, mutated_sequence)
            new_sequences.append(create_iterated_SeqRecord(count, wt_range, mutated_sequence, new_sequence))

    return new_sequences


def generate_mutated_sequence(full, range_list, mutation):
    """ Returns fully mutated sequence str """
    # range_list[0] is start, range_list[1] is end
    return full[:range_list[0] - 1] + mutation + full[range_list[1]:]


def create_iterated_SeqRecord(n, wt_range, mutated_sequence, new_sequence):
    """ Returns new SeqRecord object with mutated full sequence """
    seq = Seq(new_sequence)

    return SeqRecord(seq, id=str(n), description=f"Mutated WT Range {wt_range} with {mutated_sequence}")


def validate_nucleotide(nucleotide):
    """ Raises ValueError if nucleotide is not valid """
    valid_nucleotides = ["A", "T", "G", "C"]

    if nucleotide not in valid_nucleotides:
        raise ValueError("\nERROR: The sequence must only include DNA nucleotides A, T, G, C\n")

    return True


def get_base_range(seq_length, range):
    """ Returns list in format [start, end] """
    start, end = map(int, range.split("-"))

    if end < start:
        raise ValueError("\nERROR: End value cannot be smaller than start value\n")
    if start < 1 or end < 1:
        raise ValueError("\nERROR: DNA indexing starts at 1\n")
    if end > seq_length:
        raise ValueError(
            f"\nERROR: End value exceeds the length of the input sequence's {seq_length} bp\n")

    return [start, end]


def get_user_input(type, prompt, seq_length=None):
    """ Returns list of user's input: [str] for "Sequence" type, [[start, end]] for "Range" type """
    user_inputs = []

    print(prompt)
    print()

    while True:
        # Update user with current list of inputted sequences
        print(f"Current {type}s: {user_inputs}")

        # Get input from user
        user_input = input(f"{type}: ").strip().upper()

        # Ensure blank input is not tolerated
        if not user_input:
            continue
        # Quit out of input
        if user_input == "Q":
            if user_inputs == []:
                print(
                    f"\nERROR: Must have at least one valid {type.lower()} before quiting input.\n")
                continue
            else:
                print()
                break

        match type:
            case "Sequence":
                # Validate input for nucleotides
                for nucleotide in user_input:
                    try:
                        valid_nucleotide = validate_nucleotide(nucleotide)
                    except ValueError as e:
                        print(e)
                        valid_nucleotide = False
                        break

                # Ask user for new input if nucleotide is invalid
                if not valid_nucleotide:
                    continue
            case "Range":
                try:
                    user_input = get_base_range(seq_length, user_input)
                except ValueError as e:
                    print(e)
                    continue

        # Add input to list if valid
        user_inputs.append(user_input)
        print()

    return user_inputs


def print_info(filename, seq_length):
    """ Prints application info to user """
    print()
    print("------------------------ Synthesis by Addison Crider ------------------------")
    print()
    print(f"Successfully Opened: {filename}  |  Sequence Length: {seq_length} bp")
    print()
    print("1. Input base ranges for the regions of the input file sequence to be mutated.")
    print("2. Input insert sequences that will replace those sequences in the ranges you provided.")
    print()
    print(f"All the mutated sequences will be stored in a single file --> mutated_{filename}")
    print()


if __name__ == "__main__":
    main()
