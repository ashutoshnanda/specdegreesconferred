import urllib.request
import re
import os.path

#===============================================

urls = {2012: ("http://www.columbia.edu/cu/opir/abstract/opir_ccug_degrees_by_program_1.htm",
               "http://www.columbia.edu/cu/opir/abstract/opir_enug_degrees_by_program_1.htm",
               "http://www.columbia.edu/cu/opir/abstract/opir_gsug_degrees_by_program_1.htm"),

        2011: ("http://web.archive.org/web/20130301164116/http://www.columbia.edu/cu/opir/abstract/opir_ccug_degrees_by_program_1.htm",
               "http://web.archive.org/web/20130223044823/http://www.columbia.edu/cu/opir/abstract/opir_enug_degrees_by_program_1.htm",
               "http://web.archive.org/web/20130301164138/http://www.columbia.edu/cu/opir/abstract/opir_gsug_degrees_by_program_1.htm"),

        2010: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202010-2011.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202010-2011.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202010-2011.htm"),

        2009: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202009-2010.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202009-2010.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202009-2010.htm"),

        2008: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202008-2009.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202008-2009.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202008-2009.htm"),

        2007: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202007-2008.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202007-2008.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202007-2008.htm"),

        2006: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202006-2007.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202006-2007.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202006-2007.htm"),

        2005: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202005-2006.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202005-2006.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202005-2006.htm"),

        2004: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202004-2005.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202004-2005.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202004-2005.htm"),
        
        2003: ("http://www.columbia.edu/cu/opir/abstract/cc%20undergraduate%20degrees%20by%20program%20of%20study%202003-2004.htm",
               "http://www.columbia.edu/cu/opir/abstract/en%20undergraduate%20degrees%20by%20program%20of%20study%202003-2004.htm",
               "http://www.columbia.edu/cu/opir/abstract/gs%20undergraduate%20degrees%20by%20program%20of%20study%202003-2004.htm")}

sep = "================================================="

web_file_format = 'html/%s-%d.html'
data_file_format = 'data/%s-%d.tsv'
data_dir = 'data/'

#===============================================

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#===============================================

def print_urls():
    for key in urls:
        print(key)  
        print(sep)
        print(urls[key][0])
        print(urls[key][1])
        print(urls[key][2])
        print(sep)
        print()

def save_pages():
    for key in urls:
        print(key)
        for i, filetype in enumerate(['cc', 'en', 'gs']):
            try:
                urllib.request.urlretrieve(urls[key][i], web_file_format % (filetype, key))
            except urllib.error.ContentTooShortError:
                print('Content too short: %s - %d' % (filetype, key))
            
def extract(string, start = "<", end = ">"):
    first = string[:string.find(start)]
    string = string[string.find(start):]
    end = string[string.find(end) + 1:]
    string = string[:string.find(end)]
    return (first, string, end, first + string)

def all_file_to_tsv():
    for key in urls:
        for filetype in ['cc', 'en', 'gs']:
            file_to_tsv(key, filetype)
    
def file_to_tsv(key, filetype):
    matrix_to_tsv(file_to_matrix(key, filetype), key, filetype)
                        
def file_to_matrix(key, filetype):
    print(str(key) + " - " + filetype)
    print(sep)
    file = open(web_file_format % (filetype, key), 'r')
    bigstring = ""
    for line in [line.strip().replace("&nbsp;", "").replace("&amp;", "&") for line in file.readlines()]:
        bigstring += line
    file.close()
    biglist = []
    while len(bigstring) != 0:
        iterate = extract(bigstring)
        #print(iterate[0], iterate[1], len(iterate[2]))
        biglist.append(iterate[3])
        bigstring = iterate[2]
    sentinel = "<table"
    endsentinel = "</table"
    signal = "</td>"
    noise = "</tr>"
    table = []
    row = []
    i = 1
    looking = False
    for line in biglist:
        if sentinel in line:
            looking = True
        if looking:
            if noise in line:
                i = 1
                table.append(row)
                row = []
            if signal in line:
                item = line.replace(signal, "")
                if is_number(item):
                    item = int(item)
                if item == '-':
                    item = 0
                row.append(item)
        if endsentinel in line:
            looking = False
    print(sep)
    print()
    if key < 2011:
        for i in range(len(table)):
            if any([type(item) != int and 'grand' in item.lower() for item in table[i]]):
                table[i][0] = table[i][1]
                val = table[i].pop(len(table[i]) - 3)
                table[i][-3] += val
            elif sum([type(item) == int for item in table[i]]) == 1:
                value = 0
                for item in table[i]:
                    if type(item) == int:
                        value = item
                        break
                table[i] = ['' for j in range(7)]
                table[i][-1] = item
                table[i][-2] = "Total Number of Degrees"
            elif type(table[i][2]) == int:
                #TITLE IN HERE
                table[i] = [convert_to_standardized_string(table[i][0]), table[i][1], table[i][2], table[i][3], table[i][4] + table[i][5], table[i][6], table[i][7]]
    elif key > 2010:
        for i in range(len(table)):
            if len(table[i]) > 4 and type(table[i][2]) == int:
                if filetype == 'cc' or filetype == 'gs':
                    if len(table[i]) > 5:
                        table[i] = [convert_to_standardized_string(table[i][0]), table[i][1], table[i][2], table[i][3], table[i][4], 0, table[i][5]]
                    else:
                        table[i] = [table[i][0], 'Grand Totals', table[i][1], table[i][2], table[i][3], 0, table[i][4]]
                    if not(len(list(filter(lambda x: x != '', table[i]))) > 6):
                        table[i] = [table[i][0], 'Grand Totals', table[i][1], table[i][2], table[i][3], 0, table[i][4]]
                else:
                    table[i] = list(filter(lambda x: x != "", table[i]))
                    if len(table[i]) == 6:
                        table[i] = [convert_to_standardized_string(table[i][0]), table[i][1], table[i][2], table[i][3], 0, table[i][4], table[i][5]]
                    else:
                        table[i] = [convert_to_standardized_string(table[i][0]), 'Grand Totals', table[i][1], table[i][2], 0, table[i][3], table[i][4]]
            else:
                if any([type(table[i][j]) == int for j in range(len(table[i]))]) and len(table[i]) > 4:
                    number = 0
                    for j in range(len(table[i])):
                        if type(table[i][j]) == int:
                            number = table[i][j]
                            break
                    table[i] = ['', '', '', '', '', 'Total Number of Degrees', number]
    return table
        
def matrix_to_tsv(table, key, filetype):
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    file = open(data_file_format % (filetype, key), 'w')
    for i, row in enumerate(table):
        if any([type(item) == int for item in row]) and len(row) > 5:
            for (i, item) in enumerate(row):            
                if i != len(row) - 1:
                    if item == '':
                        file.write("NA\t")
                    else:
                        file.write(str(item) + "\t")
                else:
                    file.write(str(item) + "\n") 
    file.close()

def convert_to_standardized_string(str):
    #convert to lowercase
    newstr = str.lower()
    #take out whitespaces
    newstr = newstr.replace(" ", "")

    if "&" in newstr:
        newstr = newstr.replace("&", "and")
    elif "-" in newstr:
        newstr = newstr.replace ("-", "")

    return newstr

#===============================================
        
if __name__ == "__main__":
    all_file_to_tsv()
            
