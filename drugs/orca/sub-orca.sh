#!/bin/bash
string=".inp"
root="${1%$string}"

if [ -f $root.slurm ]
then
   rm $root.slurm
fi

echo '#!/bin/bash'>>$root.slurm
echo '#SBATCH --job-name='$root>>$root.slurm
echo '#SBATCH --output='$root'.out'>>$root.slurm
echo '#SBATCH --nodes=1'>>$root.slurm
echo '#SBATCH --ntasks-per-node=12 '>>$root.slurm
echo '#SBATCH --time=0-24:00:00 '>>$root.slurm
echo '#SBATCH --cluster=smp'>>$root.slurm

echo 'cd $SBATCH_O_WORKDIR'>>$root.slurm
echo 'module purge'>>$root.slurm
echo 'module load orca/3.0.3'>>$root.slurm

echo 'files=('>>$root.slurm
echo  $root'.inp'>>$root.slurm
echo ')'>>$root.slurm
echo 'for i in ${files[@]}; do'>>$root.slurm
echo '     cp $SLURM_SUBMIT_DIR/$i $SLURM_SCRATCH/$i'>>$root.slurm
echo 'done'>>$root.slurm

echo 'export LD_LIBRARY_PATH=/usr/lib64/openmpi-1.10/lib:$LD_LIBRARY_PATH'>>$root.slurm
echo 'export PATH=/usr/lib64/openmpi-1.10/bin:$PATH'>>$root.slurm

echo 'cd $SLURM_SCRATCH'>>$root.slurm

echo '$(which orca) '$root'.inp'>>$root.slurm
echo 'cp $SLURM_SCRATCH/*.{prop} $SLURM_SUBMIT_DIR'>>$root.slurm

exit
