import xlrd, xlwt, csv


def xl_in(file_dir, start_row, end_row):
    #start block quote here
    #read in template workbook. Activate when you get database access.
    #adds hyphens to patent numbers
    pat_col = 1
    start_row = start_row - 1
    tempWorkBook = xlrd.open_workbook(file_dir)
    tempWorkSheet = tempWorkBook.sheet_by_index(0)
    if end_row == "":
        num_rows = tempWorkSheet.nrows
    else:
        num_rows = end_row
    patent_dict = {}

    for current_row in range(start_row, num_rows):
        patent_no = str(tempWorkSheet.cell_value(current_row, pat_col))
        patent_no = patent_no[:9] + "-"+ patent_no[9:]          #adds a hyphen to the patent no
        priority_year = int(tempWorkSheet.cell_value(current_row, 2))
        application_year = int(tempWorkSheet.cell_value(current_row,3))
        patent_dict[patent_no] = (priority_year, application_year)# creates a tuple of priority year, application year
    return patent_dict

def raw_xl_in(company_name, start_row, end_row):
    '''start block quote here
    When using raw_xl_in, you must have an error handler as many patent included in the raw data file
    are international patents.
    read in template workbook. Activate when you get database access.
    adds hyphens to patent numbers
    Only outputs US patents, Discards Invalid patents exceeding lengths of 12.
    it should output a tuple: ({USPATNO1:PRIORITYYEAR, USPATNO2:PRIORITYYEAR2,...},
    {USPATNO1:[CITEDPATNO1, CITEDPATNO2, CITEDPATNO3,...], USPATNO2:[....]})
    '''
    pat_col = 0
    citing_pat_col = 6
    cited_pat_col = 5
    start_row = start_row - 1
    tempWorkBook = xlrd.open_workbook(company_name + '.xlsx')
    tempWorkSheet = tempWorkBook.sheet_by_index(0)
    if end_row == "":
        num_rows = tempWorkSheet.nrows
    else:
        num_rows = end_row
    patent_dict = {}
    citing_patent_dict = {}
    cited_patent_dict = {}
    for current_row in range(start_row, num_rows):
        patent_no = str(tempWorkSheet.cell_value(current_row, pat_col))
        patent_no = patent_no[:9] + "-"+ patent_no[9:]
        citing_patent_string = tempWorkSheet.cell_value(current_row, citing_pat_col)
        temp_patent_list = citing_patent_string.split("|")
        citing_patent_list = []
        for patent_string in temp_patent_list:
            citing_patent = patent_string.strip()
            if len(citing_patent) < 12:
                #discards the citing patents longer than 11.
                citing_patent = citing_patent[:9]+"-"+citing_patent[9:]
                citing_patent_list.append(citing_patent)
        priority_year = int(tempWorkSheet.cell_value(current_row, 1))
        application_year = int(tempWorkSheet.cell_value(current_row,9))

        citing_patent_dict[patent_no] = citing_patent_list
        cited_patent_string = tempWorkSheet.cell_value(current_row, cited_pat_col)
        temp_cited_patent_list = cited_patent_string.split("|")
        cited_patent_list = []
        for cited_patent_string in temp_cited_patent_list:
            cited_patent = cited_patent_string.strip()
            if len(cited_patent) < 12 and cited_patent[:2]=='US':
                #discards the citing patents longer than 11.
                #discards non-US patents
                cited_patent = cited_patent[:9]+"-"+cited_patent[9:]
                cited_patent_list.append(cited_patent)
        patent_dict[patent_no] = (priority_year, application_year)# creates a tuple of priority year, application year
        cited_patent_dict[patent_no] = cited_patent_list
    return (patent_dict, citing_patent_dict, cited_patent_dict)[0] #for now, the raw xl input only returns a source patent dict.

