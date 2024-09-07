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

print(adi_response['modelId'])
##### prebuilt-invoice

adi_response['content']
##### 'Spa\nSupplies\n68 Vroom Street,\nMedalia City,\nMM 88531\nPhone: 222-222-9000\nFax:\n222-222-9001\nINVOICE\nEmail: tonsofcars@it.com\nBill To:\nOlympic World Hotel.\n55 Comfort Street\nMedalia City,\nMM 88531\nInvoice #:\nPLC0920\nInvoice Date:\nMarch 2,20X3\nCustomer ID:\n124\nVendor No:\n15\nTO number:\nGSQ0415DB0037\nQuantity\nItems\nUnits\nDescri\nDiscount %\nTaxable\nUnit Price\nTotal\n14\nMTBL\n1\nMassage tables\nN/A\nN/A\n$2,300\n$32,200\n-\n14\nTH\n1\nTowel heaters\n-\nN/A\nN/A\n$768\n$10,752\n7\nEWCH\nI\n1\nEntry-way chairs\nN/A\nN/A\n$1,136\n$7,952\n14\nWAX\n1\nWax heaters\nN/A\nN/A\n$987\n$13,818\n16\nSLOU\n1\nSpa loungers\nN/A!\nN/A\n$979\n$15,616\n4\nHTUB\n1\nHot tub\nN/A\nN/A\n$50,613\n$202,453\n12\nPEDC\nI\n1\nPedicure chair\nN/A\nN/A\n$3,456\n$41,472\n4\nDRY\nI\n2\nManicure and Pedicure dryer\nN/A\nN/A\n$1,456\n$5,824\n10\nMANI\n1\n1\nManicure tables\nN/A\nI\nN/A ;\n$2,488\n$24,880\n-\n-\nI\nI\n-\nTotal\n$354,967\nDISCLAIMER: The information contained herein is of a general nature and was created for training purposes and is not intended to\naddress the circumstances of any particular audit engagement. This training is a work of fiction. Any names of persons,\ncompanies, events or incidents, are fictitious. Any resemblance to actual persons, living or dead, companies or actual events is\npurely coincidental.\nInternal use only\n@ 2022 KPMG LLP, a Delaware limited liability partnership and a member firm of the KPMG global organization of independent member firms affiliated with KPMG\nInternational Limited, a private English company limited by guarantee. All rights reserved.'


