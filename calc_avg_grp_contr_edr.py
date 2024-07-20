import subprocess
import glob

edr_files = []
ene_data = {}
for fn in glob.glob("*_BB_*.edr"):
    edr_files.append(fn)
for fn in glob.glob("*_SC_*.edr"):
    edr_files.append(fn)
for i,fn in enumerate(edr_files):
#    if i > 0: break
    print(fn)
    cmd = "gmx -nobackup energy -f " + fn
    result = subprocess.run(cmd.split(),input="26",capture_output=True, text=True)
    lines = result.stdout.split("\n")
    ene = -100.0
    for line in lines:
        if line.find("kJ/mol") > 0:
            #print(line)
            tokens = line.split()
            ene = float(tokens[4])
            print(f"{ene:12.4f}")
    tokens = fn.split("_")
    print(tokens)
    grp = tokens[2] + "_" + tokens[3]
    if not grp in ene_data:
        ene_data[grp] = [1000.0,1000.0]
    if( tokens[4].startswith("L0")):
        ene_data[grp][0] = ene
    if( tokens[4].startswith("L12")):
        ene_data[grp][1] = ene

def sort_grp_fun(grp):
    tokens=grp.split("_")
    num = int(tokens[0][3:])*10
    if(tokens[1] == "SC"):
        num += 1
    return num

grps_sorted = [grp for grp in ene_data.keys()]
grps_sorted.sort(key=sort_grp_fun)

for grp in grps_sorted:
    ene_L0  = ene_data[grp][0]/4.184
    ene_L12 = ene_data[grp][1]/4.184
    diff = ene_L12 - ene_L0
    print(f" {grp:10s} : {ene_L0:12.6f} {ene_L12:12.6f} {diff:12.6f}") 
    
		
#cmd = "sbatch " + fn_job
#subprocess.run(cmd.split())
		
		
		
					
		
	
	
