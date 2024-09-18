# Exploiting Azure Document Intelligence Capabilities

## Setup
Refer to https://github.com/himalayan-avalanche/azure_document_intelligence/tree/main/setup for details on installing necessary modeuls and setting up the document intelligence studio.
https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python-preview

Azure Document Intelligences (ADI) allows to perform various tasks powered by powerfull GPT models. The subfolders in this directory will focus on some of the most useful capabolities of ADI.

## Key Concepts

### DocumentIntelligenceClient
DocumentIntelligenceClient provides operations for analyzing input documents using prebuilt and custom models through the begin_analyze_document API. Use the model_id parameter to select the type of model for analysis. See a full list of supported models here. The DocumentIntelligenceClient also provides operations for classifying documents through the begin_classify_document API. Custom classification models can classify each page in an input file to identify the document(s) within and can also identify multiple documents or multiple instances of a single document within an input file.

Sample code snippets are provided to illustrate using a DocumentIntelligenceClient here. More information about analyzing documents, including supported features, locales, and document types can be found in the service documentation.

### DocumentIntelligenceAdministrationClient

DocumentIntelligenceAdministrationClient provides operations for:

Building custom models to analyze specific fields you specify by labeling your custom documents. A DocumentModelDetails is returned indicating the document type(s) the model can analyze, as well as the estimated confidence for each field. See the service documentation for a more detailed explanation.
Creating a composed model from a collection of existing models.
Managing models created in your account.
Listing operations or getting a specific model operation created within the last 24 hours.
Copying a custom model from one Document Intelligence resource to another.
Build and manage a custom classification model to classify the documents you process within your application.
Please note that models can also be built using a graphical user interface such as Document Intelligence Studio.


## Document Parsing

Using Azure Document Intelligence (ADI), once can parse various document types such as pdf, text, word, images etc and various content types such as paragraphs, tables, image info. The ADI has many prebuild models to choose from, and often they do better job than default layout model as document type specific models are fine tunes for parsing from specific type of documents. 

## Supported prebuild Document Models

Some of the prebuilt model types are:

1. Invoice, Model ID: prebuilt-invoice
2. Business Card, Model ID: prebuilt-businessCard
3. Bank Statement, Model ID: prebuilt-bankStatement
4. Tax Documents, Model ID: prebuilt-tax.us
5. Contract Document, Model ID: prebuilt-contract
6. Check, Model ID: prebuilt-check
7. health Insuarce Card, Model ID: prebuilt-healthInsuranceCard.us
8. ID Document, Model ID: prebuilt-idDocument
9. Morgage, Model ID: prebuilt-mortgage
10. Pay Stub, Model ID: prebuilt-paystub


Refer this link for model details: : https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/language-support-prebuilt?view=doc-intel-4.0.0&tabs=languages%2Cthermal

## Example of ID Document Model ID

<img width="725" alt="image" src="https://github.com/user-attachments/assets/bd741971-938c-4ba2-9249-74f59bae9cd7">


## Parsing the document content using Python API for ADI

```python
import os
import time
import numpy as np
import openai
from openai import AzureOpenAI
from importlib import reload
import sys

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence import DocumentIntelligenceClient

#### Load the Sample Invoice File

file_name="./uploads/Sample_Invoice.pdf"
```
#### Sample Invoice file

<img width="660" alt="image" src="https://github.com/user-attachments/assets/d00c7399-5a7c-48c8-9600-0425c76001b4">

```python

#### Define a function to ADI parsed contents using Azure Document Intelligence Client

def get_azure_parsed_contents(file_data):

    adi_end_point=os.getenv("AZURE_ENDPOINT")
    adi_api_key=os.getenv("AZURE_KEY")

    document_analysis_client=DocumentIntelligenceClient(
            endpoint=adi_end_point, 
            credential=AzureKeyCredential(adi_api_key)
            )
    
    poller=document_analysis_client.begin_analyze_document("prebuilt-invoice",
                analyze_request=file_data,
                content_type="application/octet-stream"
                )
    
    result = poller.result()

    return result

st_time=time.time()
file_data = open(file_name, "rb")
adi_response=get_azure_parsed_contents(file_data)
en_time=time.time()
print(f"Time elapsed: {np.round(en_time-st_time,2)} seconds.")
##### Time elapsed: 13.53 seconds.

print(type(adi_response))
##### <class 'azure.ai.documentintelligence.models._models.AnalyzeResult'>

print(adi_response.keys())
##### dict_keys(['apiVersion', 'modelId', 'stringIndexType', 'content', 'pages', 'tables', 'styles', 'documents', 'contentFormat'])

"""
apiVersion:       This is API version used. The current api version is "'2024-02-29-preview'"
modelId:          This is model ID used. Here it is "prebuilt-invoice"
content:          This is content of the document as parsed by ADI client.
pages:            Number of pages in the input document.
tables:           This tables content in the document. Tables includes list of any table like content in the input documents and not necsssarily explit tables from document.
documents:        Contains document specific contents such as ['docType', 'boundingRegions', 'fields', 'confidence', 'spans'].
"""

```

