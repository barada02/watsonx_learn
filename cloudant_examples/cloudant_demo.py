import os
from pathlib import Path

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, Document


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key and key not in os.environ:
            os.environ[key] = value


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    load_env_file(repo_root / ".env")

    api_key = os.environ.get("CLOUDANT_APIKEY") or os.environ.get("API_KEY")
    instance_url = os.environ.get("CLOUDANT_URL")

    if not api_key or not instance_url:
        raise SystemExit("Missing CLOUDANT_APIKEY/API_KEY or CLOUDANT_URL in environment or .env")

    # 1. Setup IAM authentication
    authenticator = IAMAuthenticator(api_key)

    # 2. Initialize the service client
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(instance_url)

    # Test the connection
    response = service.get_server_information().get_result()
    print("Server Information:")
    print(response)
    print("-" * 40)

    # 3. Create a Database
    db_name = "test_database_001"
    print(f"Creating database '{db_name}'...")
    try:
        service.put_database(db=db_name).get_result()
        print("Success! Database created.")
    except ApiException as e:
        if e.code == 412:
            print("Database already exists. Proceeding...")
        else:
            raise e

    # 4. Insert a Document
    print("\nInserting a document...")
    doc = Document(
        name="Bob",
        role="Virtual Agent",
        skills=["Text-to-Speech", "Cloudant", "Speech-to-Text"]
    )
    
    try:
        # Use put_document to specify the doc_id explicitly
        response = service.put_document(db=db_name, doc_id="user_bob", document=doc).get_result()
        print(f"Document created! ID: {response['id']}")
    except ApiException as e:
        if e.code == 409:
            print("Document ID 'user_bob' already exists. Skip creation.")
        else:
            raise e

    # 5. Read the Document Back
    print("\nReading document 'user_bob'...")
    try:
        doc_read = service.get_document(db=db_name, doc_id="user_bob").get_result()
        print("Found Document Data:")
        print(doc_read)
    except ApiException as e:
        print(f"Could not read document: {e.message}")

if __name__ == "__main__":
    main()
