#!/usr/bin/python3

# -*- coding:utf-8 -*-

import os
import re
import sys
import argparse
import subprocess
import pandas as pd
from Bio import SeqIO
import shutil
# from .cgmlst_core import mlst
from tabulate import tabulate
from cvmblaster.blaster import Blaster
from cvmcore.cvmcore import cfunc


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='cvmcgmlst -i <genome assemble directory> -o <output_directory> \n\nAuthor: Qingpo Cui(SZQ Lab, China Agricultural University)\n')

    # Add subcommand
    subparsers = parser.add_subparsers(
        dest='subcommand', title='cvmcgmlst subcommand')
    show_database_parser = subparsers.add_parser(
        'show_db', help="<show the list of all available database>")

    init_db_parser = subparsers.add_parser(
        'init', help='<initialize the reference database>')

    add_db_parser = subparsers.add_parser(
        'create_db', help='<add custome database, use cvmcgmlst createdb -h for help>')

    add_db_parser.add_argument(
        '-file', help='<The fasta format reference file>')
    add_db_parser.add_argument(
        '-name', help="<The database name parameter that could be used in 'cvmcgmlst -db [name]'>")
    add_db_parser.add_argument(
        '-force', default=False, action="store_true", help='<force create database>')

    parser.add_argument(
        "-i", help="<input_file>: the PATH of assembled genome file")
    parser.add_argument('-db', help="<database_path>: path of cgMLST database")
    parser.add_argument("-o", help="<output_directory>: output PATH")
    parser.add_argument('-minid', default=95,
                        help="<minimum threshold of identity>, default=95")
    parser.add_argument('-mincov', default=90,
                        help="<minimum threshold of coverage>, default=90")
    parser.add_argument(
        '-t', default=8, help='<number of threads>: default=8')
    parser.add_argument('-v', '--version', action='version',
                        version='Version: ' + get_version("__init__.py"), help='Display version')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_rel_path():
    """
    Get the relative path
    """
    here = os.path.abspath(os.path.dirname(__file__))
    return here


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def initialize_db():
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    # print(database_path)
    fsa_files = 0
    for file in os.listdir(database_path):
        # print(file)
        if file.endswith('.fsa'):
            fsa_files += 1
            file_path = os.path.join(database_path, file)
            file_base = os.path.splitext(file)[0]
            out_path = os.path.join(database_path, file_base)
            seq_type = cfunc.check_sequence_type(file_path)
            if seq_type == 'DNA':
                Blaster.makeblastdb(file_path, out_path, db_type='nucl')
            elif seq_type == 'Amino Acid':
                Blaster.makeblastdb(file_path, out_path, db_type='prot')
            else:
                print('Unknown sequence type, exit ...')
        else:
            next
    if fsa_files == 0:
        print('No valid reference file exist...')
        sys.exit(1)


def create_db(fasta_file, db_name, force=False):
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    # 定义源文件路径和目标路径
    dbfile = f'{db_name}.fsa'
    dest_file = os.path.join(database_path, dbfile)

    if dbfile not in os.listdir(database_path):
        # dest_file = os.path.join(database_path, fname)
        shutil.copy(fasta_file, dest_file)
        blastdb_out = os.path.join(database_path, db_name)
        print(f"Add {db_name} to database...")
        # print(blastdb_out)
        Blaster.makeblastdb(dest_file,  blastdb_out, db_type='nucl')
    else:
        if force:
            os.remove(dest_file)
            shutil.copy(fasta_file, dest_file)
            blastdb_out = os.path.join(database_path, db_name)
            print(f"Add {db_name} to database...")
            # print(blastdb_out)
            Blaster.makeblastdb(dest_file,  blastdb_out, db_type='nucl')
        else:
            print(
                f"{db_name} already exist in database, Please make sure or give another db_name")
            sys.exit(1)
    # else:
    #     print("Wrong suffix with input fasta file")
    #     sys.exit(1)


def check_db():
    """
    ruturn database list
    """
    db_list = []
    database_path = os.path.join(
        os.path.dirname(__file__), f'db')
    for file in os.listdir(database_path):
        if file.endswith('.fsa'):
            db_name = os.path.splitext(file)[0]
            db_list.append(db_name)
    return db_list


