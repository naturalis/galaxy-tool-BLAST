#!/usr/bin/env python

"""
blaster.py  -  Parallel blastn runner
Splits the query FASTA into chunks of CHUNK_SIZE sequences and executes
up to MAX_PARALLEL BLAST jobs concurrently.
"""

import sys
import os
import re
import argparse
import glob
from Bio import SeqIO
from subprocess import Popen, PIPE
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------------------------
# CLI arguments (mirrors blastn_wrapper.py so the shell wrapper can call both)
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Parallel blastn runner")
parser.add_argument("-i",    "--input",               dest="input",                type=str, required=False,
                    default=None,
                    help="Input FASTA file (required unless --annotate_only is used)")
parser.add_argument("-of",   "--output_folder",       dest="out_folder",           type=str, required=True,
                    help="Output folder")
parser.add_argument("-bt",   "--blast_task",          dest="task",                 type=str, required=False,
                    default=None, choices=["blastn", "megablast"])
parser.add_argument("-bm",   "--max_target_seqs",     dest="max_target_seqs",      type=str, required=False,
                    default="1")
parser.add_argument("-dbt",  "--blast_database_type", dest="blast_database_type",  type=str, required=False,
                    default=None, choices=["local", "user"])
parser.add_argument("-db",   "--blast_database",      dest="blast_database",       type=str, required=False,
                    default=None)
parser.add_argument("--annotate_only",                dest="annotate_only",        type=str, required=False,
                    default=None,
                    help="Path to an existing BLAST tabular file. Skips BLAST and only adds "
                         "#Source and #Taxonomy columns. Requires --output_folder and optionally --taxdump.")
parser.add_argument("-tl",   "--taxidlist",           dest="taxidlist",            type=str, required=False,
                    default="")
parser.add_argument("-id",   "--perc_identity",       dest="identity",             type=str, required=False,
                    default="0")
parser.add_argument("-cov", "--coverage",              dest="coverage",             type=str, required=False,
                    default="0")
parser.add_argument("-outfmt", "--outfmt",            dest="outfmt",               type=str, required=False,
                    default="custom_taxonomy",
                    choices=["0","1","2","3","4","5","6","7","8","9","10","11","custom_taxonomy"])
parser.add_argument("-cs",  "--chunk_size",           dest="chunk_size",           type=int, required=False,
                    default=128,
                    help="Number of sequences per BLAST chunk (default: 128)")
parser.add_argument("-p",   "--parallel",             dest="max_parallel",         type=int, required=False,
                    default=None,
                    help="Maximum number of parallel BLAST jobs. Overrides --max_cpus if set.")
parser.add_argument("-num_threads", "--num_threads",      dest="num_threads",          type=int, required=False,
                    default=1,
                    help="Number of threads per BLAST job (default: 2)")
parser.add_argument("--max_cpus",                         dest="max_cpus",             type=int, required=False,
                    default=None,
                    help="Total CPUs available (e.g. Galaxy job allocation). "
                         "Sets --parallel to max_cpus // num_threads when --parallel is not given.")
parser.add_argument("--taxdump",                          dest="taxdump",              type=str, required=False,
                    default=None,
                    help="Path to taxdump directory for taxonkit taxonomy annotation. "
                         "When provided, appends a #Taxonomy column to the final output.")
args = parser.parse_args()

# Validate: BLAST-specific args are required unless --annotate_only is set
if args.annotate_only is None:
    missing = [name for flag, name in [("-i/--input", "input"), ("-bt/--blast_task", "task"),
                                        ("-db/--blast_database", "blast_database"),
                                        ("-dbt/--blast_database_type", "blast_database_type")]
               if getattr(args, name) is None]
    if missing:
        parser.error(f"The following arguments are required when not using --annotate_only: {', '.join(missing)}")

