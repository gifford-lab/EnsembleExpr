import sys

motif= sys.argv[1]
NUMMOTIFS = int(sys.argv[2])
name = sys.argv[3]
NUMSEQS = int(sys.argv[4])

motifs = [""] * NUMMOTIFS

f = open(name + "."+ motif +".motifInstances.txt", 'r')
header = 0
scores = [[0 for j in xrange(NUMMOTIFS)] for i in xrange(NUMSEQS)]
# scores[i][j] corresponds to the score of motif i in sequence j

for line in f:
    if header == 0:
        labels = line.split()
        header = header + 1
    else:
        line_split = line.split()
        motif_id = int(line_split[0])
        seq_id = int(line_split[1])
        motif_name = line_split[2]
        score = float(line_split[8])
        motifs[motif_id] = motif_name
        scores[seq_id][motif_id] = max(scores[seq_id][motif_id], score)
    
f.close()

sys.stdout = open(name + "."+ motif +".scorematrix.txt", 'w')

print('\t'.join(map(str, motifs)))

for i in xrange(NUMSEQS):
    print('\t'.join(map(str, scores[i])))

sys.stdout.close()

