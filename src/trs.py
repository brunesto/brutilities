#!/usr/bin/env python
#
# GPL v3 licence
#
# this script is similar to tr but it replaces strings instead of single characters
# it is meant to be used on large files
#
# example to reformat a osm xml file so that each element has its own line:
# ./trs.py "\n" "" "<way" "\n<way " "<relation" "\n<relation " "<node" "\n<node "
#
import sys
import codecs


def tr_strings_stream(infile, outfile, replacements, buffer_size=64000):
    buffer = ""
    max_key_len = max(len(key) for key in replacements) if replacements else 1
    r=0
    w=0
    while True:
        chunk = infile.read(buffer_size)
        if not chunk:
            break  # End of file

        r+=len(chunk)
        buffer += chunk  # Append to buffer

        
        # Replace substrings
        for old, new in replacements.items():
            buffer = buffer.replace(old, new)

        # compute margin
        process_upto = len(buffer) - max_key_len
        if process_upto <= 0:
            continue  # Not enough data left inside the buffer to produce output now

        # Write processed text to output
        outfile.write(buffer[:process_upto])

        # Keep the remainder into buffer for next iteration
        buffer = buffer[process_upto:]
        w+=process_upto
        print("r:%d mb w:%d mb",  int(r/(1024*1024)),int(w/(1024*1024)),file=sys.stderr,end='\r')


    w+=len(buffer)
    
    outfile.write(buffer)  # Write final part


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " old1 new1 old2 new2 ...")
        sys.exit(1)

    rs = sys.argv[1:]
    replacements = {}

    for i in range(0, len(rs), 2):

        # since this is a raw replacement (no regexp), we need to parse the escape characters from the command line
        key = codecs.decode(rs[i], "unicode_escape")
        value = codecs.decode(rs[i + 1], "unicode_escape")

        replacements[key] = value
        #print("replace " + repr(key) + " by " + repr(value) + "")

    tr_strings_stream(sys.stdin, sys.stdout, replacements)
