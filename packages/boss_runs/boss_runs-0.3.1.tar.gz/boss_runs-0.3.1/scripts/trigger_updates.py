from pathlib import Path
import numpy as np
import sys


DIR = Path(sys.argv[1])
DIR_C = DIR / "contigs"
DIR_M = DIR / "masks"



def random_id(k: int = 20) -> str:
    """
    Generate a random alphanumeric ID of length k.

    :param k: The length of the ID.
    :type k: int
    :return: The generated random ID.
    :rtype: str
    """
    import random
    import string
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return x


def gen_dummy_seqs(nseqs):
    # fill a dictionary with n random contigs
    seqs = {}
    for i in range(nseqs):
        i_id = random_id()
        i_len = np.random.randint(1000, 10000, size=1)
        i_seqlist = np.random.choice(['A', 'C', 'G', 'T'], size=i_len, replace=True)
        i_seq = "".join(i_seqlist)
        seqs[i_id] = i_seq
    return seqs



def seqs_to_file(seqs):
    with open(f"{DIR_C}/aeons.fa", "w") as dfa:
        for header, seq in seqs.items():
            dfa.write(f'>{header}\n{seq}\n')



def gen_dummy_strat(seqs):
    contig_strats = {}
    for header, seq in seqs.items():
        random_strat = np.random.choice([0, 1], size=(len(seq), 2), replace=True)
        contig_strats[header] = random_strat

    np.savez(DIR_M / "boss.npz", **contig_strats)



sequences = gen_dummy_seqs(5)
seqs_to_file(sequences)
gen_dummy_strat(sequences)