def xl_out(company_name, patent_dict, final_output, citation):
    '''
    creates an output excel file. This is not used in main.py but it can be used on demand.
    columns: Reference Patents, Patent Number, Earliest Priority Year, Derwent Class Code, Counts
    '''
    #citation should say cited or citing.
    out_workbook = xlwt.Workbook()
    out_worksheet = out_workbook.add_sheet('Reference Patents', cell_overwrite_ok = True)
    out_worksheet.write (0, 1, 'Patent Number')
    out_worksheet.write (0, 2, 'Earliest Priority Year')
    out_worksheet.write (0, 3, 'Derwent Class Code')
    out_worksheet.write (0, 4, 'Counts')
    patent_list = patent_dict.keys()
    row = 1
    for patent_no in patent_list:
        #patent_no = patent_no[:9] + "-"+ patent_no[9:]          #Omitted. Hyphen added in xl_in. adds a hyphen to the patent no.
        dc_dict = final_output[patent_no]
        dc_list = dc_dict.keys()
        for derwent_code in dc_list:
            out_worksheet.write(row, 1, patent_no)
            out_worksheet.write(row, 2, int(patent_dict[patent_no]))
            out_worksheet.write(row, 3, str(derwent_code))
            out_worksheet.write(row, 4, int(dc_dict[derwent_code]))
            row = row + 1

    citation = citation.lower()
    if citation == 'cited':
        out_workbook.save(company_name + ' Cited.xls')
    elif citation == 'citing':
        out_workbook.save(company_name + ' Citing.xls')
    else:
        print "Citation input should either be 'cited' or 'citing'."

def xl_out_with_app_year(company_name, patent_dict, final_output, citation):
    #citation should say cited or citing.
    out_workbook = xlwt.Workbook()
    out_worksheet = out_workbook.add_sheet('Reference Patents', cell_overwrite_ok = True)
    out_worksheet.write (0, 1, 'Patent Number')
    out_worksheet.write (0, 2, 'Earliest Priority Year')
    out_worksheet.write (0, 3, 'Application Year')
    out_worksheet.write (0, 4, 'Derwent Class Code')
    out_worksheet.write (0, 5, 'Counts')
    patent_list = patent_dict.keys()
    row = 1
    for patent_no in patent_list:
        #patent_no = patent_no[:9] + "-"+ patent_no[9:]          #Omitted. Hyphen added in xl_in. adds a hyphen to the patent no.
        dc_dict = final_output[patent_no]
        dc_list = dc_dict.keys()
        for derwent_code in dc_list:
            out_worksheet.write(row, 1, patent_no)
            out_worksheet.write(row, 2, int(patent_dict[patent_no][0])) #Priority Year
            out_worksheet.write(row, 3, int(patent_dict[patent_no][1])) #Application Year
            out_worksheet.write(row, 4, str(derwent_code))
            out_worksheet.write(row, 5, int(dc_dict[derwent_code]))
            row = row + 1

    citation = citation.lower()
    if citation == 'cited':
        out_workbook.save(company_name + ' Cited.xls')
    elif citation == 'citing':
        out_workbook.save(company_name + ' Citing.xls')
    else:
        print "Citation input should either be 'cited' or 'citing'."

def csv_out(company_name, patent_dict, final_output, citation):
    '''
    creates an output csv file. This is not used in main.py but it can be used on demand.
    '''
    #citation should say cited or citing.
    citation = citation.lower()
    if citation == 'cited':
        out_file = open(company_name + ' Cited.csv', 'wb')
    elif citation == 'citing':
        out_file = open(company_name + ' Citing.csv', 'wb')
    else:
        print "Citation input should either be 'cited' or 'citing'."

    writer = csv.writer(out_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow (['Patent Number',
                      'Earliest Priority Year',
                      'Application Year',
                      'Derwent Class Code',
                      'Counts'])
    patent_list = patent_dict.keys()
    for patent_no in patent_list:
        #patent_no = patent_no[:9] + "-"+ patent_no[9:]      #adds a hyphen to the patent no
        dc_dict = final_output[patent_no]
        dc_list = dc_dict.keys()
        for derwent_code in dc_list:
            writer.writerow([patent_no,
                             patent_dict[patent_no][0],
                             patent_dict[patent_no][1],
                             derwent_code,
                             int(dc_dict[derwent_code])])
    out_file.close()


