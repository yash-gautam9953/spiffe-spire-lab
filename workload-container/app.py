import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from spiffe.workloadapi.x509_source import X509Source

SOCKET_PATH = os.environ.get(
    "SPIFFE_ENDPOINT_SOCKET", "unix:///opt/spire/sockets/workload_api.sock"
)
OUTPUT_DIR = Path(os.environ.get("SVID_OUTPUT_DIR", "/tmp/svid"))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with X509Source(socket_path=SOCKET_PATH, timeout_in_seconds=15) as source:
        svid = source.get_x509_context().default_svid
        certificate_path = OUTPUT_DIR / "svid-chain.pem"
        private_key_path = OUTPUT_DIR / "svid-key.pem"
        svid.save(certificate_path, private_key_path, serialization.Encoding.PEM)

        print(f"SPIFFE ID: {svid.spiffe_id}")
        print(f"Certificate: {certificate_path}")
        print(f"Private key: {private_key_path}")
        print(f"Valid after: {svid.leaf.not_valid_before_utc}")
        print(f"Valid until: {svid.leaf.not_valid_after_utc}")


if __name__ == "__main__":
    main()