### Parsing Document Level and Table level Data Elements

The pages field contains documents content page by page, which can be parsed using python to extract document level data elements.

```python
adi_response['pages'][0].keys()
##### dict_keys(['pageNumber', 'angle', 'width', 'height', 'unit', 'words', 'lines', 'spans'])
```
There is only one page in this input document. We can count total number of words in the document by:

```python
len(adi_response['pages'][0]['words'])
##### 253

adi_response['pages'][0]['words'][:2]
##### [{'content': 'Spa', 'polygon': [2.4927, 1.0217, 3.6913, 1.0026, 3.7056, 1.6185, 2.507, 1.6328], 'spans': [{'offset': 0, 'length': 3}]},
 {'content': 'Supplies', 'polygon': [2.6169, 1.7378, 4.9472, 1.7283, 4.9472, 2.3537, 2.6169, 2.3633], 'spans': [{'offset': 4, 'length': 8}]}]

adi_response['pages'][0]['spans']
##### [{'offset': 0, 'length': 1490}]

adi_response['pages'][0]['lines']
##### 126

adi_response['pages'][0]['width']
##### 8.5

adi_response['pages'][0]['height']
##### 11

adi_response['pages'][0]['unit']
##### inch

adi_response['pages'][0].keys()
##### dict_keys(['pageNumber', 'angle', 'width', 'height', 'unit', 'words', 'lines', 'spans'])

page=adi_response.pages[0]
line=page['lines'][0]

print(line)
##### {'content': 'Spa', 'polygon': [2.4927, 1.0217, 3.6913, 1.0026, 3.7056, 1.6185, 2.507, 1.6328], 'spans': [{'offset': 0, 'length': 3}]}

### Here
##### content: text content
##### polygon: Polygon here describes the four corners of a rectangular boundary around the recognized text.
	The points follow the sequence of:
	1.	Top-left corner (x1, y1)
	2.	Top-right corner (x2, y2)
	3.	Bottom-right corner (x3, y3)
	4.	Bottom-left corner (x4, y4)
##### spans: span of the text i.e. offset and length of text on the page.


```

### Using OpenAI API to parse ADI extracted content to structured output format

The document can contain both document level data elements and table level data elements. Though the response from ADI API call is structured, however the table level data elements can be both part of document level "documents" field and "tables" field in the ADI response. To seperate the document level output from table level data elements output, we can use OpenAI API chat completion call with metaprompt to parse document level and table level elements in structured JSON format, which can be formatted to a pandas dataframe for easier view.

#### Step 1. Load necessary python modules
Note that you would have to have access to OpenAI API key to use the chat completion API. The files https://github.com/himalayan-avalanche/azure_document_intelligence/blob/main/document_parsing/baseDocumentParser.py and https://github.com/himalayan-avalanche/azure_document_intelligence/blob/main/document_parsing/basePromptDetails.py contains documentParser and promptDetails classes that implements the necessary functions to parse the ADI responses to structured responses.

