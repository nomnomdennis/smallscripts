def btrdna2rna(str):
	"""

	[Superior version] Convert a sequence of DNA to the complimentary RNA strand

	"""
	import sys

	temp = str;  #ATCG 
	
	temp = temp.replace("A","U") 
	temp = temp.replace("T","A") 
	temp = temp.replace("G","c") 
	temp = temp.replace("C","G") 	
	temp = temp.replace("c","C")

	result = temp; #UAGC

	return result

def dna2rna(str):
	"""

	Convert a sequence of DNA to the complimentary RNA strand

	"""

	import sys

	temp = str;

	temp = temp.replace("A","u")
	temp = temp.replace("T","a")
	temp = temp.replace("G","c")
	temp = temp.replace("C","g")

	temp = temp.replace("u","U")
	temp = temp.replace("a","A")
	temp = temp.replace("g","G")
	temp = temp.replace("c","C")

	result = temp;

	return result

def dna2dna(str):
	"""

	Convert a sequence of DNA to the complimentary DNA strand

	"""

	import sys

	temp = str;

	temp = temp.replace("A","t")
	temp = temp.replace("T","a")
	temp = temp.replace("G","c")
	temp = temp.replace("C","g")

	temp = temp.replace("t","T")
	temp = temp.replace("a","A")
	temp = temp.replace("g","G")
	temp = temp.replace("c","C")

	result = temp;

	return result	


initial_gene = raw_input("Enter Sequence: ")

#result = dna2rna(initial_gene)

#print "> "+ result
result = btrdna2rna(initial_gene)
#result = dna2dna(initial_gene)

print "> "+ result
