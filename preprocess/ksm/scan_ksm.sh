ksm_name=m0;            # top 1 motif from each ChIP-seq expt
ksm="gm.tf.$ksm_name.ksm_list.txt";
ksm_count=$(wc -l $ksm | cut -d " " -f 1);  # number of KSM motifs
fasta_name=$1;
fasta="$2";
                                                                                                                                          
java -Xmx100G -cp ksm.jar edu.mit.csail.cgs.deepseq.analysis.MotifScan --fasta $fasta --g hg19.info --ksm $ksm --out $fasta_name.$ksm_name;
                                                                                                                                          
python parser.py $ksm_name $ksm_count $fasta_name $(expr $(wc -l $fasta | cut -d " " -f 1) / 2);
