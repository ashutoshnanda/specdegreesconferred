#! /usr/bin/python

#NOTE: Concentrations are considered the same thing as minors for the purpose of
#      this data analysis. Additionally, interdepartmental majors are considered
#      majors.

#Basic Structure of Code:
#Lots of TSV's 
#-----
#Year Dictionary (key = year (int), value = (number, dictionary))
#   number: "Total Number of Degrees for that Year"
#   dictionary:
#       Deparment Dictionary (key = department (string), 
#                        value = (majors, minors))
#-----
#Department Spreadsheet
# 6 metrics:
#   0 --> Year
#   1 --> Number of Majors
#   2 --> Number of Minors
#   3 --> Department Composition (majors / (majors + minors))
#       I changed this metric from the original because having a 0 minor count
#       was pretty common. Now, closer to 1 indicates major dominated and closer
#       to 0 indicates minor dominated. Also, if majors + minors == 0, it is 
#       coded as 0.5 since the department isn't dominated by either.
#   4 --> Major Percentage (majors / degrees conferred)
#   5 --> Minor Percentage (minors / degrees conferred)
#   6 --> Combined Percentage ((majors + minors) / degrees conferred

import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

yearly_data_dir = "data"
department_data_dir = "department_data"
departmental_plots_dir = "departmental_plots"
index2description = {0 : "Number of Majors", 1 : "Number of Minors", 
                     2 : "Department Composition", 3 : "Major Percentage",
                     4 : "Minor Percentage", 5 : "Combined Percentage"}
school2longerschool = {"cc" : "Columbia College", "en" : "Columbia Engineering",
                       "gs" : "School of General Studies"}

yearly_data_file_name_format = "%s-%d.tsv"
department_data_file_name_format = "%s-%s.tsv"

section_separator = "============================="

def get_years(school):
    '''
    This function determines the years in which we have data for a particular 
    school.
    '''
    if not os.path.isdir(yearly_data_dir):
        print("Directory with yearly spreadsheets not found! Exiting!")
        exit(1)
    school_files = list(filter(lambda x: school in x, 
                        os.listdir(yearly_data_dir))) #Filter by school
    school_files = list(filter(lambda x: '-' in x, 
                        school_files)) #Filter by whether it is a year file
    years = [int( #Convert to integer
             file.replace('.tsv', '') #Get rid of file extension
             .split('-')[1] #Second half of string
             ) for file in school_files]
    return years

def extract_year_dictionary(school):
    '''
    This function extracts a dictionary that maps from years to a tuple that 
    contains the total number of degrees conferred that year and a dictionary
    that maps from department names to a tuple of majors and minors.
    '''
    time_period = get_years(school)
    years2department = {}
    for year in time_period:
        department2information = {}
        yearly_file_name = yearly_data_file_name_format % (school, year)
        yearly_file = open(os.path.join(yearly_data_dir, yearly_file_name), 'r')
        degrees_conferred = 0
        for i, line in enumerate([line.strip() #Take away the new line
                                  for line in yearly_file.readlines()]):
            if i != 0:
                data = line.split("\t")
                if data[0] == 'NA':
                    degrees_conferred = int(data[-1])
                else:
                    major_name = data[0]
                    #0 --> Program Description
                    #1 --> Offering Unit(s)
                    #2 --> Major
                    #3 --> Interdepartmental Major
                    #4 --> Concentration
                    #5 --> Minor
                    #6 --> Total
                    majors = int(data[2])
                    interdepartmental_majors = int(data[3])
                    concentrations = int(data[4])
                    minors = int(data[5])
                    totalmajors = majors + interdepartmental_majors
                    totalminors = concentrations + minors
                    previous = department2information.get(major_name, (0, 0))
                    new = (totalmajors + previous[0], totalminors + previous[1])
                    department2information[major_name] = new
        years2department[year] = (degrees_conferred, department2information)
    return years2department

