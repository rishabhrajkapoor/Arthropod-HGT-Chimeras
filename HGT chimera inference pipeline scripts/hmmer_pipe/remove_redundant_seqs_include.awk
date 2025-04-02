#!/usr/bin/awk -f

BEGIN {
    FS = "\n"
    RS = "\n>"
}

# Read input.txt and populate the descriptions hash table
NR == FNR {
    descriptions[$1] = 1
    next
}

NF > 1 {
    seq = $2
    gsub("\n", "", seq)

    if (!(seq in sequences)) {
        sequences[seq] = $1
        headers[numHeaders] = $1  # Store the header in the headers array
        seqs[numHeaders] = seq  # Store the sequence in the seqs array
        numHeaders++  # Increment the counter for the number of headers
    } else {
        if ($1 in descriptions) {
            sequences[seq] = $1
        }
        print "Redundant sequence removed: " sequences[seq] > "/dev/stderr"
    }
}

END {
    for (i = 0; i < numHeaders; i++) {
        print ">" headers[i]
        print seqs[i]
    }
}