```python
import os
import time
import numpy as np
import openai
from importlib import reload
import sys
from openai import OpenAI

import baseDocumentParser
reload(baseDocumentParser)
from baseDocumentParser import *

import basePromptDetails
reload(basePromptDetails)
from basePromptDetails import promptDetails

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

documentParser=documentParser()
promptDetails=promptDetails()

#### path of sample invoice document

file_name="./uploads/Sample_Invoice.pdf"

#### Specify document details: document type, short description, and data elements to be extracted

document_type_name="Invoice"
document_type_description="""An invoice is a formal document issued by a seller to a buyer, detailing a transaction. It outlines the goods or services provided, their quantities, unit prices, and the total amount owed. Key data elements in an invoice include the invoice number, issue date, buyer and seller contact details, item descriptions, unit prices, taxes, discounts, payment terms, and the total payable amount. The primary purpose of an invoice is to request payment, provide a record of the transaction, and facilitate accounting and tax reporting for both parties involved in the business transaction."""
data_elements="""Invoice Number, Invoice Date, Supplier Name, Buyer Name, Item Description, Quantity, Unit Price, Total Amount, Tax Amount, Payment Terms"""

data_elements_str="\n".join(data_elements.split(", "))
data_elements_str
##### 'Invoice Number\nInvoice Date\nSupplier Name\nBuyer Name\nItem Description\nQuantity\nUnit Price\nTotal Amount\nTax Amount\nPayment Terms'

#### Call ADI parser to extract document contents

file_data = open(file_name, "rb")
model_id="prebuilt-invoice"
adi_response=documentParser.get_azure_parsed_contents(file_data, model_id)

##### TO pass the message to OpenAI chat completion, we need metapromot and document level and table level contents as json dump object.

table_level_data=documentParser.get_table_contents(adi_response)
document_level_data=documentParser.get_document_contents(adi_response)
doc_json = {"paragraph_data": document_level_data, "table_data" : table_level_data}

#### OpenAI api call to parse the document level data elements

prompts_details=promptDetails.get_metaprompt()
system_prompt_message=prompts_details['system_prompt']
model="gpt-4o"
response_format="json_object"

user_prompt_message = f"""**Document Type Details:** 
                            \n Document Type: {document_type_name} 
                            \n Document Description:{document_type_description}
                            \n**Data Elements for Extraction:** \n{data_elements_str} 
                            \n\n**Document Content:** \n{json.dumps(doc_json)}"""

messages = [
    {"role": "system", "content": "You are a data extractor expert for various documents types and various content type" + system_prompt_message},
    {"role": "user", "content": user_prompt_message},
]


status, openai_response=documentParser.get_openai_formatted_response(messages=messages)
response_json=documentParser.json_post_process(openai_response)


#### Parse the document details to paragraph and table dataframes
While a given document may contain fields wuth varied names, if we want the document table column names mapped to prespecified data elements, we can use OpenAI chat completion to map the document's table column name to data elements as column names.

table_col_names_str="\n".join(documentParser.get_table_col_names(doc_json))

message_col_names=promptDetails.get_openai_column_mapped_names_message(document_type_name, document_type_description, data_elements_str, table_col_names_str)
status, openai_response_col_names=documentParser.get_openai_formatted_response(messages=message_col_names)

table_cols_to_data_elements_dict=documentParser.json_post_process(openai_response_col_names)

table_cols_to_data_elements_dict

##### From the given Invoice.pdf document, we can map the document column name to desired data element cokumn names.
{'Quantity': 'Quantity',
 'Items': 'n/a',
 'Units': 'n/a',
 'Descri': 'Item Description',
 'Discount %': 'n/a',
 'Taxable': 'Tax Amount',
 'Unit Price': 'Unit Price',
 'Total': 'Total Amount'}


para_dict=documentParser.get_para_dict(response_json)
documentParser.get_para_df(para_dict)
```
<img width="302" alt="image" src="https://github.com/user-attachments/assets/68dd98e8-4a9d-4c4c-b16f-f709cac009d0">

```python
#### Next extract the table level data elements dataframe.

table_list=documentParser.get_table_dict(response_json)

table_cols=[x[0] for x in table_list]
documentParser.get_table_col_names(doc_json)
######
['Quantity',
 'Items',
 'Units',
 'Descri',
 'Discount %',
 'Taxable',
 'Unit Price',
 'Total']

documentParser.get_table_col_names(doc_json)

data_elements_order={x.strip():i for i,x in enumerate(data_elements.split(","))}
table_df=documentParser.get_table_dataframe(doc_json, table_cols_to_data_elements_dict, data_elements_order)
table_df
```
<img width="680" alt="image" src="https://github.com/user-attachments/assets/9698d570-f958-4dd2-8281-a1996abe46b5">



