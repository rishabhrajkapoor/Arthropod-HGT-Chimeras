#appends a fasta for sequence 1 to a file 2 
blastdbcmd -db /n/holyscratch01/extavour_lab/Lab/rkapoor/nr_db/nr -entry $1 -target_only >> $2