def show_db_list():
    """
    Convert the ResBlaster database to tidy dataframe
    Paramters
    ----------

    Returns
    ----------
    A tidy dataframe contains the blast database name and No. of seqs in database and the last modified date

    """
    here = get_rel_path()
    db_path = os.path.join(here, 'db')
    db_list = []
    for file in os.listdir(db_path):
        file_path = os.path.join(db_path, file)
        if file_path.endswith('.fsa'):
            db_dict = {}
            fasta_file = os.path.basename(file_path)
            file_base = os.path.splitext(fasta_file)[0]
            num_seqs = len(
                [1 for line in open(file_path) if line.startswith(">")])
            update_date = cfunc.get_mod_time(file_path)
            db_dict['DB_name'] = file_base
            db_dict['No. of seqs'] = num_seqs
            db_dict['Update_date'] = update_date
            db_list.append(db_dict)
        else:
            next

    db_df = pd.DataFrame(db_list)
    db_df = db_df.sort_values(by='DB_name', ascending=True)
    tidy_db_df = tabulate(db_df, headers='keys', showindex=False)
    return print(tidy_db_df)


def main():
    # df_all = pd.DataFrame()
    args = args_parse()
    if args.subcommand is None:
        # print('Start cgMLST analysis ...')
        # threads
        threads = args.t
        # print(threads)

        minid = args.minid
        mincov = args.mincov

        # check if the output directory exists
        if not os.path.exists(args.o):
            os.mkdir(args.o)
        output_path = os.path.abspath(args.o)
        # print(output_path)

        # get the database path
        database = args.db

        # check if input db is in dblist
        exist_database = check_db()

        if database in exist_database:
            database_path = os.path.join(
                os.path.dirname(__file__), f'db/{args.db}')
            # seq_type = cfunc.check_sequence_type(f'{database_path}.fsa')
        else:
            print(
                f'Could not found {database} in {exist_database}, Please check your input or view database list using "cvmcgmlst show_db"')
            sys.exit(1)

        # decide blast type
        # print(f'The database type is {seq_type} \n')
        # if seq_type == 'Amino Acid':
        #     blast_type = 'blastx'
        # else:
        #     blast_type = 'blastn'

        # get the input assembled genome path
        inputfile = os.path.abspath(args.i)
        file_base = str(os.path.basename(os.path.splitext(inputfile)[0]))
        output_filename = file_base + '_tab.txt'

        # Create the outfile
        outfile = os.path.join(output_path, output_filename)

        # print(file_path)
        if os.path.isfile(inputfile):
            # print("TRUE")
            if cfunc.is_fasta(inputfile):
                print(f'Processing {inputfile}')
                # cvmcgmlst is blastn, so here I ignore the blast_type parameter in mlst_blast
                result = Blaster(inputfile, database_path,
                                 output_path, threads, minid, mincov).mlst_blast()

                # print(df)
                if len(result) != 0:
                    df = pd.DataFrame.from_dict(result, orient='index')
                    df.index.name = 'Loci'
                    df.rename(columns={0: 'Allele_Num'}, inplace=True)
                    df_trans = df.T
                    df_trans.index = [file_base]

                    # df_out['FILE'] = file_base
                    # order = list(reversed(df.columns.to_list()))
                    # df = df[order]
                    # print(df)
                    df.to_csv(outfile, sep='\t', index=True)
                    print(
                        f"Finishing process {inputfile}: writing results to " + str(outfile))
                else:
                    print('Empty result')
                    df = pd.DataFrame(columns=['Loci', 'Allele_Num'])
                    df.to_csv(outfile, sep='\t')
                    # print(df)
                #     df.index.name = 'Loci'
                #     df_trans = df.T
                #     df_trans.index = [file_base]
                # df_all = pd.concat([df_all, df_trans])
        else:
            print('Could not find your input file, exit...')
    elif(args.subcommand == 'show_db'):
        show_db_list()
    elif(args.subcommand == 'init'):
        initialize_db()
    elif(args.subcommand == 'create_db'):
        custome_db_file = os.path.abspath(args.file)
        databasename = args.name
        force = args.force
        create_db(custome_db_file, databasename, force)
        print(f'Adding {args.file} to reference database...')
        # print(f'Initializing reference data...')
        # initialize_db()
    else:
        print(
            f'{args.subcommand} do not exists, please using "ResBlaster -h" to show help massage.')


if __name__ == '__main__':
    main()
