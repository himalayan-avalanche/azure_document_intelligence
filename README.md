# Exploiting Azure Document Intelligence Capabilities

## Setup
Refer to https://github.com/himalayan-avalanche/azure_document_intelligence/tree/main/setup for details on installing necessary modeuls and setting up the document intelligence studio.
https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python-preview

Azure Document Intelligences (ADI) allows to perform various tasks powered by powerfull GPT models. The subfolders in this directory will focus on some of the most useful capabolities of ADI.

# Key Concepts

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

