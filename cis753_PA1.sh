#!/bin/bash
#
#$ -S /bin/tcsh -cwd
#$ -o out.txt -j y
echo `date` >> out.txt
python cis753_PA1.py
echo `date` >> out.txt
exit 0

