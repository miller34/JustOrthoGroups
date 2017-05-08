#!/bin/bash

#Submit this script with: sbatch thefilename
#SBATCH --qos=long
#SBATCH --time=57:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=5G   # memory per CPU core
#SBATCH -J "OMA"   # job name

# Compatibility variables for PBS. Delete if not needed.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`
export PBS_JOBID=$SLURM_JOB_ID
export PBS_O_WORKDIR="$SLURM_SUBMIT_DIR"
export PBS_QUEUE=batch


# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE


#input="CDS/"$1
#output="ONLY_CDS/"$1$1
#out2="ONLY_CDS/"$1
#echo "Mouse and Rat amino"
#input=$1
#in2=$2
#output=$3
#time python findOrthologs.py H_sapiens_w_Pan_genes Pan_paniscus_w_H_genes test_human_pan
#time python findOrthologs.py Falco_peregrinus_w_cherrug Falco_cherrug_w_peregrinus test_falco_falco
#time python findOrthologs.py H_sapiens_w_Falco_peregrinus Falco_peregrinus_w_H_sapiens test_human_falco_peregrinus
#time python findOrthologs.py Pan_paniscus_w_peregrinus Falco_peregrinus_w_pan test_pan_falco
#time python findOrthologs_w_AminoAcids.py M_w_R R_w_M MR_out_amino
#time python findOrthologs_w_AminoAcids.py M_w_R R_w_M MR_otherTest
#./doIt.sh specNames
time OMA
#time python original_findOrthologs.py genes_with_split_sorted/H_sapiens genes_with_split_sorted/Pan_paniscus human_pan_cor9

#python findOrthologs.py $input $in2 $output

#awk '!a[$0]++' $input >$output
#python eraseHeaders.py $output $out2
#rm $output
#python makeCompleteReference.py $1 References/$1
#python gff3_parser.py ../../ALL_genomes/H_sapiens/GFF/ref_GRCh38_top_level.gff3.gz H_sapiens
#python gff3_parser.py $1 $2
#./doIt.sh ../paths_to_NC/$1 $1
#python ml_make_arff.py CompleteReference/H_sapiens_ncRNA CompleteReference/H_sapiens_ncRNA.arff
#./doIt.sh $1


exit 0
