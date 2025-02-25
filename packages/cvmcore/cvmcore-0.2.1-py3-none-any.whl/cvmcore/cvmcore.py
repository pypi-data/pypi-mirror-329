import os
import sys
import time

# data process
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, complete, to_tree
from scipy.spatial.distance import squareform
from tabulate import tabulate
from io import StringIO
import warnings
# from Bio.Blast import NCBIWWW
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=DeprecationWarning)
    from Bio import SeqIO
    from Bio import Phylo
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Blast import NCBIXML


# matplotlib
import matplotlib
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, FancyArrow
from matplotlib.transforms import Affine2D
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.collections as mpcollections
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from typing import Optional, List, Dict, Union, Tuple

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['svg.fonttype'] = 'none'


class cfunc():
    pass

    @staticmethod
    def is_fasta(file):
        """
        chcek if the input file is fasta format
        """
        try:
            with open(file, "r") as handle:
                records = SeqIO.parse(handle, "fasta")
                # False when `fasta` is empty, i.e. wasn't a FASTA file
                for record in records:
                    pass
            return true
        except:
            print(f'The input file {file} is not a valid fasta file.')
            return False

    def get_mod_time(file):
        """
        Return the last modified time of file as YYYY-MM-DD string format.
        Parameters
        ----------
        file :
            file path string
        Returns
        ----------
        Raises
        ----------
        Notes
        ----------
        References
        ----------
        See Also
        ----------
        Examples
        ----------
        """
        file = os.path.abspath(file)
        md_time = os.stat(file).st_mtime
        lst_mod_time = time.strftime("%Y-%m-%d", time.localtime(md_time))
        return lst_mod_time

    def check_sequence_type(file_path):
        """
        Check the input file type (DNA or Amino Acid)
        """
        try:
            # Read the sequence from the file
            records = list(SeqIO.parse(file_path, "fasta"))
            if not records:
                return "Unknown"

            sequence = str(records[0].seq).upper()

            # Define sets of characters for DNA and amino acids
            dna_chars = set("ATCG")
            amino_acid_chars = set("ACDEFGHIKLMNPQRSTVWY")

            # Check if the sequence contains only DNA characters
            if set(sequence).issubset(dna_chars):
                return "DNA"
            # Check if the sequence contains only amino acid characters
            elif set(sequence).issubset(amino_acid_chars):
                return "Amino Acid"
            else:
                return "Unknown"
        except Exception as e:
            return f"Error: {e}"

    @staticmethod
    def alleles2ref(files_dir: str, outpath: str, outname: str):
        """
        Create cgMLST reference sequences using fasta files downloaded from "https://www.cgmlst.org/"
        """
        files_dir = os.path.abspath(files_dir)
        new_records = []
        for file in os.listdir(files_dir):
            # print(file)
            if file.endswith('.fasta'):
                file_base = file.split('.')[0]
                # print(file_base)
                file = os.path.join(files_dir, file)
                records = SeqIO.parse(file, 'fasta')
                for record in records:
                    record.id = file_base + "_" + record.id
                    record.name = file_base + "_" + record.name
                    record.description = ''
                    # print(record.id)
                    # print(record)
                    new_records.append(record)

        # check if outpath exists
        outdir = os.path.abspath(outpath)
        if not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=True)

        # Specify the output file nameå
        output_file = f'{outname}.fsa'
        output_file = os.path.join(outdir, output_file)
        # Write the modified sequences to the new fasta file
        with open(output_file, "w") as output_handle:
            SeqIO.write(new_records, output_handle, "fasta")
