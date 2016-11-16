args = commandArgs(T)

vcffile = args[1]
bedfile = args[2]

system(paste0('cat ',vcffile,' | sed \'/^#/ d\' | awk \'{print $1 \"\\t\" $2-1 \"\\t\"  $2 \"\\t\" $3 \"\\t\"  0 \"\\t\" \"+\"}\' | sort -k2  -n -s | sort -k1 -n -s | sed -e \'s/^/chr/\' > ',bedfile))
