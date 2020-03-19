import os 
import json
import tempfile

from apple_notifications.push_package.signer import PackageSigner
from apple_notifications.push_package.utilities import PushPackageUtilities

from definitions import STATIC_PATH

class PushPackage:

    def __init__(self, website_push_id):
        self.website_push_id = website_push_id
        self.website_push_dir = "{}/apple_notifications/{}".format(STATIC_PATH, website_push_id)

        self.certificate = "{}/certificates/cert.p12".format(self.website_push_dir)
        self.package_raw = "{}/push_package".format(self.website_push_dir)

        self.raw_files = [
            "icon.iconset/icon_16x16.png",
            "icon.iconset/icon_16x16@2x.png",
            "icon.iconset/icon_32x32.png",
            "icon.iconset/icon_32x32@2x.png",
            "icon.iconset/icon_128x128.png",
            "icon.iconset/icon_128x128@2x.png",
            "website.json"
        ]

    # Metodo responsavel pela copia dos icons para o zip.
    def create_iconset(self, package_dir):
        PushPackageUtilities.copytree("{}/icon.iconset".format(self.package_raw), 
                                      "{}/icon.iconset".format(package_dir))

    # metodo responsavel pela criacao do arquivo website.json com o token do usuario.
    def create_website_info(self, authentication_token, package_dir):
        with open("{}/website.json".format(self.package_raw), 'r') as website_raw:
            website_info = json.loads(website_raw.read())
            website_info['authenticationToken'] = authentication_token
            with open("{}/website.json".format(package_dir), 'w') as website:
                website.write(json.dumps(website_info, indent=4))

    # Metodo responsavel pela criacao do arquivo manifest.json, com as checksums 
    # dos arquivos do pacote.
    def create_manifest(self, package_dir):
        manifest_data = {}
        for raw_file in self.raw_files:            
            file_contents = "{}/{}".format(package_dir, raw_file)
            manifest_data[raw_file] = {
                'hashType': 'sha512',
                'hashValue': PushPackageUtilities.checksum(file_contents)
            }
        with open("{}/{}".format(package_dir, 'manifest.json'), 'w') as f:
            f.write(json.dumps(manifest_data, indent=4))

    # Metodo responsavel por assinar o manifest.json com o certificado.
    def create_signature(self, package_dir):
        PackageSigner(package_dir, self.certificate).sign()

    # Metodo responsavel pela criacao de um zip temporario e exclusao do original,
    # para nao guardar arquivos no servidor
    def create_temporary_zip(self, zip_file):
        temporary_zip = tempfile.NamedTemporaryFile(dir = os.path.dirname(zip_file), suffix = '.zip', delete=True)
        PushPackageUtilities.copy_file(zip_file, temporary_zip.name) # cria a copia temporaria do zip
        os.remove(zip_file) # remove o arquivo apos criar a copia temporaria 
        return temporary_zip 

    def create_push_package(self, authentication_token):
        # creates temporary directory
        package = PushPackageUtilities.create_temporary_directory(self.package_raw)
        package_dir = package.name
        package_name = os.path.basename(package.name)

        # creating website file 
        self.create_website_info(authentication_token, package_dir)

        # creating icon set
        self.create_iconset(package_dir)

        # creating manifest.json
        self.create_manifest(package_dir)
        
        # creating signature
        self.create_signature(package_dir)

        dst =  '{}.zip'.format(package_name) # self.push_package_dir() + '/pushPackage.zip'

        # temporary_zip = tempfile.NamedTemporaryFile(dir = package_dir, suffix = '.zip', delete=False)
        # temporary_zip_file = temporary_zip.name

        PushPackageUtilities.zip(package_dir, dst)

        return dst

        # PushPackageUtilities.copy_file(temporary_zip_file, dst)

        # temporary_zip.close()

