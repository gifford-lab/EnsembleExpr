#!/bin/bash
#
# Usage: ./find_chromatin_states.sh example.vcf > additional_data/CAGI_roadmap_E116_chromatin_states.tsv
#
OIFS=$IFS
IFS=$'\n'
states="../data/E116_18_core_K27ac_mnemonics.bed.gz" # roadmap
# states="../additional_data/wgEncodeBroadHmmGm12878HMM.bed.gz" # ernst
echo "chromatin_state"
for line in `cat $1 | cut -f 1-3 | tail -n +2`; do
    id=`echo $line | cut -f 3`
    chr=`echo $line | cut -f 1`
    pos=`echo $line | cut -f 2`
    # echo -en $id"\t"
    # stupid tricks to only have one state per variant and print missing if it can't find any
    cat <(zcat $states | grep -F chr$chr | awk -v chr=$chr -v pos=$pos '$1=="chr"chr && pos>=$2 && pos<=$3') <(echo "missing") | head -1 | cut -f 4
done
IFS=$OIFS
