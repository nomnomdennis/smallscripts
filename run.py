import sys
import os

from mpc_funcs import dl_data, find_orb, run_date, run_night, run_obs

# define wanted accuracy
ACCURACY = 0.05;

# check command line arguments is correct
if len(sys.argv)<2:
	print "Error: func.py <asteroid_file>"
	sys.exit()

# find list of asteroids [PUT IN SAME DIRECTORY]
asteroids_file = sys.argv[1];

# define directory for all the data
path_to_script = os.path.dirname(os.path.abspath(__file__))
data_directory = path_to_script + "/_data/"	

# make it if it doesn't exist
if not os.path.exists(data_directory):
	os.makedirs(data_directory)

# open data file for edit
master_data_file = open(data_directory + "/_master_data.txt","a");

# open list of asteroids
with open(asteroids_file, "r") as file:

	# for each asteroid
	for line in file:
		
		# prepares asteroids name
		ast = str(line[0:13]);
		ast = ast.strip();
		_ast = ast.replace(" ","_");

		# prepare and make individual asteroid directory
		ast_data_directory = data_directory + _ast
		os.makedirs(ast_data_directory)
		
		# get data
		data = dl_data(ast);

		# transfer data from .dat to temp.txt file
		temp = "temp.txt";
		dl = open(temp, "w");
		dl.write(data);
		dl.close()

		# get 'true' values
		# return (a, i, e, delta_v)
		true_result = find_orb(temp);

		# find the acceptable range
		acceptable = true_result[3] * ACCURACY;

		# date_result = run_night(ast, temp, acceptable, ast_data_directory, true_result[3]);
		date_result = run_date(ast, temp, acceptable, ast_data_directory, true_result[3]);
		#returns (conv_obs_night, conv_date = day, conv_dv, conv_a, conv_e, conv_i)
		obs_result = run_obs(ast, temp, acceptable, ast_data_directory, true_result[3])

		# append 0 as neccessary
		conv_obs_night = date_result[0];
		if conv_obs_night < 10:
			conv_obs_night = "0" + str(conv_obs_night);
		else:
			conv_obs_night = str(conv_obs_night)

 		# write results
 		# asteroid + converging night + converging date + converging d_v + converging a + converging e + converging i
 		results = _ast + " " + conv_obs_night + " " + str(date_result[1]) + " " + str(date_result[2]) + " " + str(date_result[3]) + " " + str(date_result[4]) + " " + str(date_result[5]);
 		master_data_file.write(results + "\n")

 		# observation result -
 		ovn = str(obs_result[0]) + " " + conv_obs_night  
 		obsvnight_data_file = open(data_directory + "/_obs_v_night.txt","a");
 		obsvnight_data_file.write(ovn + "\n")
 		obsvnight_data_file.close()

# close file
master_data_file.close()
