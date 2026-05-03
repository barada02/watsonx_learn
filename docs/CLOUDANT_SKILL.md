# IBM Cloudant quick start

Portable quick start for connecting to and interacting with IBM Cloudant via Python.

## Prereqs

- Python 3.8+ recommended
- Package installed: `ibmcloudant >= 0.11.5`

## Environment variables

Set these in your environment (or in a `.env` file your app loads):

- `CLOUDANT_APIKEY`
- `CLOUDANT_URL`

## Operations Example

Use your own script to call Cloudant. At minimum you need:

- IAM API key and service URL
- The `ibmcloudant` SDK

Example (Python, Create DB and Document):

```python
import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.api_exception import ApiException

# 1. Setup IAM authentication
authenticator = IAMAuthenticator(os.environ["CLOUDANT_APIKEY"])
service = CloudantV1(authenticator=authenticator)
service.set_service_url(os.environ["CLOUDANT_URL"])

# 2. Create a Database
db_name = "my_test_database"
try:
    service.put_database(db=db_name).get_result()
    print(f"Database '{db_name}' created.")
except ApiException as e:
    if e.code == 412:
        print(f"Database '{db_name}' already exists.")
    else:
        raise

# 3. Create a Document
doc = Document(
    id="doc_001",
    name="Bob",
    role="Agent",
    status="Active"
)

response = service.post_document(
    db=db_name,
    document=doc
).get_result()
print(f"Document created with ID: {response['id']}")

# 4. Read the Document
doc_read = service.get_document(
    db=db_name,
    doc_id="doc_001"
).get_result()

print(f"Retrieved Document: {doc_read}")
```

## Useful Notes

- Use `Document` class or standard Python dictionaries for payloads.
- Status `412` is returned when recreating a DB that already exists; `404` when getting a non-existent doc.
- By default, documents require an `_id` field. If not provided, Cloudant auto-generates one. In the SDK, use `id` without the underscore to set the document ID.