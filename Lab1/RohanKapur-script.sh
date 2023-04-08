#! /usr/bin/bash
IFS=$'\n' # Set the "internal field separator" variable
	      # which the shell uses to split words in loops
for file in `ls`; do 
    for line in `cat $file | sed -n 'n;p'`; do 
        echo "$file:$line"
    done 
done 
unset IFS # Unset the IFS variable to restore the default
          # word-splitting behavior