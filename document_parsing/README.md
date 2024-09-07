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



