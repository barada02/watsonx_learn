import os
from pathlib import Path

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1


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


if __name__ == "__main__":
    main()
