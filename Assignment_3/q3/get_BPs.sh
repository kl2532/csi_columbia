downloads_dir_path=$1
fail_dir=$downloads_dir_path"/fail/*"
pass_dir=$downloads_dir_path"/pass/*"

touch pass_BPcount.txt
touch fail_BPcount.txt

for file in $pass_dir
do
	echo $file >> pass_BPcount.txt 
	poretools stats  $file | sed -n 2p >> pass_BPcount.txt
done

for file in $fail_dir
do
	echo $file >> fail_BPcount.txt
	poretools stats $file | sed -n 2p >> fail_BPcount.txt
done
