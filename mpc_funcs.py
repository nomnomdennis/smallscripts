def dl_data(ast):
	"""
	Downloads and returns data from the Minor Planet Center
	"""
	import urllib
	import urllib2
	
	# input asteroid
	query_args = { 'object_id':ast} 
	init_ast = urllib.urlencode(query_args);
	data_ast = ast.replace(" ","_");

	# use url to initialize url (tricks mpc to thinking we are not software)
	s_url = 'http://www.minorplanetcenter.net/db_search/show_object?';
	initurl = s_url + init_ast;
	init = urllib2.urlopen(initurl);

	# after initialization, get data
	tmp = 'http://www.minorplanetcenter.net/tmp/'
	dataurl = tmp + data_ast + '.dat';
	get_data = urllib2.urlopen(dataurl)
	data = get_data.read()
	
	return (data)
	
def find_orb(txt_file):
	"""
	Runs Find_Orb Command line (./fo)
		Returns a, i, e as well as delta_v 
		Delta_v calculated using Shoemaker and Heilin (1979)
	"""
	import os
	import subprocess
	import math
	from computedeltav import cdv_SH, cdv_SH_bennerbug

	# run find_orb on file
	subprocess.call(["./fo", txt_file])
	
	# if find_orb outputted a result
	if os.path.isfile("mpc_fmt.txt") == True:
		# open the mpc_format
		mpc = open("mpc_fmt.txt", "r")
		result = mpc.readline()
		mpc.close()

		# get base a, i, e values
		a = float(result[92:103]);
		i = float(result[59:68]);
		e = float(result[70:79]);

		# convert inclination to radians
		i = math.radians(i);

		delta_v = cdv_SH(a,e,i);

		return (a, i, e, delta_v)	
	else:
		return False	

def run_obs(ast, temp, acceptable, ast_data_directory, true_delta_v):
	"""
	Sorts NEAs by each observation.
	"""	
	import sys
	import os
	import math
	import urllib
	import urllib2
	import subprocess
	import shutil

	os.makedirs(ast_data_directory + "/obs_temp")
	
	obs_file = open(ast_data_directory + "/obs_temp" + "/date.txt","a");
	a_file = open(ast_data_directory + "/obs_temp" + "/a.txt","a");
	i_file = open(ast_data_directory + "/obs_temp" + "/i.txt","a");
	e_file = open(ast_data_directory + "/obs_temp" + "/e.txt","a");
	delta_v_file = open(ast_data_directory + "/obs_temp" + "/delta_v.txt","a");

	row = ast_data_directory + "temp_os.txt"
	index = 0;
	f = "TRUE"
	with open(temp, "r") as file:
		for line in file:
			index = index + 1;

			rw = open(row, "a")
		  	rw.write(line)
		  	rw.close()

			result = find_orb(row)
	 		rw = open(row, "a")

	 		if result != False: #return (a, i, e, delta_v)
				
				#write everything
				obs_file.write(line[15:31] + "\n")	#write date
				a_file.write(str(result[0]) + "\n")
				i_file.write(str(result[1]) + "\n") # value printed is in radians
				e_file.write(str(result[2]) + "\n") 
				delta_v_file.write(str(result[3]) + "\n")

				variation = abs(result[3] - true_delta_v);
				
				if variation < acceptable and f == "TRUE":
					first_value = result[3];
					arrived_observation = index;
					f = "FALSE";
				elif variation > acceptable and f == "FALSE":
					f = "TRUE";		
			else:
				print "Skipped by Find Orb"	
	os.remove(row) 			
	return (arrived_observation, first_value)	
	rw.close()
