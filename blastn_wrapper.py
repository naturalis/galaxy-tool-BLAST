#!/usr/bin/python

"""
blastn_wrapper   V1.0    martenhoogeveen@naturalis.nl
"""
import sys, argparse, os, glob, string
from Bio import SeqIO
from subprocess import call, Popen, PIPE

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='blastn wrapper')
parser.add_argument('-i', '--input', dest='input', type=str,help='blast inputfile', required=True)
parser.add_argument('-it', '--input_type', dest='input_type', type=str,required=True, choices=['fasta', 'zip'])
parser.add_argument('-of', '--folder_output', dest='out_folder', type=str, required=True)
parser.add_argument('-bt', '--blast_task', dest='task', type=str, required=True, choices=['blastn', 'megablast'])
parser.add_argument('-bm', '--max_target_seqs', dest='max_target_seqs', type=str, required=False, nargs='?', default="1")
parser.add_argument('-db', '--blast_database', dest='blast_database', type=str, required=True)
parser.add_argument('-tl', '--taxidlist', dest='taxidlist', type=str, required=False, nargs='?', default="")
parser.add_argument('-id', '--perc_identity', dest='identity', type=str, required=False, nargs='?', default="0")
parser.add_argument('-outfmt', '--outfmt', dest='outfmt', type=str, required=False, nargs='?', default="custom_taxonomy", choices=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','custom_taxonomy'])

args = parser.parse_args()

def admin_log(out=None, error=None, function=""):
    with open(args.out_folder.strip() + "/log.log", 'a') as adminlogfile:
        seperation = 60 * "="
        if out:
            adminlogfile.write(function + " \n" + seperation + "\n" + out + "\n\n")
        if error:
            adminlogfile.write(function + "\n" + seperation + "\n" + error + "\n\n")

def make_output_folders():
    """
    Output en work folders are created. The wrapper uses these folders to save the files that are used between steps.
    args.out_folder contains the path of the output folder
    """
    call(["mkdir", "-p", args.out_folder.strip()])
    call(["mkdir", args.out_folder.strip() + "/files"])
    call(["mkdir", args.out_folder.strip() + "/fasta"])

def unpack_or_cp():
    if args.input_type == "zip":
        zip_out, zip_error = Popen(["unzip", args.input, "-d", args.out_folder.strip() + "/fasta"], stdout=PIPE,stderr=PIPE).communicate()
        admin_log(zip_out, zip_error)
    else:
        cp_out, cp_error = Popen(["cp", args.input, args.out_folder.strip() + "/fasta"], stdout=PIPE,stderr=PIPE).communicate()
        admin_log(cp_out, cp_error)

def check_if_fasta(file):
    if os.path.splitext(file)[1] != ".zip":
        with open(file, "r") as handle:
            fasta = SeqIO.parse(handle, "fasta")
            return any(fasta)
    else:
        return False

def extension_check_and_rename():
    files = [os.path.basename(x) for x in sorted(glob.glob(args.out_folder.strip() + "/fasta/*"))]
    for x in files:
        if check_if_fasta(args.out_folder.strip() + "/fasta/" + x):
            fastafile = os.path.splitext(x)[0].translate((string.maketrans("-. ", "___"))) + ".fa"
            if x != fastafile:
                call((["mv", args.out_folder.strip() + "/fasta/" + x, args.out_folder.strip() + "/fasta/" + fastafile]))
        else:
            admin_log(error="Problems with fasta file, file will be ignored: " + x,function="extension_check")
            call(["rm", args.out_folder.strip() + "/fasta/" + x])
    if not os.listdir(args.out_folder.strip() + "/fasta/"):
        admin_log(error="No fasta file found", function="extension_check")
        sys.exit("No fasta file found")

def file_count_check(files):
    if args.input_type == "fasta" and len(files) > 1:
        admin_log(error="Multiple fasta files found", function="file_count_check")
        sys.exit("Something went wrong, multiple fasta files found")

def create_blast_command(query, output_name):
    if args.outfmt.strip() == "custom_taxonomy":
        outformat = "6 qseqid stitle sacc staxids pident qcovs evalue bitscore"
    else:
        outformat = args.outfmt.strip()
    print args.blast_database.strip().replace(","," ")
    base_command = ["/home/ubuntu/testmapMarten/test/Marten/github_scripts/galaxy-tool-BLAST/ncbi-blast-2.8.0+/bin/blastn", "-query", query, "-db", args.blast_database.strip().replace(","," "), "-task", args.task.strip(),
                    "-max_target_seqs", args.max_target_seqs.strip(), "-num_threads", "2", "-perc_identity", args.identity, "-out",
                    args.out_folder.strip() + "/files/" + output_name.strip(), "-outfmt",
                    outformat]
    if args.taxidlist and args.taxidlist.strip() != "none":
        base_command = base_command + ["-taxidlist", args.taxidlist]
        admin_log(out="taxonomy filter used:" + str(args.taxidlist), error=None, function="blast")
    return base_command

def blast_fasta():
    files = [x for x in sorted(glob.glob(args.out_folder.strip() + "/fasta/*.fa"))]
    #just an extra check
    file_count_check(files)
    for query in files:
        admin_log(out="BLAST: blasting " +str(os.path.basename(query)), error=None, function="blast")
        output_name = "blast_" + os.path.splitext(os.path.basename(query))[0] + ".tabular"
        blast_command = create_blast_command(query, output_name)
        blast_out, blast_error = Popen(blast_command, stdout=PIPE,stderr=PIPE).communicate()
        admin_log(blast_out, blast_error, "blasting:"+str(os.path.basename(query)))

def main():
    make_output_folders()
    unpack_or_cp()
    extension_check_and_rename()
    blast_fasta()





if __name__ == "__main__":
    main()