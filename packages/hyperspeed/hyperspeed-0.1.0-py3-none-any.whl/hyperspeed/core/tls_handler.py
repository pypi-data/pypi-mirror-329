import ssl
import datetime
from OpenSSL import SSL
from cryptography.hazmat.primitives import serialization
from cryptography import *
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from typing import Optional, Tuple
import tempfile
import os

class TLSHandler:
    def __init__(self, config: dict):
        self.config = config
        self.session_cache = {}
        self._init_certificates()

    def _init_certificates(self):
        """生成自签名根证书（生产环境应使用正式证书）"""
        # 生成私钥
        self.key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # 创建自签名证书
        subject = issuer = x509.Name([
            x509.NameAttribute(x509.NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "hyperspeed"),
            x509.NameAttribute(x509.NameOID.COMMON_NAME, "hyperspeed Root CA"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        ).sign(self.key, hashes.SHA256(), default_backend())

        # 存储为PEM格式
        self.cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
        self.key_pem = self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    def create_tls_context(self) -> ssl.SSLContext:
        """创建服务端SSL上下文"""
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.options |= ssl