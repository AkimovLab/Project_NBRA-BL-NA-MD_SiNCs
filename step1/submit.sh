for i in 0 
do
  mkdir traj${i}  
  cp dftb_in.hsd traj${i}
  cp position.gen traj${i}
  cp velocity.txt traj${i}
  cp submit.slm traj${i}
  cp thermal.py traj${i}
  cp convert.py traj${i}
  cd traj${i}
  sbatch submit.slm
  cd ../
done




