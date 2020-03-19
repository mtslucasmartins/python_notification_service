import os
import hashlib
import shutil
import tempfile
import zipfile

class PushPackageUtilities:

    @staticmethod
    def checksum(filename):
        _hash = hashlib.sha512()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                _hash.update(chunk)
        return _hash.hexdigest()

    @staticmethod
    def create_temporary_directory(dir, name=None):
        return tempfile.TemporaryDirectory(name, dir = dir)

    @staticmethod
    def copy_file(src, dest):
        shutil.copyfile(src, dest)

    @staticmethod
    def copytree(src, dst, symlinks=False, ignore=None):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d, symlinks, ignore)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    shutil.copy2(s, d)

    @staticmethod
    def zip(src, dest):
        zipf = zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(src):
            for file in files:
                zipf.write(
                    os.path.join(root, file), 
                    os.path.relpath(os.path.join(root, file), os.path.join(src)) # , '..'
                )
        zipf.close()
