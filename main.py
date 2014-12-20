from xlio import *
from auth import *
from parse import *
from search import *
from retrieveById import *
import time
import multiprocessing
import os
import sqlite3



def main(file_dir):
    '''
    Prerequisites: You must purchase the Web of Knowledge subscription from Thomson Reuters.
    SID numbers must be passed in from auth.py
    Template filename must be in the following format. "companyname".xlsx
    Main directory with patent numbers is folder_dir = '/Users/James/Documents/'.
    Opens the excel file that contains source patent numbers and examines the backward citing 
    patents for each source patent.
    The backward citing patents' derwent technological classification numbers and their respective
    counts will be recorded in the database.
    '''
    conn = sqlite3.connect("patent_database.db") #creates a patent database.
    cursor = conn.cursor()
    print "Start Time: ", time.strftime('%X %x %Z')
    #Start a counter here so you can renew your SID when 3.5 hours have passed.
    comp_name = file_dir
    patent_dict = xl_in(comp_name, 10, "") # insert "" for a full list.
    # note that when importing a raw dataset, you must change patent_dict to raw_xl_in()[0] since
    # the output is a tuple: (patent_dict, citing_pat_dict)
    # patents in the xl file should not have a hyphen as the input module adds them.

    sid_list = authlist(3, 'up', 1, 2)
    SID = sid_list #You may hard-code the SID list as such: SID = ['SID1', 'SID2']
    

    patent_list = patent_dict.keys()

    print 'Number of patents', len(patent_list)
    print 'Estimated Time: ', (len(patent_list) * 0.35), 'minutes'

    max_count = 500
    i = 0
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name="+'"'+comp_name+'"') # check if the database table exists.
    if len(cursor.fetchall()) == 0: # if the database table does not exist, then make one.
        create_table="CREATE TABLE"+'"' + comp_name + '"'+ "(patent_number text, derwent_code text, derwent_count float)"
        cursor.execute(create_table) # creates a table...
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'invalid_pats'") # check if the database table exists.
    if len(cursor.fetchall()) == 0: # if the invalid table does not exist, then make one.
        invalids="CREATE TABLE"+'invalid_pats'+ "(comp_name text, patent_number text)"
        cursor.execute(invalids) # creates a table...
    for patent_no in patent_list:
        cursor.execute("SELECT patent_number FROM " + comp_name)
        rawpat_db = cursor.fetchall()
        patents_in_db = []
        for pat in rawpat_db:
            patents_in_db.append(pat[0])

        if patent_no not in patents_in_db:
            i = i + 1 #initiate the counter.
            print patent_no, 'Count: ', i
            throttle_time = 0.2
            try:
                search_result = search('PN', str(patent_no), 3, 5, SID[0]) #SID[0]
            except:
                conn.close()
                break
            output_dict = get_ids_of_cited_patents(search_result)
            if output_dict == None:
                db_insert="insert into "+'invalid_pats'+ " ('comp_name', 'patent_number') values "+\
                                          "('" + comp_name + "' ,'" + patent_no + "')"
                cursor.execute(db_insert)
            else:
                uid_source_pat = output_dict.keys()[0]
                cited_uid_list = output_dict[uid_source_pat]
                number_cited = len(cited_uid_list)
                print 'number cited', number_cited
                if number_cited > max_count: 
                #handles the case in which there are too many cited patents. 
                #In this case, the script sends a second request to collect the remaining counts.
                    derwent_count_loop = {} # initializes the output
                    for num_loops in range(1, (number_cited // max_count) + 1):

                        SID_counter = num_loops % len(SID) #SID[(num_loops % 2)] alternates between 0 and 1 to avoid being throttled out.
                        start_record = ((num_loops - 1) * max_count) + 1
                        try:
                            cited_search_result = retrieve_by_id(cited_uid_list, 3, start_record, max_count, SID[SID_counter])
                        except:
                            conn.close()
                            break
                        iter_derwent_counts = get_derwent_counts(cited_search_result)
                        derwent_count_loop = aggregate(derwent_count_loop, iter_derwent_counts)

                    start_record = int(number_cited / max_count) * max_count + 1
                    remainder_count = number_cited % max_count
                    try:
                        remainder_search_result = retrieve_by_id(cited_uid_list, 3, start_record, remainder_count, SID[0]) 
                        # handles the remaining cited patents
                    except:
                        conn.close()
                        break
                    remainder_derwent_counts = get_derwent_counts(remainder_search_result)
                    derwent_counts = aggregate(derwent_count_loop, remainder_derwent_counts)

                elif number_cited != 0:
                    try:
                        cited_search_result = retrieve_by_id(cited_uid_list, 3, 1, number_cited, SID[0]) #SID[]
                    except:
                        conn.close()
                        break
                    derwent_counts = get_derwent_counts(cited_search_result)

                if number_cited < 5:
                    time.sleep(throttle_time)
                if number_cited == 0:
                    final_output = {0:0} #no cited patents
                elif derwent_counts == {}:
                    final_output = {'parse error':0}
                else:
                    final_output = check_for_r(derwent_counts) #creates a dict without an R class code.
                    # sample final output: {derwentcode1: count, derwentcode2: count...} counts are floats.
                for derwent_code in final_output.keys():
                    db_insert="insert into "+'"'+ comp_name +'"'+ " ('patent_number', 'derwent_code', 'derwent_count') values "+\
                                          "('" + patent_no + "' ,'" + derwent_code + "' ,'"  + final_output[derwent_code] + "')"
                    cursor.execute(db_insert)


        print "End Time: ", time.strftime('%X %x %Z')
if __name__ == '__main__':
    folder_dir = '/Users/James/Documents/'
    os.chdir(folder_dir)
    file_list = []
    for files in os.listdir("."):
        if files.endswith(".xlsx"):
            file_list.append(folder_dir+'/'+files)
    conn = sqlite3.connect("patent_database.db")
    pool = Pool(processes=2)
    pool.map(main, file_list)