# Derive max_parallel from max_cpus if --parallel was not explicitly provided
if args.max_parallel is None:
    if args.max_cpus is not None:
        args.max_parallel = max(1, args.max_cpus // args.num_threads)
    else:
        args.max_parallel = 8  # fallback default


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def log(out=None, error=None, function=""):
    log_path = os.path.join(args.out_folder.strip(), "log.log")
    sep = "=" * 60
    with open(log_path, "a") as f:
        if out:
            f.write(f"{function} \n{sep}\n{out}\n\n")
        if error:
            msg = error.decode() if isinstance(error, bytes) else error
            f.write(f"{function}\n{sep}\n{msg}\n\n")


# ---------------------------------------------------------------------------
# Step 1 – Split input FASTA into chunk files
# ---------------------------------------------------------------------------
def split_fasta_into_chunks(input_file, chunk_dir):
    """
    Parse *input_file* and write one FASTA file per CHUNK_SIZE sequences
    into *chunk_dir*.  Returns the list of written chunk file paths.
    """
    os.makedirs(chunk_dir, exist_ok=True)

    chunk_files = []
    buffer = []
    chunk_index = 0

    with open(input_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            buffer.append(record)
            if len(buffer) == args.chunk_size:
                chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_index:04d}.fa")
                SeqIO.write(buffer, chunk_path, "fasta")
                chunk_files.append(chunk_path)
                log(out=f"Written chunk {chunk_index:04d} ({len(buffer)} sequences) -> {chunk_path}",
                    function="split_fasta")
                buffer = []
                chunk_index += 1

    # Write any remaining sequences as a final (smaller) chunk
    if buffer:
        chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_index:04d}.fa")
        SeqIO.write(buffer, chunk_path, "fasta")
        chunk_files.append(chunk_path)
        log(out=f"Written chunk {chunk_index:04d} ({len(buffer)} sequences) -> {chunk_path}",
            function="split_fasta")

    log(out=f"Total chunks: {len(chunk_files)}", function="split_fasta")
    return chunk_files


# ---------------------------------------------------------------------------
# Step 2 – Build and run a single BLAST command for one chunk
# ---------------------------------------------------------------------------
def build_blast_command(query_path, output_path):
    if args.outfmt.strip() == "custom_taxonomy":
        outformat = "6 qseqid stitle sacc staxid pident qcovs evalue bitscore"
    else:
        outformat = args.outfmt.strip()

    cmd = [
        "blastn",
        "-query",          query_path,
        "-db",             args.blast_database.strip().replace(",", " "),
        "-task",           args.task.strip(),
        "-num_threads",    str(args.num_threads),
        "-max_hsps",       "1",
        "-perc_identity",  args.identity,
        "-out",            output_path,
        "-outfmt",         outformat,
    ]

    if args.taxidlist and args.taxidlist.strip() not in ("", "none"):
        cmd += ["-taxidlist", args.taxidlist.strip()]

    if args.outfmt.strip() in ("custom_taxonomy", "6"):
        cmd += ["-max_target_seqs", args.max_target_seqs.strip()]
    elif args.outfmt.strip() in ("0", "8", "11"):
        cmd += ["-num_alignments", args.max_target_seqs.strip()]

    return cmd


def run_blast_chunk(chunk_path):
    """Run BLAST for a single chunk file; returns the output tabular path."""
    chunk_name = os.path.splitext(os.path.basename(chunk_path))[0]
    output_path = os.path.join(args.out_folder.strip(), "files", f"blast_{chunk_name}.tabular")
    cmd = build_blast_command(chunk_path, output_path)

    log(out=f"Running: {' '.join(cmd)}", function=f"blast:{chunk_name}")
    out, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    log(out=out.decode() if out else None, error=err if err else None,
        function=f"blast:{chunk_name}")
    return output_path


# ---------------------------------------------------------------------------
# Step 3 – Merge chunk results and optionally apply coverage filter
# ---------------------------------------------------------------------------
def coverage_filter(tabular_path):
    filtered = tabular_path + "_cov"
    with open(tabular_path, "r") as src, open(filtered, "w") as dst:
        for line in src:
            if float(line.split("\t")[5]) >= float(args.coverage):
                dst.write(line)
    os.replace(filtered, tabular_path)


