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
#def run_date(ast, temp, acceptable, ast_data_directory, true_delta_v):
	"""
	Lots.

	"""
	import sys
	import os
	import math
	import urllib
	import urllib2
	import subprocess
	import shutil

	# sort by date
	os.makedirs(ast_data_directory + "/date_temp")
	with open(temp, "r") as file:
		for line in file:

			# set date
			date = ast_data_directory + "/date_temp/" + line[15:19] + "-" + line[20:22] + "-" + line[23:25] + ".txt"
			
			# create file if it doesn't exist
			if os.path.isfile(date):
				rw = open(date, "a")
		  		rw.write(line)
		  		rw.close()
			
			# otherwise write to file
			else:
				rw = open(date, "a")
		  		rw.write(line)
		  		rw.close()


	# initiate temporary run file
	run = ast_data_directory + "/run.txt"
	runfile = open(run, "w")
	runfile.close()

	# open storage files
	os.makedirs(ast_data_directory + "/date")
	a_file = open(ast_data_directory + "/date" + "/a_date.txt","a+");
	i_file = open(ast_data_directory + "/date" + "/i_date.txt","a+");
	e_file = open(ast_data_directory + "/date" + "/e_date.txt","a+");
	delta_v_file = open(ast_data_directory + "/date" + "/delta_v_date.txt","a+");
	norm_delta_v_file = open(ast_data_directory + "/date" + "/norm_delta_v_date.txt","a+");
   
	# reorder dates
	filenames = os.listdir(ast_data_directory + "/date_temp");
	#filenames = filenames.sort

	obs_night = 0;
	check = "TRUE";

	# open runfile that goes into Find Orb
	with open(run, "a") as f:

	 	# for each date file
	 	for fn in os.listdir(ast_data_directory + "/date_temp"):
	 		print "\nAdding " + fn + "..."
	 		
	 		# count observing night
	 		obs_night = obs_night + 1;

	 		# add it to run.txt
	 		with open(ast_data_directory + "/date_temp" + "/" + fn, "r") as file:
	 			put = file.read()
	 			f.write(put)

	 		# run find orb on up to that date	
	 		f.close()	
	 		result = find_orb(run)
	 		f = open(run, "a")

	 		if result != False: #return (a, i, e, delta_v)

	 			# calculate normalized delta_v
	 			norm_delta_v = result[3] / true_delta_v;	

	 			# take result and record in text files
	 			day = fn.replace(".txt", " ")
	 			a_file.write(day + str(result[0]) + "\n")
	 			i_file.write(day +str(result[1]) + "\n") # value printed is in radians
	 			e_file.write(day +str(result[2]) + "\n") 
	 			delta_v_file.write(day + str(result[3]) + "\n")
	 			norm_delta_v_file.write(day + str(norm_delta_v) + "\n")

	 			# check for convergence
	 			variation = abs(result[3] - true_delta_v);

				if variation < acceptable and check == "TRUE":
					conv_obs_night = obs_night;
					conv_date = day;
					conv_dv = result[3];
					conv_a = result[0];
					conv_e = result[2];
					conv_i = result[1];				
					check = "FALSE";

				elif variation > acceptable and check == "FALSE":
					check = "TRUE";

	return (conv_obs_night, conv_date, conv_dv, conv_a, conv_e, conv_i)	
