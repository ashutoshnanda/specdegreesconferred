import os

datadir = "./data"
spreadsheet_name_cc = "cc_major_by_year.tsv"
spreadsheet_name_en = "en_major_by_year.tsv"
spreadsheet_name_gs = "gs_major_by_year.tsv"

def aggregate_to_dictionary(tsv_list):
	name_to_major_count = {}

	for tsv in tsv_list:
		f = open(os.path.join(datadir, tsv), 'r')
		year = int(tsv.replace(".tsv", "").split("-")[1])

		for i, line in enumerate(f):
			if i != 0:
				line_list = line.strip().split("\t")
				major_name = line_list[0]
				if major_name == 'NA':
					major_name = line_list[-2]
				if major_name not in name_to_major_count:
					name_to_major_count[major_name] = {}

				if line_list[2] == 'NA':
					name_to_major_count[major_name][year] = (line_list[-1], 0)
				else:
					#tuple composed of number of majors, and number of total academic accreditation
					name_to_major_count[major_name][year] = (line_list[2], line_list[-1])
	return name_to_major_count

def dictionary_to_spreadsheet(dictionary, spreadsheet_name):
	f = open(os.path.join(datadir, spreadsheet_name), 'w')
	headings = "Major\t"

	for i in range(2003, 2013):
		headings += "%d-%d"%(i, i+1)
		if i != 2012:
			headings+="\t"
		else:
			headings+="\n"

	f.write(headings)

	for major in sorted(dictionary.keys()):
		f.write(major+'\t')
		for i in range(2003, 2013):
			val = dictionary[major].get(i)
			if val == None:
				f.write('0')
			else:
				f.write(val[0])
			print(spreadsheet_name, i, major, val)
			if i != 2012:
				f.write("\t")
			else:
				f.write("\n")
	f.close()


'''
Returns a list of TSV's from a directory
'''	
def get_cc_tsv_list():
	tsv_list = []
	for i in range(2003, 2013):
		tsv_list.append("cc-%d.tsv"%i)
	return tsv_list

def get_en_tsv_list():
	tsv_list = []
	for i in range(2003, 2013):
		tsv_list.append("en-%d.tsv"%i)
	return tsv_list

def get_gs_tsv_list():
	tsv_list = []
	for i in range(2003, 2013):
		tsv_list.append("gs-%d.tsv"%i)
	return tsv_list

if __name__ == "__main__":
    dictionary_to_spreadsheet(aggregate_to_dictionary(get_cc_tsv_list()), spreadsheet_name_cc)
    dictionary_to_spreadsheet(aggregate_to_dictionary(get_en_tsv_list()), spreadsheet_name_en)
    dictionary_to_spreadsheet(aggregate_to_dictionary(get_gs_tsv_list()), spreadsheet_name_gs)
