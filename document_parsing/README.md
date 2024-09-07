# Document Parsing

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


```