def run_nights(ast, temp, acceptable, ast_data_directory, true_delta_v):
	"""
	Lots.

	"""
	import sys
	import os
	import math
	import urllib
	import urllib2
	import subprocess
	import shutil

	os.makedirs(ast_data_directory + "/date_temp")
	os.makedirs(ast_data_directory + "/obs_temp")
	
	# sort by observatory
	with open(temp, "r") as file:
		for line in file:

			# set date
			obsver = ast_data_directory + "/obs_temp/" + line[77:80] + ".txt"
			
			# create file if it doesn't exist
			if os.path.isfile(obsver):
				rw = open(obsver, "a")
		  		rw.write(line)
		  		rw.close()
			
			# otherwise write to file
			else:
				rw = open(obsver, "a")
		  		rw.write(line)
		  		rw.close()

	# sort by date
	for obsfile in os.listdir(ast_data_directory + "/obs_temp"):

			# open observatory file
	 		with open(ast_data_directory + "/obs_temp" + "/" + obsfile, "r") as file:
				for line in file: 

 					new_year = int(line[15:19])
 					new_month = int(line[20:22])
 					new_day = float(line[23:31]) 		

	print "DONE WTIH OBSERVATORY SORTING"
	# initiate temporary run file
	run = ast_data_directory + "/run.txt"
	runfile = open(run, "w")
	runfile.close()

	# open storage files
	os.makedirs(ast_data_directory + "/date")
	a_file = open(ast_data_directory + "/date" + "/a_date.txt","a+");
	i_file = open(ast_data_directory + "/date" + "/i_date.txt","a+");
	e_file = open(ast_data_directory + "/date" + "/e_date.txt","a+");
	delta_v_file = open(ast_data_directory + "/date" + "/delta_v_date.txt","a+");
	norm_delta_v_file = open(ast_data_directory + "/date" + "/norm_delta_v_date.txt","a+");
   
	# reorder dates
	filenames = os.listdir(ast_data_directory + "/date_temp");
	#filenames = filenames.sort

	obs_night = 0;
	check = "TRUE";

	# open runfile that goes into Find Orb
	with open(run, "a") as f:

	 	# for each date file
	 	for fn in os.listdir(ast_data_directory + "/date_temp"):
	 		print "\nAdding " + fn + "..."
	 		
	 		# count observing night
	 		obs_night = obs_night + 1;

	 		# add it to run.txt
	 		with open(ast_data_directory + "/date_temp" + "/" + fn, "r") as file:
	 			put = file.read()
	 			f.write(put)

	 		# run find orb on up to that date	
	 		f.close()	
	 		result = find_orb(run)
	 		f = open(run, "a")

	 		if result != False: #return (a, i, e, delta_v)

	 			# calculate normalized delta_v
	 			norm_delta_v = result[3] / true_delta_v;	

	 			# take result and record in text files
	 			day = fn.replace(".txt", " ")
	 			a_file.write(day + str(result[0]) + "\n")
	 			i_file.write(day +str(result[1]) + "\n") # value printed is in radians
	 			e_file.write(day +str(result[2]) + "\n") 
	 			delta_v_file.write(day + str(result[3]) + "\n")
	 			norm_delta_v_file.write(day + str(norm_delta_v) + "\n")

	 			# check for convergence
	 			variation = abs(result[3] - true_delta_v);

				if variation < acceptable and check == "TRUE":
					conv_obs_night = obs_night;
					conv_date = day;
					conv_dv = result[3];
					conv_a = result[0];
					conv_e = result[2];
					conv_i = result[1];				
					check = "FALSE";

				elif variation > acceptable and check == "FALSE":
					check = "TRUE";

	return (conv_obs_night, conv_date, conv_dv, conv_a, conv_e, conv_i)	
