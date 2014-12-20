import xml.etree.ElementTree as ET
from multiprocessing import Pool

def  convert_text_data_to_xml(xml_data):
    text_data=xml_data.text
    return text_data

def  retrieve_patent_data_from_xml(text_data):
     record=ET.fromstring(text_data)
     for rec in record:
         for pantypl in rec:
             pan_of_source_patent=pantypl.get("pan")
             list=retrieve_pan_of_cited_patents(pantypl)
             return {pan_of_source_patent:list}

def retrieve_pan_of_cited_patents(pan_type_xml_element):
    cited_pan_list=[]
    for patent_typ1 in pan_type_xml_element:
        for pci_typ1 in patent_typ1:
            for cited in pci_typ1:
                #cited_patent_element=cited.findall("CitedPt")
                for citedPt in cited:

                    cited_pt_pan=citedPt.get("pan")
                    if cited_pt_pan!=None:
                       if cited_pt_pan not in cited_pan_list:

                          cited_pan_list.append(cited_pt_pan)
    return cited_pan_list

# Given an xml result  on a search by patent id this function returns the pan of the queried patents along with a list of  patents that cited the source patent
def get_ids_of_cited_patents(xml_result):
  root=ET.fromstring(xml_result)
  for soap_envelope in root:
    for soap_body in soap_envelope:
        for return_result in soap_body:
            records=return_result.findall("records")
            for record in records:
                patent_record_text_data=convert_text_data_to_xml(record)
                return retrieve_patent_data_from_xml(patent_record_text_data)
def mp_parsing(pre_parse):

    pool = Pool(processes=2)
    temp_result = pool.map(parser, [pre_parse])
    result = post_thread_processing(temp_result)
    return result

def mp_parsing2(xml_result):

    pool = Pool(processes=2)
    temp_result = pool.apply_async(get_derwent_counts, [xml_result])
    return temp_result.get()

def pre_parser(xml_result):
    pre_parsed_result = []
    root=ET.fromstring(xml_result)
    for soap_envelope in root:
          for soap_body in soap_envelope:
            for return_result in soap_body:
                records=return_result.findall("records")
                for record in records:
                    patent_record_text_data=convert_text_data_to_xml(record)
                    pre_parsed_result = ET.fromstring(patent_record_text_data)
    return pre_parsed_result

def parser(xml_record):
    dce_counts_hash={}
    for rec in xml_record:
        list_of_dce=[]
        for pan_typ1 in rec:
            for patent_typ1 in pan_typ1:
                for tags in patent_typ1:
                    if tags.tag.split("}")[1]=='IndexingCorePtTyp1':
                          for dc in tags:
                               for child_tags in dc:
                                   if child_tags.tag.split("}")[1]=="EPIs":
                                      for epi in child_tags:
                                          for epigp in epi:
                                              for dce in epigp:
                                                  if dce.tag.split("}")[1]=="DCE":
                                                      text=dce.text.split()[0]
                                                      if text  not in list_of_dce:
                                                         list_of_dce+=[text]

                                   elif child_tags.tag.split("}")[1]=="CPIs":

                                      for cpi in child_tags:
                                          for cpi_tags  in cpi:
                                              if cpi_tags.tag.split("}")[1]=="DCCM":
                                                 text=cpi_tags.text.split()[0]
                                                 if text not in list_of_dce:

                                                        list_of_dce+=[text]
                                              if cpi_tags.tag.split("}")[1]=="DCCSs":
                                                 for dccs in cpi_tags:

                                                     text=dccs.text.split()[0]
                                                     if text not in list_of_dce:

                                                        list_of_dce+=[text]
                                   elif child_tags.tag.split("}")[1]=="EngPIs":

                                            for eng_pi in child_tags:
                                                    for dce_engs in  eng_pi:
                                                        for dce_eng  in dce_engs:

                                                            text=dce_eng.text.split()[0]
                                                            if text not in list_of_dce:
                                                               list_of_dce+=[text]


            for dce in list_of_dce:
                if dce in dce_counts_hash.keys():
                   dce_counts_hash[dce]=dce_counts_hash[dce]+1
                else:
                   dce_counts_hash[dce]=1
    return dce_counts_hash



def get_derwent_counts(xml_result):
    root=ET.fromstring(xml_result)
    dce_counts_hash={}
    for soap_envelope in root:
          for soap_body in soap_envelope:
            for return_result in soap_body:
                records=return_result.findall("records")
                for record in records:
                    patent_record_text_data=convert_text_data_to_xml(record)
                    root_record=ET.fromstring(patent_record_text_data)

                    for rec in root_record:

                        list_of_dce=[]
                        for pan_typ1 in rec:
                            for patent_typ1 in pan_typ1:
                                for tags in patent_typ1:
                                    if tags.tag.split("}")[1]=='IndexingCorePtTyp1':
                                          for dc in tags:
                                               for child_tags in dc:
                                                   if child_tags.tag.split("}")[1]=="EPIs":
                                                      for epi in child_tags:
                                                          for epigp in epi:
                                                              for dce in epigp:
                                                                  if dce.tag.split("}")[1]=="DCE":
                                                                      text=dce.text.split()[0]
                                                                      if text  not in list_of_dce:
                                                                         list_of_dce+=[text]

                                                   elif child_tags.tag.split("}")[1]=="CPIs":

                                                      for cpi in child_tags:
                                                          for cpi_tags  in cpi:
                                                              if cpi_tags.tag.split("}")[1]=="DCCM":
                                                                 text=cpi_tags.text.split()[0]
                                                                 if text not in list_of_dce:

                                                                        list_of_dce+=[text]
                                                              if cpi_tags.tag.split("}")[1]=="DCCSs":
                                                                 for dccs in cpi_tags:

                                                                     text=dccs.text.split()[0]
                                                                     if text not in list_of_dce:

                                                                        list_of_dce+=[text]
                                                   elif child_tags.tag.split("}")[1]=="EngPIs":

                                                            for eng_pi in child_tags:
                                                                    for dce_engs in  eng_pi:
                                                                        for dce_eng  in dce_engs:

                                                                            text=dce_eng.text.split()[0]
                                                                            if text not in list_of_dce:
                                                                               list_of_dce+=[text]


                            for dce in list_of_dce:
                                if dce in dce_counts_hash.keys():
                                   dce_counts_hash[dce]=dce_counts_hash[dce]+1
                                else:
                                   dce_counts_hash[dce]=1
    return dce_counts_hash


def aggregate(output_dict, input_dict):
    if output_dict == {}:
        output_dict = input_dict
    else:
        output_key = output_dict.keys()
        input_key = input_dict.keys()
        temp_dict = dict(output_dict, **input_dict)
        for old_code in input_key: #adds up for ones that exist
            for new_code in output_key:
                if new_code == old_code:
                    temp_dict[new_code] = temp_dict[new_code] + output_dict[new_code]
        output_dict = temp_dict

    return output_dict

def post_thread_processing(input_list):
    output_dict = {}
    for each_dict in input_list:
        output_dict = aggregate(output_dict, each_dict)

    global output_list
    output_list = [] #resets the global variable - output_list post-threading.
    return output_dict

def check_for_r(input_dict):
    output = {}
    input_key = input_dict.keys()
    for key in input_key:
        if key [0] != 'R':
            output[key] = input_dict[key]
    return output

def tally(list_of_dcs):
    dce_counts_hash = {}
    for dce in list_of_dcs:
        if dce in dce_counts_hash.keys():
            dce_counts_hash[dce] = dce_counts_hash[dce]+1
        else:
            dce_counts_hash[dce] = 1
    return dce_counts_hash
