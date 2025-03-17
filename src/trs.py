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


def tr_strings_stream(infile, outfile, replacements, buffer_size=32768):
    buffer = ""
    max_key_len = max(len(key) for key in replacements) if replacements else 1

    while True:
        chunk = infile.read(buffer_size)
        if not chunk:
            break  # End of file

        buffer += chunk  # Append to buffer

        
        # Replace substrings
        # new_text = buffer
        for old, new in replacements.items():
            buffer = buffer.replace(old, new)

        # buffer=new_text

        # Process only up to a safe margin
        process_upto = len(buffer) - max_key_len
        if process_upto <= 0:
            continue  # Not enough data to process


        # Write processed text to output
        outfile.write(buffer[:process_upto])

        # Keep the remainder as buffer for next iteration
        buffer = buffer[process_upto:]

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