def merge_results(result_files, final_output):
    header = "#Query ID\t#Subject\t#Subject accession\t#Subject Taxonomy ID\t#Identity percentage\t#Coverage\t#evalue\t#bitscore\n"
    with open(final_output, "w") as out:
        out.write(header)
        for path in sorted(result_files):
            if not os.path.isfile(path):
                continue
            with open(path, "r") as src:
                out.write(src.read())
    log(out=f"Merged {len(result_files)} result files -> {final_output}", function="merge")


# ---------------------------------------------------------------------------
# Step 4 – Annotate taxonomy
# ---------------------------------------------------------------------------
SUBJECT_COL = 1   # stitle  – contains BOLD/UNITE taxonomy when present
ACC_COL     = 2   # sacc    – accession used for source DB detection
TAXID_COL   = 3   # staxid  – numeric NCBI taxid

# Prefix → standard rank mapping for BOLD/UNITE subject titles
BOLD_PREFIX_MAP = {
    "k__": "kingdom",
    "p__": "phylum",
    "c__": "class",
    "o__": "order",
    "f__": "family",
    "g__": "genus",
    "s__": "species",
}
RANK_ORDER = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]

TAXONKIT_FORMAT = "{kingdom} / {phylum} / {class} / {order} / {family} / {genus} / {species}"


def _is_bold_unite(subject_title):
    """Return True when the subject title contains BOLD/UNITE-style taxonomy."""
    return "k__" in subject_title


def _is_silva(accession):
    """Return True for SILVA accessions: GenBank ID + two positional suffixes, e.g. AB015360.1.1526"""
    return bool(re.match(r'^[A-Z]{1,3}\d{5,8}\.\d+\.\d+$', accession.strip().upper()))


def _detect_source(accession):
    """
    Infer the source database from the accession string.
    Returns a short label: 'BOLD', 'UNITE', 'SILVA', 'RefSeq', 'GenBank', or 'Unknown'.
    """
    acc = accession.strip()
    if acc.lower().startswith("silva|"):
        return "SILVA"
    if acc.upper().startswith("BOLD|") or "|COI-" in acc or ("|ITS" in acc and "BOLD" in acc):
        return "BOLD"
    if acc.startswith("SH") or "|SH" in acc or acc.endswith("FU"):
        return "UNITE"
    if any(acc.upper().startswith(p) for p in ("NR_", "NC_", "NG_", "NM_", "NW_", "NT_")):
        return "RefSeq"
    if _is_silva(acc):
        return "SILVA"
    # GenBank: 1-3 letters followed by 5-8 digits (optionally versioned with .N)
    if re.match(r'^[A-Z]{1,3}\d{5,8}(\.\d+)?$', acc.upper()):
        return "GenBank"
    return "Unknown"



def _parse_silva(subject_title):
    """
    Parse a SILVA subject title into the 7-rank taxonomy string.
    Supports two formats:
      1. 'silva|accession|Domain;Phylum;Class;Order;Family;Genus;Species'  (pipe-delimited)
      2. '<accession> Domain;Phylum;Class;Order;Family;Genus;Species'       (space-delimited)
    Ranks are positional (no prefixes): index 0=kingdom, 1=phylum, ... 6=species.

    When the taxonomy string contains more than 7 levels (common in SILVA), the
    first 4 broad ranks and the last 3 specific ranks are kept, following the
    strategy from https://gist.github.com/walterst/9ddb926fece4b7c0e12c.
    """
    s = subject_title.strip()
    pipe_parts = s.split("|")
    if len(pipe_parts) >= 3 and pipe_parts[0].lower() == "silva":
        # Pipe-delimited: silva|accession|taxonomy
        tax_str = pipe_parts[2]
    else:
        # Space-delimited: strip leading accession token if present
        space_parts = s.split(" ", 1)
        tax_str = space_parts[1] if len(space_parts) == 2 else space_parts[0]
    tokens = [t.strip() for t in tax_str.split(";") if t.strip()]
    depth = len(tokens)
    if depth == 7:
        seven = tokens
    elif depth > 7:
        # Keep first 4 broad ranks + last 3 specific ranks
        seven = tokens[0:4] + tokens[depth - 3:depth]
    else:
        # Pad missing trailing ranks with "None"
        seven = tokens + ["None"] * (7 - depth)
    result = [v if v else "None" for v in seven]
    return " / ".join(result)


