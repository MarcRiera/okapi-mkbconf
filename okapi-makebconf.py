#!/usr/bin/python
import os
import sys
import fnmatch
import csv

sig = "batchConf";
version = 2;

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    print("USAGE: okapi-makebconf.py <folder>")
    sys.exit(1)

if os.path.exists(fn):
    outfile = "{}.bconf".format(os.path.basename(fn))
    folder = os.path.abspath(fn)
    pipeline = os.path.join(folder, "pipeline.pln")
    if not os.path.exists(pipeline):
        print("Pipeline file not found: '{}'".format(pipeline))
        sys.exit(1)
    mapping = os.path.join(folder, "extensions-mapping.txt")
    if not os.path.exists(mapping):
        print("Extension mapping file not found: '{}'".format(mapping))
        sys.exit(1)
else:
    print("Input folder not found: '{}'".format(fn))
    sys.exit(1)

with open(outfile, "wb") as out:
    # File signature
    out.write(len(sig).to_bytes(2, 'big'))
    out.write(sig.encode('utf-8'))
    out.write(version.to_bytes(4, 'big'))
    # Section 1 (plugins, unsupported)
    out.write((0).to_bytes(4, 'big'))
    # Section 2 (files, unsupported)
    out.write((-1).to_bytes(4, 'big', signed=True))
    # Section 3 (pipeline)
    out.write((1).to_bytes(4, 'big'))
    p = open(pipeline, "rb").read()
    out.write(len(p).to_bytes(2, 'big'))
    out.write(p)
    # Section 4 (filters)
    filters = fnmatch.filter(os.listdir(folder), '*.fprm')
    out.write(len(filters).to_bytes(4, 'big'))
    for f in filters:
        name = os.path.splitext(f)[0]
        out.write(len(name).to_bytes(2, 'big'))
        out.write(name.encode('utf-8'))
        fi = open(os.path.join(folder, f), "rb").read()
        out.write(len(fi).to_bytes(2, 'big'))
        out.write(fi)
    # Section 4 (mapping)
    with open(mapping) as file:
        tsv = list(csv.reader(file, delimiter="\t"))
        out.write(len(tsv).to_bytes(4, 'big'))
        for line in tsv:
            out.write(len(line[0]).to_bytes(2, 'big'))
            out.write(line[0].encode('utf-8'))
            out.write(len(line[1]).to_bytes(2, 'big'))
            out.write(line[1].encode('utf-8'))
