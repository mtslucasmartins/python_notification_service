from OpenSSL import crypto

class PackageSigner:

    def __init__(self, package_dir, p12_certificate):
        self.PKCS7_DETACHED = 0x40
        with open(p12_certificate, 'rb') as f:
            self.p12_data = f.read()
        self.package_dir = package_dir
        self.p12_certificate = p12_certificate
        self.p12_passphrase = ""

    def sign(self):
        manifest_file = "{}/manifest.json".format(self.package_dir)
        signature_dest = "{}/signature".format(self.package_dir)

        p12 = crypto.load_pkcs12(self.p12_data, self.p12_passphrase)
        
        certificate = p12.get_certificate()
        private_key = p12.get_privatekey()

        with open(manifest_file, 'r') as m:
            bio_in = crypto._new_mem_buf(m.read().encode())

        pkcs7 = crypto._lib.PKCS7_sign(
            certificate._x509, 
            private_key._pkey, 
            crypto._ffi.NULL, 
            bio_in, 
            self.PKCS7_DETACHED
        )

        self.write(signature_dest, pkcs7)


    def write(self, dest, pkcs7):
        out = crypto._new_mem_buf()
        crypto._lib.i2d_PKCS7_bio(out, pkcs7)
        sigbytes = crypto._bio_to_string(out)
        with open(dest, 'wb') as s:
            s.write(sigbytes)
        

