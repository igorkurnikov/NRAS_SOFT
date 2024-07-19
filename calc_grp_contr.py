import subprocess

grp_list_str = """GLY10_BB GLY12_BB GLY13_BB VAL14_BB VAL14_SC GLY15_BB LYS16_BB LYS16_SC 
SER17_BB SER17_SC ALA18_BB ALA18_SC LEU19_SC PHE28_SC VAL29_BB ASP30_BB GLU31_BB TYR32_BB TYR32_SC 
ASP33_BB PRO34_BB PRO34_SC THR35_BB THR35_SC ILE36_BB ASP57_SC THR58_BB ALA59_BB ALA59_SC 
GLY60_BB GLN61_BB GLN61_SC GLU63_BB TYR64_BB TYR64_SC ASN116_BB ASN116_SC LYS117_BB LYS117_ YS118_BB
ASP119_BB ASP119_SC LEU120_SC THR144_BB SER145_BB SER145_SC ALA146_SC LYS147_BB LYS147_SC THR148_SC"""

grp_list = grp_list_str.split()
print(grp_list)

mdp_templ = "md_rerun_templ.mdp"
job_templ = "jobscript_rerun_templ"
nn = 0
for grp in grp_list:
	nn += 1 
	if( nn < 6 ): continue
	if( nn > 6 ): break
	for lmb in (0,12):
		fn_mdp = "md_rerun_" + grp + "_L" + str(lmb) + ".mdp"
		fn_tpr = "md_rerun_" + grp + "_L" + str(lmb) + ".tpr"
		print(fn_mdp)
		with open(fn_mdp,"w") as fout:
			with open(mdp_templ,"r") as finp:
				for line in finp:
					if line.startswith("energygrps"):
						line = "energygrps = GTI " + grp + " \n"
					if line.startswith("init-lambda-state"):
						line = "init-lambda-state        = " + str(lmb) + " \n"
					fout.write(line)
		init_gro = "NRAS_MD_HVAT_RESTR_L" + str(lmb) + ".gro"
		cmd = f"gmx grompp -f {fn_mdp} -c {init_gro} -r NRAS_15H_ions_init.gro -p NRAS_FF19SB_GTI_2_3_gmx_4.top -n NRAS_GRPS_5A.ndx -o {fn_tpr} -maxwarn 30 "
		print(cmd)
		subprocess.run(cmd.split())
		fn_job = "jobscript_rerun_" + grp + "_L" + str(lmb)
		job_prefix = "NRAS_RERUN_" + grp + "_" + str(lmb)
		with open(fn_job,"w") as fout:
			with open(job_templ,"r") as finp:
				for line in finp:
					job_name = "NL" + str(lmb) + grp
					line = line.replace("JOB_NAME",job_name)
					line = line.replace("MD_RERUN.tpr",fn_tpr)
					line = line.replace("JOB_PREFIX",job_prefix)
					fout.write(line)
		cmd = "sbatch " + fn_job
		subprocess.run(cmd.split())
		
		
		
					
		
	
	