def run_night(ast, temp, acceptable, ast_data_directory, true_delta_v):
	"""
	Lots.

	"""
	import sys
	import os
	import math
	import urllib
	import urllib2
	import subprocess
	import shutil

	# sort by date
	os.makedirs(ast_data_directory + "/date_temp")
	
	obsv = "NONE"
	night_counter = 0
	year = 0
	month = 0
	day = 0
	date_file =" "

	with open(temp, "r") as file:
		for line in file: 

			# find observatory
			new_obsv = line[77:80]
			new_year = int(line[15:19])
			new_month = int(line[20:22])
			new_day = float(line[23:31])
			# print new_obsv
			# print new_year
			# print new_month
			# print new_day

			# for the first one
			if obsv == "NONE":

				# set observatories and date info
				obsv = new_obsv
				year = new_year
				month = new_month
				day = new_day
				
				# create new file with next file
				night_counter = night_counter + 1
				if night_counter < 1000 and night_counter > 99:	
					date_file = ast_data_directory + "/date_temp/" + "0" + str(night_counter) + ".txt"	
				elif night_counter < 100 and night_counter > 9:
					date_file = ast_data_directory + "/date_temp/" + "00" + str(night_counter) + ".txt"
				elif night_counter < 10:
					date_file = ast_data_directory + "/date_temp/" + "000" + str(night_counter) + ".txt"				
				else:
					date_file = ast_data_directory + "/date_temp/" + str(night_counter) + ".txt"

				rw = open(date_file, "a")
	  			rw.write(line)
	  			rw.close()

		  	# if the same observatory
			elif obsv == new_obsv:
				# if the year + month are the same...
				if (year == new_year and month == new_month): 
					diff = abs(day - new_day)		
					#print str(day) +" - "+str(new_day) +" = " +str(diff)
					# ...and if the observation is within 6 hours
					if diff < 0.25:
						# ...same observation night
						rw = open(date_file, "a")
		  				rw.write(line)
		  				rw.close()
				
				# create new file
				else:
					obsv = new_obsv
					year = new_year
					month = new_month
					day = new_day

					night_counter = night_counter + 1
					if night_counter < 1000 and night_counter > 99:	
						date_file = ast_data_directory + "/date_temp/" + "0" + str(night_counter) + ".txt"	
					elif night_counter < 100 and night_counter > 9:
						date_file = ast_data_directory + "/date_temp/" + "00" + str(night_counter) + ".txt"
					elif night_counter < 10:
						date_file = ast_data_directory + "/date_temp/" + "000" + str(night_counter) + ".txt"				
					else:
						date_file = ast_data_directory + "/date_temp/" + str(night_counter) + ".txt"	
					rw = open(date_file, "a")
	  				rw.write(line)
	  				rw.close()

		  	# if different observatory, new file
		  	else:			
				# set observatories and date info
				obsv = new_obsv
				year = new_year
				month = new_month
				day = new_day

				# create new file with next file
				night_counter = night_counter + 1
				if night_counter < 1000 and night_counter > 99:	
					date_file = ast_data_directory + "/date_temp/" + "0" + str(night_counter) + ".txt"	
				elif night_counter < 100 and night_counter > 9:
					date_file = ast_data_directory + "/date_temp/" + "00" + str(night_counter) + ".txt"
				elif night_counter < 10:
					date_file = ast_data_directory + "/date_temp/" + "000" + str(night_counter) + ".txt"				
				else:
					date_file = ast_data_directory + "/date_temp/" + str(night_counter) + ".txt"
				rw = open(date_file, "a")
	  			rw.write(line)
	  			rw.close()

	# initiate temporary run file
	run = ast_data_directory + "/run.txt"
	runfile = open(run, "w")
	runfile.close()

	# open storage files
	os.makedirs(ast_data_directory + "/date")
	a_file = open(ast_data_directory + "/date" + "/a_date.txt","a+");
	i_file = open(ast_data_directory + "/date" + "/i_date.txt","a+");
	e_file = open(ast_data_directory + "/date" + "/e_date.txt","a+");
	delta_v_file = open(ast_data_directory + "/date" + "/delta_v_date.txt","a+");
	norm_delta_v_file = open(ast_data_directory + "/date" + "/norm_delta_v_date.txt","a+");
   
	# reorder dates
	filenames = os.listdir(ast_data_directory + "/date_temp");
	#filenames = filenames.sort

	obs_night = 0;
	check = "TRUE";

	# open runfile that goes into Find Orb
	with open(run, "a") as f:

	 	# for each date file
	 	for fn in os.listdir(ast_data_directory + "/date_temp"):
	 		print "\nAdding " + fn + "..."
	 		global conv_obs_night
	 		global conv_date
	 		global conv_dv
	 		global conv_a
	 		global conv_e
	 		global conv_i
	 		
	 		# count observing night
	 		obs_night = obs_night + 1;

	 		# add it to run.txt
	 		with open(ast_data_directory + "/date_temp" + "/" + fn, "r") as file:
	 			put = file.read()
	 			f.write(put)

	 		# run find orb on up to that date	
	 		f.close()	
	 		result = find_orb(run)
	 		f = open(run, "a")

	 		if result != False: #return (a, i, e, delta_v)

	 			# calculate normalized delta_v
	 			norm_delta_v = result[3] / true_delta_v;	

	 			# take result and record in text files
	 			day = fn.replace(".txt", " ")
	 			a_file.write(day + str(result[0]) + "\n")
	 			i_file.write(day +str(result[1]) + "\n") # value printed is in radians
	 			e_file.write(day +str(result[2]) + "\n") 
	 			delta_v_file.write(day + str(result[3]) + "\n")
	 			norm_delta_v_file.write(day + str(norm_delta_v) + "\n")

	 			# check for convergence
	 			variation = abs(result[3] - true_delta_v);

				if variation < acceptable and check == "TRUE":
					conv_obs_night = obs_night;
					conv_date = day;
					conv_dv = result[3];
					conv_a = result[0];
					conv_e = result[2];
					conv_i = result[1];				
					check = "FALSE";

				elif variation > acceptable and check == "FALSE":
					check = "TRUE";

	return (conv_obs_night, conv_date, conv_dv, conv_a, conv_e, conv_i)	