def write_spreadsheet(year2department, school):
    '''
    This function accomplishes the main goal of writing out departmental
    spreadsheets which contain the 6 metrics listed at the top of this file
    (see the 3rd section).
    '''
    if not os.path.exists(department_data_dir):
        os.makedirs(department_data_dir)
    departments = get_all_departments(year2department)
    for department in departments:
        department_file_name = department_data_file_name_format % (school, 
                                                                   department)
        department_file = open(os.path.join(department_data_dir,
                                            department_file_name), 'w')
        headers = ["Year", "Number of Majors", "Number of Minors", 
                   "Department Composition", "Major Percentage",
                   "Minor Percentage", "Combined Percentage"]
        write_row(department_file, headers)
        for year in year2department:
            degrees_conferred = year2department[year][0]
            department2information = year2department[year][1]
            result = department2information.get(department, (0, 0))
            (majors, minors) = result
            ratio = majors / (majors + minors) if majors + minors != 0 else 0.5
            row = [year, majors, minors, ratio,
                   majors / degrees_conferred, minors / degrees_conferred,
                   (majors + minors) / degrees_conferred]
            write_row(department_file, row)
            
def get_all_departments(year2department):
    '''
    This function gets all the departments present across all years from the 
    given dictionary, which is assumed to map from years to (normalized)
    department names.
    '''
    unique_departments = []
    department_names_by_year = [sorted( #Sort the names
                                list(   #Convert to a list
                                item[1]    #Grab the second value of the tuple 
                                .keys()))  #Extract the key (department name)
                                for item in list(year2department.values())]
    for name_set in department_names_by_year:
        for name in name_set:
            if name not in unique_departments:
                unique_departments.append(name)
    unique_departments.sort()
    return unique_departments
    
def write_row(file, row):
    '''
    This function writes a given row to a file that is assumed to a .tsv file.
    It exists because making sure not to write the trailing tab and including 
    newlines is messy.
    '''
    for i, value in enumerate(row):
        file.write(str(value))
        end = "\t" if i != len(row) - 1 else "\n"
        file.write(end)
        
def plot_all_spreadsheets(school):
    all_spreadsheets = os.listdir(department_data_dir)
    school_spreadsheets = list(filter(lambda x: x.startswith(school), 
                                      all_spreadsheets))
    school_spreadsheets.sort()
    top = os.path.join(departmental_plots_dir, school)
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    for i in range(6):
        path = os.path.join(departmental_plots_dir,
                            school,
                            index2description[i])
        if not os.path.isdir(path):
            os.makedirs(path)
    for spreadsheet in school_spreadsheets:
        department_name = spreadsheet.replace(".tsv", "")
        department_name = department_name.replace("%s-" % school, "")
        spreadsheet_file = open(os.path.join(department_data_dir, spreadsheet), 
                                'r')
        years = []
        metrics = [[] for i in range(6)]
        for i, line in enumerate([line.strip()  #Remove the newline
                                  for line in spreadsheet_file]):
            if i != 0:
                data = line.split("\t")
                years.append(int(data[0]))
                for i in range(6):
                    if i == 0 or i == 1:
                        metrics[i].append(int(data[i + 1]))
                    else:
                        metrics[i].append(float(data[i + 1]))
        for i in range(6):
            x = np.array(years)
            y = np.array(metrics[i])
            current_size = plt.gcf().get_size_inches()
            adjustment = [4.5, 6.5]
            new_size = [current_size[i] + adjustment[i] for i in range(len(current_size))]
            plt.figure(figsize = new_size)
            plt.plot(x, y)
            title = '%s - %s - %s' % (school, 
                                      department_name,
                                      index2description[i])
            plt.title(title)
            plt.xlabel('Year')
            plt.ylabel(index2description[i])
            label_text = ["%d-%d" % (year, year + 1) for year in years]
            plt.xticks(years, label_text, rotation = 90)
            plt.savefig(os.path.join(departmental_plots_dir,
                                     school,
                                     index2description[i],
                                     title + ".png"))
            plt.close()
            
def write_out_and_plot_all_department_spreadsheets():
    '''
    This method encapsulates the usual chain of calls to produce all of the 
    departmental spreadsheets.
    '''
    for school in ["cc", "en", "gs"]:
        print(section_separator)
        print(school)
        year_dictionary = extract_year_dictionary(school)
        write_department_spreadsheet = write_spreadsheet(year_dictionary, 
                                                         school)
        plot_all_spreadsheets(school)
        print(section_separator)
    
if __name__ == "__main__":
    write_out_and_plot_all_department_spreadsheets()