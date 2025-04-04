#appends a fasta for sequence 1 to a file 2 
singularity exec /cvmfs/singularity.galaxyproject.org/b/l/blast:2.13.0--hf3cf87c_0 blastdbcmd -db nr_db/nr -entry $1 >> $2