def _parse_bold_unite(subject_title):
    """
    Parse a semicolon-separated BOLD/UNITE taxonomy string into the 7-rank
    format: kingdom\t/\tphylum\t/\tclass\t/\torder\t/\tfamily\t/\tgenus\t/\tspecies
    Ranks absent or set to 'None' are returned as empty string.
    """
    ranks = {r: "" for r in RANK_ORDER}
    for token in subject_title.split(";"):
        token = token.strip()
        for prefix, rank in BOLD_PREFIX_MAP.items():
            if token.startswith(prefix):
                value = token[len(prefix):].strip()
                if value.lower() != "none":
                    ranks[rank] = value
                break
    return " / ".join(ranks[r] for r in RANK_ORDER)


def _taxonkit_lineage(taxids):
    """Call taxonkit for a set of numeric taxids; return {taxid: lineage_str}."""
    taxid_input = "\n".join(sorted(taxids)).encode()
    lineage_cmd = ["taxonkit", "lineage", "--show-lineage-ranks",
                   "--data-dir", args.taxdump]
    reformat_cmd = ["taxonkit", "reformat2",
                    "--format", TAXONKIT_FORMAT,
                    "--data-dir", args.taxdump]

    p1 = Popen(lineage_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    lineage_out, lineage_err = p1.communicate(input=taxid_input)
    if lineage_err:
        log(error=lineage_err, function="add_taxonomy:taxonkit_lineage")

    p2 = Popen(reformat_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    reformat_out, reformat_err = p2.communicate(input=lineage_out)
    if reformat_err:
        log(error=reformat_err, function="add_taxonomy:taxonkit_reformat2")

    result = {}
    for line in reformat_out.decode().splitlines():
        parts = line.split("\t")
        if parts:
            result[parts[0].strip()] = parts[-1].strip()
    return result


def add_taxonomy(tabular_path):
    """
    Append a #Taxonomy column to *tabular_path* in-place.

    - BOLD/UNITE rows (stitle contains 'k__'): taxonomy parsed directly from stitle.
    - GenBank rows (numeric staxid): taxonomy resolved via taxonkit.
    """
    # First pass: scan to decide which strategy each row needs
    ncbi_taxids = set()
    with open(tabular_path, "r") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            subject = parts[SUBJECT_COL] if len(parts) > SUBJECT_COL else ""
            taxid   = parts[TAXID_COL].strip() if len(parts) > TAXID_COL else ""
            if not _is_bold_unite(subject) and taxid.isdigit():
                ncbi_taxids.add(taxid)

    # Resolve NCBI taxids via taxonkit only when needed
    taxid_to_lineage = {}
    if ncbi_taxids:
        if args.taxdump:
            taxid_to_lineage = _taxonkit_lineage(ncbi_taxids)
        else:
            log(out="NCBI taxids found but --taxdump not provided; taxonomy will be empty for these rows.",
                function="add_taxonomy")

    # Second pass: rewrite with appended source + taxonomy
    annotated = tabular_path + "_tax"
    source_col_idx = None
    taxonomy_col_idx = None
    
    with open(tabular_path, "r") as src, open(annotated, "w") as dst:
        for line in src:
            if line.startswith("#"):
                # Detect existing Source and Taxonomy columns from header
                header_parts = line.rstrip("\n").split("\t")
                source_col_idx = None
                taxonomy_col_idx = None
                for i, col in enumerate(header_parts):
                    if col == "#Source":
                        source_col_idx = i
                    elif col == "#Taxonomy":
                        taxonomy_col_idx = i
                
                # Reconstruct header: remove existing Source/Taxonomy columns if present
                new_header = []
                for i, col in enumerate(header_parts):
                    if i != source_col_idx and i != taxonomy_col_idx:
                        new_header.append(col)
                dst.write("\t".join(new_header) + "\t#Source\t#Taxonomy\n")
                continue
            
            parts = line.rstrip("\n").split("\t")
            subject = parts[SUBJECT_COL] if len(parts) > SUBJECT_COL else ""
            acc     = parts[ACC_COL].strip() if len(parts) > ACC_COL else ""
            taxid   = parts[TAXID_COL].strip() if len(parts) > TAXID_COL else ""
            source   = _detect_source(acc)
            if _is_bold_unite(subject):
                taxonomy = _parse_bold_unite(subject)
            elif source == "SILVA":
                taxonomy = _parse_silva(subject)
            else:
                taxonomy = taxid_to_lineage.get(taxid, "")
            if not taxonomy:
                taxonomy = "None"
            else:
                taxonomy = "\t/\t".join(
                    p if p.strip() else "None" for p in taxonomy.split("\t/\t")
                )
            
            # Reconstruct row: remove existing Source/Taxonomy columns if present
            new_parts = []
            for i, part in enumerate(parts):
                if i != source_col_idx and i != taxonomy_col_idx:
                    new_parts.append(part)
            dst.write("\t".join(new_parts) + "\t" + source + "\t" + taxonomy + "\n")
    os.replace(annotated, tabular_path)
    log(out=f"Taxonomy annotation complete -> {tabular_path}", function="add_taxonomy")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_output_folders():
    os.makedirs(args.out_folder.strip(), exist_ok=True)
    os.makedirs(os.path.join(args.out_folder.strip(), "files"),  exist_ok=True)
    os.makedirs(os.path.join(args.out_folder.strip(), "chunks"), exist_ok=True)


def make_user_database():
    out, err = Popen(
        ["makeblastdb", "-in", args.blast_database, "-dbtype", "nucl"],
        stdout=PIPE, stderr=PIPE
    ).communicate()
    log(out, err, "create_database")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    make_output_folders()

    # Annotate-only mode: skip BLAST entirely
    if args.annotate_only:
        log(out=f"annotate_only: annotating {args.annotate_only} in-place", function="main")
        add_taxonomy(args.annotate_only)
        return

    if args.blast_database_type == "user":
        make_user_database()

    chunk_dir = os.path.join(args.out_folder.strip(), "chunks")
    chunk_files = split_fasta_into_chunks(args.input.strip(), chunk_dir)

    if not chunk_files:
        log(error="No sequences found in input file.", function="main")
        sys.exit("No sequences found in input file.")

    # Run up to MAX_PARALLEL BLAST jobs concurrently
    result_files = []
    with ThreadPoolExecutor(max_workers=args.max_parallel) as executor:
        futures = {executor.submit(run_blast_chunk, chunk): chunk for chunk in chunk_files}
        for future in as_completed(futures):
            chunk = futures[future]
            try:
                result_path = future.result()
                result_files.append(result_path)
            except Exception as exc:
                log(error=f"Chunk {chunk} raised an exception: {exc}", function="main")

    if args.coverage and args.outfmt.strip() == "custom_taxonomy":
        for path in result_files:
            if os.path.isfile(path):
                coverage_filter(path)

    final_output = os.path.join(args.out_folder.strip(), "files", "blast_results.tabular")
    merge_results(result_files, final_output)

    if args.outfmt.strip() == "custom_taxonomy":
        add_taxonomy(final_output)

    # Clean up temp files: chunk FASTAs and per-chunk BLAST tabulars
    for path in chunk_files:
        try:
            os.remove(path)
        except OSError:
            pass
    for path in result_files:
        try:
            os.remove(path)
        except OSError:
            pass
    try:
        os.rmdir(chunk_dir)
    except OSError:
        pass  # not empty or already gone


if __name__ == "__main__":
    main()
