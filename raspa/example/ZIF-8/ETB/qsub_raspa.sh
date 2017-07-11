#!/bin/bash

#PBS -j oe
#PBS -N ZIF-8-ETB
#PBS -q idist_big
#PBS -l nodes=1:ppn=1
#PBS -l walltime=24:00:00
#PBS -S /bin/bash

echo JOB_ID: $PBS_JOBID JOB_NAME: $PBS_JOBNAME HOSTNAME: $PBS_O_HOST
echo start_time: `date`

## Load python virtual environment
. /ihome/cwilmer/kbs37/venv/ipmof/bin/activate

cd $PBS_O_WORKDIR
simulate simulation.input

echo end_time: `date`
# workaround for .out / .err files not always being copied back to $PBS_O_WORKDIR
cp /var/spool/torque/spool/$PBS_JOBID.OU $PBS_O_WORKDIR/$PBS_JOBID$(hostname)_$$.out
cp /var/spool/torque/spool/$PBS_JOBID.ER $PBS_O_WORKDIR/$PBS_JOBID$(hostname)_$$.err

exit
