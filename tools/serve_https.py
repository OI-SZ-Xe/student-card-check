# -*- coding: utf-8 -*-
import datetime, http.server, ssl, os, socketserver, mimetypes
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

BASE = r"F:\请出示学生证\build\web"
CERT = os.path.join(BASE, "cert.pem")
KEY = os.path.join(BASE, "key.pem")

if not (os.path.exists(CERT) and os.path.exists(KEY)):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "192.168.10.9")])
    cert = (x509.CertificateBuilder()
        .subject_name(subject).issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(x509.SubjectAlternativeName([
            x509.IPAddress(__import__("ipaddress").ip_address("192.168.10.9")),
            x509.DNSName("localhost"),
        ]), critical=False)
        .sign(key, hashes.SHA256()))
    open(CERT, "wb").write(cert.public_bytes(serialization.Encoding.PEM))
    open(KEY, "wb").write(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()))

mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("application/octet-stream", ".pck")

os.chdir(BASE)
httpd = http.server.ThreadingHTTPServer(("0.0.0.0", 8443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
print("HTTPS on 8443", flush=True)
httpd.serve_forever()
