#!/bin/bash

export PATH=${PATH}/:$HOME/software/gsutil
file=GoogleList.txt
output_dir=output
data_dir=/oasis/projects/nsf/usu104/igarousi/projects/scratch

# IFS stands for "internal field separator". It is used by the shell to determine how to 
# do word splitting, i. e. how to recognize word boundaries.
# Here, I used "new line" because we have one path in each line within GoogleList.txt
IFS=$'\n'

# Run the following bash command.  This uses gsutil library 
# that is already installed on the system.
for i in `cat ../$output_dir/$file`; do gsutil cp -r "$i" $data_dir; done

# Organize files such that to speed up the data acquisition process
!for i in {2007..2018}; do mkdir -p $data_dir/$i; done
!for i in {2007..2018}; do mv $data_dir/$i* $data_dir/$i; done