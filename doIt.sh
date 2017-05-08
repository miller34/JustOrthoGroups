#! /bin/bash
filename="$1"
while read -r line
do
	name=$line
	#newFileName=foundOrthologs/H_similarity_$line

	#sbatch analyze_files.sh genes_with_split_sorted/H_sapiens genes_with_split_sorted/$name $newFileName
	#python combineGenes.py CDS/$line filteredGenes_noException/$name
	#python getNoException.py filteredGenes_noException/$name filteredGenes_noException/$line
	#python combineGenes.py CDS/$line genes_with_split/$name
	#python getNoException.py genes_with_split/$name genes_with_split/$line
	#bash sortFastaBySeqLen.sh genes_with_split/$name genes_with_split_sorted/$name
	#rm genes_with_split/$name
	#python findError.py "primates/$name" "error/$name"
	
	#echo "Name read from file - $name"
	
	##python getNumGenesTheSame.py Human_Equus_noSame/"$name"/DB/H_sapiens Human_Equus_noSame/"$name"/DB/Equus_caballus equusGenes
	#time python findOrthologs.py Human_Falco_noSame/"$name"/DB/H_sapiens.fa Human_Falco_noSame/"$name"/DB/Falco_peregrinus.fa Human_Falco_noSame/"$name"/orthologs_found_"$name"
	
	
	#wc -l Human_Falco_noSame/"$name"/orthologs_found_"$name"
	
	#python findError.py Human_Pan_w_mismatches/"$name"/output Human_Pan_w_mismatches/"$name"/error_"$name"
	#python findError.py Human_Pan_w_mismatches/"$name"/output2 Human_Pan_w_mismatches/"$name"/error2_"$name"
	#python combineTwoFoundOrthologFiles.py $name
	#python findError.py Human_Pan/"$name"/output Human_Pan/"$name"/error_"$name"
	#python findError.py Human_Pan/"$name"/output2 Human_Pan/"$name"/error2_"$name"
	#python findError2.py Human_Pan/"$name"/output3c Human_Pan/"$name"/error3c_"$name"
	
	#mv Human_Equus/$name/output3 Human_Equus_w_mismatches/$name/output3	
	#mv Human_Equus/$name/output3d Human_Equus_w_mismatches/$name/output3d	
	echo "Name read from file - $name"
	#scancel $name
	#python refog.data/findCorrectGroupPercent.py refog.data/outputHeaders_all $name "$name"_correct
	sbatch analyze_files.sh $name
#	grep -n $name nucleotide_position/Zonotrichia_albicollis >> PLACEIT
#	grep -A 1 $name ONLY_CDS/H_sapiens >> localization
#	chmod 770 all_extensions/$name
#	grep 0111 $name
#	python makeCompleteReference.py $name References/$2
#	python makeCompleteReference.py $name CompleteReference/H_sapiens
#	./readFile.py all_extensions/$name all_single_in_fasta_analysis/$name 
#	echo "Name read from file - $name"
#	cat CDS/$name ONLY_CDS/$name > temp/$name
#	python CompleteReference/cleanData.py combinedGenes/$name filteredGenes/$name
done < "$filename"







