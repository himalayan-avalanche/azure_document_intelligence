class promptDetails:
    
    def __init__(self):
        pass
        
    def get_metaprompt(self):
    
        #### This returns a generic metaprompt to be used as message to role: system 
        
        system_instruction_intro="Your task is to extract specific data elements from the contents of the given input document (which could be in PDF, JPEG, Word, or other formats). Extract paragraph and table level data seperately and output as per the expected JSON output format described below. Note that table level data elements must come from input table contents only, and paragraph level data must come from document data only. For each data element, provide the extracted value along with a confidence score (from 0 to 1). The output should be presented as a neatly formatted JSON key-value pair."
    
        system_doc_desc_prompt=f"\n For this data extraction task, you will be given a type of document and high level description of the document. You can use the document type and its description as relevant context to further optimize your document relevant data elements extraction task. \n"
        
        output_format_text="""\n Refer below for the expected JSON output format. Use this to extract the relevant data elements values and output in the desired format as given by examples below: \n\n
    
        1. **Extract Data and Output JSON**:
    - Extract data elements from document content into JSON objects. Format extracted data as structured JSON.
    - **Schema**: `{""fields"": {""<data_element_name>"": [{""source"": ""<source>"", ""source_id"": ""<source_id>"", ""value"": ""<value>""}]}}`
        - source: ""paragraph"" or ""table""
        - source_id: the paragraph_id if source is ""paragraph"" or the table_id, row_index, column_index if source is ""table""
        - value: the value of the extracted data element. If the value is missing or n/a, fill the values by 'n/a'
    
    - **Example 1 - Invoice Extraction Data Element Output Format**:
    ```json
    {""fields"": {""Supplier Name"": [{""source"": ""paragraph"", ""source_id"": ""1"", ""value"": ""Spa Supplies Co.""}], ""Item Number"": [{""source"": ""table"", ""source_id"": ""1,1,0"", ""value"": ""1446""}, {""source"": ""table"", ""source_id"": ""1,2,0"", ""value"": ""1447""}]}}
    ```
    
    - **Example 2 - Not Found Data Element Output Format**:
    ```json
    {""fields"": {""Customer Name"": ""n/a""}}
    ```
    '''
     
        """
        
        system_rde_extraction_guidlines="""You can refer below as the guidlines for extracting and outputing the data.\n\n
                                
        ## Guidelines for Precise Output Data
                            
        - **Data Sourcing**: 
                            The given document contents is a json object that contains both paragraph data and table data. Tabular content may 
                            be present in both the paragraph_data and table data fields.
        -**Document-Level Data**: 
                            Document level data elements that will pertain to the entire document (such as invoice number, supplier 
                            name, lease ID, etc.) from the paragraph_data field. Examples of document-Level data includes Invoice Number, 
                            Bank Name, Account Number, Statement Period, etc.
        -**Line-Item-Level Data**: 
                            Extract data elements that pertain to individual line items (such as item number, item quantity, item price, 
                            etc.) from the table_data field. Examples of line-item-level data include Item Number, Item Quantity, 
                            Transactional Details, etc. Keep an eye on the variation in table format to ensure accurate header and line 
                            level data formatting.
        - **Multiple Values**: 
                            Ensure that all occurrences of a data element are extracted. Do not stop after the first occurrence. Accurately 
                            capture and format all instances in the output JSON. If there are multiple tables in the document, output the 
                            Line-Item-Level Data for each tables as seperate table contents json outputs.
        """
    
        system_implementation_guidlines="""
        ## Refer the below on how you need to implement the extraction, formatting, and otuputting the extracted data.
    
        **-- Implementation Task ---
                            Follow the specifications outlined above to extract and format the specified fields from the provided document 
                            data. Review the output of all data elements before implementation to ensure 80% or higher confidence.
    
        1. **Naming Standards**:
                        - Adhere strictly to the specified data element names in the input content, avoiding modifications such as 
                        underscores or hyphens or invalid characters.
        2. **Data Values**:
                            - Extract the exact value of the data present within the input document content, including punctuation. For 
                            example, the content $1,000 should be extracted as $1,000 annd NOT as 1000. If there are invalid characters 
                            aligned with data value, ignore such invalid values. For instance if Unit Quantiy value is |1 or -1, you can 
                            refine the extracted value to 1.
    
        """
        
        system_message = system_instruction_intro + system_doc_desc_prompt + output_format_text + system_rde_extraction_guidlines + system_implementation_guidlines
       
        return {'system_prompt':system_message}


    def get_openai_column_mapped_names_message(self, document_type_name, document_type_description, data_elements_str, table_col_names_str):
        
        user_prompt_message = f"""**Document Type Details:** 
                                    \n Document Type: {document_type_name} 
                                    \n Document Description:{document_type_description}
                                    \n**Data Elements:** \n{data_elements_str} 
                                    \n\n**Document Column Names:** \n{table_col_names_str}"""
        output_guidlines="""
                                  ** Output Guidlines:**
                                  \n Return a strict JSON object with the following schema:
                                  **Schema**: {""<document column name>"": ""<data_element name>""}
                                - document column nam: the document column name from among given document column names
                                - data element name: the value of the mapped data element. If the value is missing or n/a, fill the values by 'n/a'.                                                            """
        
        messages = [
            {"role": "system", "content": "You are a data extractor expert for various documents types and various content type. Your task is to map the document column names to data elements to accurately. To better infer and map the document column names to desired data elements, you are given type of document, and a short description of the documents. You are given document column names and data element names"},
            {"role": "user", "content": user_prompt_message+output_guidlines},
        ]
    
        return messages