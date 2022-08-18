import os
import click
from time import sleep


@click.command()
@click.option('-county')
@click.option('-year', type=str)
def main(county, year):
    county_arg = '' if county is None else f'-county "{county}"'
    county_id = '' if county is None else f'{county.replace(" ", "")}'
    run_id = f"{county_id+year}"
    with open("job.sh", "w") as f:
      f.writelines("#!/bin/bash\n")
      f.writelines(f"#SBATCH --job-name={county_id}_{year}\n")
      f.writelines(f"#SBATCH --time=4-00:00:00\n")
      f.writelines(f"#SBATCH --nodes=4\n")
      f.writelines(f"#SBATCH --ntasks-per-node=4\n")
      f.writelines(f"#SBATCH --mem=64000\n")
      f.writelines(f"#SBATCH -o progress/{county}-{year}.txt\n")
      f.writelines(f"#SBATCH -e progress/{county}-{year}-e.txt\n\n")
      #f.writelines(f"python BISG.py -county {county} -year {year}\n")
      #f.writelines(f"python fill_nans.py -county {county} -year {year}\n")              
      f.writelines(f"python remerge.py -county {county} -year {year}\n")
      
    os.system("sbatch -p largemem job.sh")
    # sleep(3)
    return

if __name__=="__main__":
    main()
