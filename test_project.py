from project import generate_mutated_sequence, create_iterated_SeqRecord, validate_nucleotide, get_base_range
import pytest


""" Tests: get_base_range(range) """


def test_getBaseRange_valid():
    assert get_base_range(600, "432-550") == [432, 550]


def test_getBaseRange_invalid():
    with pytest.raises(ValueError):
        assert get_base_range(500, "0-400")

    with pytest.raises(ValueError):
        assert get_base_range(500, "300-200")

    with pytest.raises(ValueError):
        assert get_base_range(250, "200-300")


""" Tests: generate_mutated_sequence(full, range, mutation) """


def test_generateMutatedSequence():
    assert generate_mutated_sequence("ATGCTGATGATGTAA", [1, 6], "TGC") == "TGCATGATGTAA"
    assert generate_mutated_sequence("ATGCTGATGATGTAA", [3, 6], "TGC") == "ATTGCATGATGTAA"
    assert generate_mutated_sequence("ATGCTGATGATGTAA", [6, 15], "ATG") == "ATGCTATG"


""" Tests: create_iterated_SeqRecord(n, new_sequence) """


def test_createIteratedSeqRecord():
    record = create_iterated_SeqRecord(3, "1-5", "AGCTGC", "ATGAGCTGCTAA")

    assert record.id == "3"
    assert record.seq == "ATGAGCTGCTAA"
    assert record.description == "Mutated WT Range 1-5 with AGCTGC"


""" Tests: validate_nucleotide(nucleotide) """


def test_validateNucleotide_valid():
    assert validate_nucleotide("A") == True
    assert validate_nucleotide("T") == True
    assert validate_nucleotide("G") == True
    assert validate_nucleotide("C") == True


def test_validateNucleotide_invalid():
    with pytest.raises(ValueError):
        validate_nucleotide("U")

    with pytest.raises(ValueError):
        validate_nucleotide("*")
