
# -*- coding:utf-8 -*-

import os
import re
import sys
import pandas as pd
from cvmblaster.blaster import Blaster
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIXML

# from Bio.Blast import NCBIWWW
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbimakeblastdbCommandline


class mlst():
    def __init__(self, inputfile, database, output, threads, minid=95, mincov=90):
        self.inputfile = os.path.abspath(inputfile)
        self.database = database
        self.minid = int(minid)
        self.mincov = int(mincov)
        self.temp_output = os.path.join(os.path.abspath(output), 'temp.txt')
        self.threads = threads

    def biopython_blast(self):
        # cline = NcbiblastnCommandline(query=self.inputfile, db=self.database, dust='no', ungapped=True,
        #                               evalue=1E-20, out=self.temp_output,  # delete culling_limit parameters
        #                               outfmt="6 sseqid slen length nident",
        #                               task='dc-megablast',
        #                               perc_identity=self.minid, max_target_seqs=1000000,
        #                               num_threads=self.threads)
        cline = NcbiblastnCommandline(query=self.inputfile, db=self.database, dust='no', ungapped=True,
                                      evalue=1E-20, out=self.temp_output,  # delete culling_limit parameters
                                      outfmt='"6 sseqid slen length nident"',
                                      # task='dc-megablast',
                                      perc_identity=self.minid, max_target_seqs=1000000,
                                      num_threads=self.threads)
        # print(cline)
        stdout, stderr = cline()
        df = pd.read_csv(self.temp_output, sep='\t', names=[
            'sseqid', 'slen', 'length', 'nident'])
        # print(df)

        result = {}
        for i, row in df.iterrows():
            gene, num = re.match(
                '^(\w+)[_-](\d+)', row['sseqid']).group(1, 2)
            # print(gene)
            num = int(num)
            hlen = row['slen']
            alen = row['length']
            nident = row['nident']
            if nident * 100 / hlen >= self.mincov:
                # if sch not in result.keys():  # check if sch is the key of result
                #     result[sch] = {}
                # resolve the bug that could not get exactly matched allele
                if hlen == alen & nident == hlen:  # exact match
                    if gene in result.keys():

                        if not re.search(r'[~\?]', str(result[gene])):
                            old_num = int(result[gene])
                            if num < old_num:
                                # print(f'{num}\t{old_num}')
                                result[gene] = num
                                print(
                                    f'Found additional allele match, replace {gene}:{old_num} -> {num}')
                            else:
                                print(
                                    f'Found additional allele match, but the allele number {num} is greater or equal to stored one {gene}:{old_num}, skip...')
                        else:  # replace not perfect match
                            result[gene] = num
                    else:
                        result[gene] = num
                # new allele
                elif (alen == hlen) & (nident != hlen):
                    # print('xx')
                    if gene not in result.keys():
                        # print('xxx')
                        result[gene] = f'~{num}'
                    else:
                        next
                    # result[sch] = mlst
                elif (alen != hlen) & (nident == hlen):  # partial match
                    # print('xxxx')
                    if gene not in result.keys():
                        result[gene] = f'{num}?'
                else:
                    next
        # remove temp blastn output file
        os.remove(self.temp_output)
        return result

    @staticmethod
    def makeblastdb(file):
        cline = NcbimakeblastdbCommandline(
            dbtype="nucl", title='cgMLST',
            hash_index=True,
            parse_seqids=True,
            input_file=file)
        print(f"Making database...")
        stdout, stderr = cline()
        print(stdout)

    @staticmethod
    def is_fasta(file):
        """
        chcek if the input file is fasta format
        """
        try:
            with open(file, "r") as handle:
                fasta = SeqIO.parse(handle, "fasta")
                # False when `fasta` is empty, i.e. wasn't a FASTA file
                return any(fasta)
        except:
            return False
