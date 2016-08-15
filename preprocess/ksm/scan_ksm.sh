scan_ksm(){
    ksm_name=m0;            # top 1 motif from each ChIP-seq expt
    ksm="gm.tf.$ksm_name.ksm_list.txt";
    ksm_count=$(wc -l $ksm | cut -d " " -f 1);  # number of KSM motifs
    fasta_name=$1;
    fasta="$2";

    java -Xmx1G -cp ksm.jar edu.mit.csail.cgs.deepseq.analysis.MotifScan --fasta $fasta --g hg19.info --ksm $ksm --out $fasta_name.$ksm_name;

    python parser.py $ksm_name $ksm_count $fasta_name $(expr $(wc -l $fasta | cut -d " " -f 1) / 2);
}

scan_ksm sample /cluster/projects/CAGI4-eQTL/processed_data/4-eQTL-causal_SNPs_sample.txt/150nt.fa;
scan_ksm dataset1 /cluster/projects/CAGI4-eQTL/processed_data/4-eQTL-causal_SNPs_dataset1.txt/150nt.fa;
scan_ksm dataset2 /cluster/projects/CAGI4-eQTL/processed_data/4-eQTL-causal_SNPs_dataset2.txt/150nt.fa;
