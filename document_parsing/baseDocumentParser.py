import datetime
import os
import re
import json
import time
import openai
from openai import AzureOpenAI
import httpx
import textwrap
import traceback
import pandas as pd
import concurrent.futures
from logging import Logger

import io
from importlib import reload
import pickle
import sys
import numpy as np


class documentParser:
    
    def __init__(self):

        from openai import OpenAI
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.documentintelligence import DocumentIntelligenceClient

        adi_end_point=os.getenv("AZURE_ENDPOINT")
        adi_api_key=os.getenv("AZURE_KEY")
        
        self.azure_doc_client=DocumentIntelligenceClient(
                endpoint=adi_end_point, 
                credential=AzureKeyCredential(adi_api_key)
                )
        
        self.open_ai_client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_azure_parsed_contents(self, file_data, model_id):
        
        poller=self.azure_doc_client.begin_analyze_document(model_id,
                    analyze_request=file_data,
                    content_type="application/octet-stream"
                    )
        
        result = poller.result()
    
        return result
        
    def create_table_content_from_invoice_documents(self, one_table):
        table_details = {
                        "row_count"    : one_table["rowCount"],
                        "column_count" : one_table["columnCount"],
                        "cells" : []
                        }
    
        for one_cell in one_table["cells"]:
            if 'kind' in one_cell:
                kind=one_cell["kind"]
            else:
                kind='values'
            
            table_details["cells"].append({ "row_index"    : one_cell["rowIndex"],
                                        "column_index" : one_cell["columnIndex"],
                                        "content"      : one_cell["content"],
                                        "kind"         : kind
                                     })
            
                
        
        return table_details

    def get_paragraph_contents(self, tmp):
        doc_contents={}
        keys=tmp.keys()
        for k in keys:
            if not k in ['content', 'boundingRegions', 'spans']:
                doc_contents[k]=tmp[k]        

        return doc_contents
    
    def get_dict_object(self, ob):
        aa={}
        for k in ob:
            aa[k]=ob[k]
        return aa
        
    def get_document_contents(self, adi_response):
        
        fields=adi_response['documents'][0]['fields']
        doc_content={}
        doc_tracker=0
        
        for f in fields:
            doc_tracker+=1
            field_content=adi_response['documents'][0]['fields'][f]
            
            if field_content['type']=='array':
                pass
            else:
                doc_content[doc_tracker]={}
                
                if field_content['type'] in ['address', 'currency']:
                    field_content=self.get_dict_object(field_content['value'+field_content['type'].title()])
                    doc_content[doc_tracker][f]=self.get_paragraph_contents(field_content)
                else:
                    doc_content[doc_tracker][f]=self.get_paragraph_contents(field_content)
    
        return doc_content
    
    def create_table_content_from_invoice_documents(self, one_table):
        table_details = {
                        "row_count"    : one_table["rowCount"],
                        "column_count" : one_table["columnCount"],
                        "cells" : []
                        }
    
        for one_cell in one_table["cells"]:
            if 'kind' in one_cell:
                kind=one_cell["kind"]
            else:
                kind='values'
            
            table_details["cells"].append({ "row_index"    : one_cell["rowIndex"],
                                        "column_index" : one_cell["columnIndex"],
                                        "content"      : one_cell["content"],
                                        "kind"         : kind
                                     })
        
        return table_details
    
    def get_table_contents(self, adi_response):
        adi_tables=adi_response['tables']
        table_tracker = 0
        table_contents = {}
    
        if adi_tables:
            for one_table in adi_tables:
                table_tracker += 1
                table_contents[str(table_tracker)] = self.create_table_content_from_invoice_documents(one_table)
    
        return table_contents
    
    def get_openai_formatted_response(self, messages):
        response_content = ""
        try:
            response = self.open_ai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                seed=42
            )
    
            return True, response.choices[0].message.content
                
        except Exception as e:
            raise print(f"Error in OpenAI API call: {e}", e)
    
    
    def json_post_process(self, output):
        json_match = re.search("```json\n(.*?)\n```", output, re.DOTALL)
        if json_match:
            json_output = json.loads(json_match.group(1))
        else:
            json_output = eval(output)
        return json_output
    
    
    def get_para_dict(self, response_json):
        fields=response_json['fields']
        para_list=[]
        for f in fields:
            if fields[f]!='n/a':
                if fields[f][0]['source']=='paragraph':
                    row={'field':f, 'value':fields[f][0]['value'], 'source_id':fields[f][0]['source_id']}
                    para_list.append(row)
    
        return para_list
        
    def get_table_dict(self, response_json):
        fields=response_json['fields']
        table_rows=[]
        field_keys=[f for f in fields if fields[f]!='n/a']
        col_names=[f for f in field_keys if fields[f][0]['source']=='table']
        
        for f in col_names:
            table_rows.append([f,fields[f]])
    
        return table_rows
    
    def get_para_df(self, para_dict):
        tmp=pd.DataFrame(columns=['data element','data value','source_id'])
        p_iter=iter(para_dict)
        for _ in range(len(para_dict)):
            items=next(p_iter)
            row=[[items['field'], items['value'], items['source_id']]]
            tmp=pd.concat([tmp,pd.DataFrame(row, columns=tmp.columns)])
    
        return tmp.sort_values(['source_id'])[['data element','data value']]
    
    def get_table_col_names(self, doc_json):
        
        table_data=doc_json['table_data']['1']
        n_rows=table_data['row_count']
        n_cols=table_data['column_count']
        
        c_names=[]
        for cell in table_data['cells']:
            if cell['kind']=='columnHeader':
                c_names.append([cell['content'],cell['row_index'],cell['column_index']])
        
        c_names.sort(key= lambda x: (x[1], x[2]))
        if max([x[1] for x in c_names])==0:
            col_names=[x[0] for x in c_names]
    
        return col_names
    
    def get_table_dataframe(self, doc_json, table_cols_to_data_elements_dict, data_elements_order):
        table_data=doc_json['table_data']['1']
        n_rows=table_data['row_count']
        n_cols=table_data['column_count']
        
        c_names=[]
        for cell in table_data['cells']:
            if cell['kind']=='columnHeader':
                c_names.append([cell['content'],cell['row_index'],cell['column_index']])
        
        c_names.sort(key= lambda x: (x[1], x[2]))
        if max([x[1] for x in c_names])==0:
            col_names=[x[0] for x in c_names]
        
        values_list=[]
        for cell in table_data['cells']:
            if cell['kind']=='values':
                values_list.append([cell['content'],cell['row_index'],cell['column_index']])
        
        values_list.sort(key= lambda x: (x[1], x[2]))
        data_frame_rows=[[] for _ in range(n_rows)]
        
        for i in range(len(values_list)):
            row_count=values_list[i][1]-1
            data_frame_rows[row_count].append(values_list[i][0])
        
        tmp_df=pd.DataFrame(data_frame_rows,columns=col_names)
        last_row=tmp_df.iloc[-1]
        if len(last_row.isna())==sum(last_row.isna()):
            tmp_df=tmp_df.iloc[:-1]
    
        tmp_df=tmp_df.rename(columns=table_cols_to_data_elements_dict)
        a=[[x,y] for x,y in data_elements_order.items() if x in table_cols_to_data_elements_dict.values()]
        col_names_final=[x[0] for x in a]
        
        return tmp_df[col_names_final]