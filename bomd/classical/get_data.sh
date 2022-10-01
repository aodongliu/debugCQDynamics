##!/bin/bash

#This bash script will parse the output file of a CQ Ehrenfest job and return some data to plot


# *******************************************
# Prepation Work
# *******************************************


# The user should provide the name of the file to parse (without suffix)
echo "Name of the output file (WITHOUT THE .out SUFFIX)"
read DirectoryName


# Generate the filename
Suffix='.out'
FileName="${DirectoryName}${Suffix}"


# Make a directory to store the data files
mkdir $DirectoryName

# Copy the file over to the sub directory and work over there
cp $FileName $DirectoryName
cd $DirectoryName






# *******************************************
# Get the Position of the Two Atoms (to plot their bond length)
# *******************************************



# This will get all of the 2 lines following "Molecular Geometry"
grep 'Molecular Geometry: (Bohr)' -A 2 $FileName  | grep -v 'Molecular Geometry: (Bohr)' | grep -v '\-\-' > nuc_pos_raw.txt

# Too bad, there's another line called "Predicted Molecular Geometry" (The two lines following this are NOT what we want), the previous command will grep those as well. So in "nuc_pos_raw.txt", we need to get rid of every third and fourth line

# This gets rid of every fourth line
awk 'NR%4' nuc_pos_raw.txt > temp1.txt

# This gets rid of every third line
awk 'NR%3' temp1.txt > temp2.txt

# Now we can extract the positions of the two atoms:
awk 'NR %2 == 1' temp2.txt | awk '{print $5}' > h_pos.dat
awk 'NR %2 == 0' temp2.txt | awk '{print $5}' > f_pos.dat







# *******************************************
# Get the Time
# *******************************************
grep 'Time (fs):' $FileName | awk '{print $3}' > time.dat







# *******************************************
# Get the Energy
# *******************************************
grep 'EKin' $FileName | awk '{print $2}' > e_kin.dat
grep 'EKin' $FileName | awk '{print $4}' > e_pot.dat




# *******************************************
# Get the force
# *******************************************

grep 'Forces: (Hartrees/Bohr)' -A 2 $FileName  | grep -v 'Forces: (Hartrees/Bohr)' | grep -v '\-\-' > force_raw.txt
awk 'NR %2 == 1' force_raw.txt | awk '{print $5}' > h_force.dat
awk 'NR %2 == 0' force_raw.txt | awk '{print $5}' > f_force.dat





# *******************************************
# Clean up
# *******************************************
rm *txt

echo Done! All files generated in $DirectoryName
cd ..
