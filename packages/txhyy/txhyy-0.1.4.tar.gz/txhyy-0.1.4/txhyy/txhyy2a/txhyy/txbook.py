import argparse
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime

def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

def generate_certificate(private_key, domain):
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Shanghai"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Shanghai"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
        x509.NameAttribute(NameOID.COMMON_NAME, domain),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(domain)]),
            critical=False,
        )
        .sign(private_key, hashes.SHA256(), default_backend())
    )
    return cert

def generate_additional_config(domain):
    config_content = f"""
[General]
domain = {domain}
cert_file = certificate.pem
key_file = private_key.pem
    """
    return config_content

def add_extra_info_to_config(config_path):
    extra_info = """
[Extra]
info = This is some extra information added to the config file.
    """
    with open(config_path, 'a') as f:
        f.write(extra_info)

def main():
    parser = argparse.ArgumentParser(description='Generate self-signed HTTPS certificate and additional files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for the generated files')
    parser.add_argument('-i', '--key_type', choices=['private', 'public'], required=True, help='Generate private or public key')
    parser.add_argument('-p', '--domain', required=True, help='Domain name or port number')
    args = parser.parse_args()

    target_dir = os.path.join(args.output, "txhyy.config")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    private_key = generate_private_key()
    cert = generate_certificate(private_key, args.domain)
    additional_config = generate_additional_config(args.domain)

    if args.key_type == 'private':
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_path = os.path.join(target_dir, "private_key.pem")
        with open(private_key_path, "wb") as f:
            f.write(private_pem)
        print(f"Private key saved to {private_key_path}")
    else:
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        cert_path = os.path.join(target_dir, "certificate.pem")
        with open(cert_path, "wb") as f:
            f.write(cert_pem)
        print(f"Certificate saved to {cert_path}")

    config_path = os.path.join(target_dir, "additional_config.ini")
    with open(config_path, "w") as f:
        f.write(additional_config)
    print(f"Additional config file saved to {config_path}")


    add_extra_info_to_config(config_path)
    print(f"Extra information added to {config_path}")

if __name__ == "__main__":
    main()