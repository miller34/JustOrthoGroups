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
	
	
	
	#python combineTwoFoundOrthologFiles.py $name
	
	##python countCorrectOrthologs.py thousand_splits/Human_Pan/"$name"/DB/Results_May09/OrthologousGroups.csv

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
	echo "Name read from file - $name"
#	python CompleteReference/cleanData.py combinedGenes/$name filteredGenes/$name
done < "$filename"