def run_obs(ast, temp, acceptable, ast_data_directory, true_delta_v):
	"""
	Lots.

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
	#return (conv_obs_night, conv_date, conv_dv, conv_a, conv_e, conv_i)						
	rw.close()
def run_date(ast, temp, acceptable, ast_data_directory, true_delta_v):
	"""
	Lots.

	"""
	import sys
	import os
	import math
	import urllib
	import urllib2
	import subprocess
	import shutil
	import calendar

	# sort by date
	with open(temp, "r") as file:
		first_line = file.readline()
		first_time = float(first_line[23:31]) - float(first_line[23:25])
		
	os.makedirs(ast_data_directory + "/date_temp")
	with open(temp, "r") as file:
		file.seek(0)
		for line in file:

			# set date
			year = line[15:19]
			month = line[20:22]
			actualdate = float(line[23:31]) - first_time
			
			if actualdate < 1:
				if int(month) != 1:
					month = int(month) - 1
					if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10:
						actualdate = actualdate + 31
					elif month == 2: 
						if calendar.isleap(int(year)) == True:
							actualdate = actualdate + 29
						else:	 	
							actualdate = actualdate + 28
					elif month == 4 or month == 6 or month == 9 or month == 11:	
						actualdate = actualdate + 30	
				else:
					month = "12"		
					actualdate = actualdate + 31

			if actualdate < 10:
					actualdate = "0" + str(int(actualdate))	
			else:
				actualdate = str(int(actualdate))	

			if int(month) < 10:
				month = "0" + str(int(month))
			else:
				month = str(int(month))

			date = ast_data_directory + "/date_temp/" + year + "-" + month + "-" + actualdate + ".txt"
			
			# create file if it doesn't exist
			if os.path.isfile(date):
				rw = open(date, "a")
		  		rw.write(line)
		  		rw.close()
			
			# otherwise write to file
			else:
				rw = open(date, "a")
		  		rw.write(line)
		  		rw.close()


	# initiate temporary run file
	run = ast_data_directory + "/run.txt"
	runfile = open(run, "w")
	runfile.close()

	# open storage files
	os.makedirs(ast_data_directory + "/date")
	a_file = open(ast_data_directory + "/date" + "/a_date.txt","a+");
	i_file = open(ast_data_directory + "/date" + "/i_date.txt","a+");
	e_file = open(ast_data_directory + "/date" + "/e_date.txt","a+");
	delta_v_file = open(ast_data_directory + "/date" + "/delta_v_date.txt","a+");
	norm_delta_v_file = open(ast_data_directory + "/date" + "/norm_delta_v_date.txt","a+");
   
	# reorder dates
	filenames = os.listdir(ast_data_directory + "/date_temp");
	filenames.sort

	obs_night = 0;
	check = "TRUE";

	# open runfile that goes into Find Orb
	with open(run, "a") as f:

	 	# for each date file
	 	for fn in os.listdir(ast_data_directory + "/date_temp"):
	 		print "\nAdding " + fn + "..."
	 		
	 		# count observing night
	 		obs_night = obs_night + 1;

	 		# add it to run.txt
	 		with open(ast_data_directory + "/date_temp" + "/" + fn, "r") as file:
	 			put = file.read()
	 			f.write(put)

	 		# run find orb on up to that date	
	 		f.close()	
	 		result = find_orb(run)
	 		f = open(run, "a")

	 		if result != False: #return (a, i, e, delta_v)

	 			# calculate normalized delta_v
	 			norm_delta_v = result[3] / true_delta_v;	

	 			# take result and record in text files
	 			day = fn.replace(".txt", " ")
	 			a_file.write(day + str(result[0]) + "\n")
	 			i_file.write(day +str(result[1]) + "\n") # value printed is in radians
	 			e_file.write(day +str(result[2]) + "\n") 
	 			delta_v_file.write(day + str(result[3]) + "\n")
	 			norm_delta_v_file.write(day + str(norm_delta_v) + "\n")

	 			# check for convergence
	 			variation = abs(result[3] - true_delta_v);

				if variation < acceptable and check == "TRUE":
					conv_obs_night = obs_night;
					conv_date = day;
					conv_dv = result[3];
					conv_a = result[0];
					conv_e = result[2];
					conv_i = result[1];				
					check = "FALSE";

				elif variation > acceptable and check == "FALSE":
					check = "TRUE";

	return (conv_obs_night, conv_date, conv_dv, conv_a, conv_e, conv_i)	
