import random
import string
import sys
import tarfile
import tempfile
import os
import subprocess
import shutil

class Error (Exception): pass


class FileEncrypter:
    def __init__(self, infile, outfile, password=None):
        self.infile = os.path.abspath(infile)
        self.outfile = outfile
        self.password = password

    @staticmethod
    def _make_password(length=16):
        chars = string.ascii_letters + string.digits
        char_list = [random.choice(chars) for _ in range(length)]
        return ''.join(char_list)

    @staticmethod
    def ftp_url_from_file(filename):
        if filename.startswith('web-bfint:/'):
            server, path = filename.split(':', maxsplit=1)
            path_list = path.split(os.sep)
            if path_list[0] == '':
                path_list = path_list[1:]
            if len(path_list) >= 4 and path_list[0:3] == ['data', 'scratch', 'project']:
                return '/'.join(['ftp://ngs.sanger.ac.uk'] + path_list[1:])
        
        return None

    def _print_email(self):
        url = FileEncrypter.ftp_url_from_file(self.outfile)
        if url is None:
            return
        
        print('Email contents:')
        print('Below is the url and password you need to access the data.')
        print('password:', self.password)
        print('url:', url)
        print('To access the data on osx or linux, download the data. In the terminal, cd to the directory where you put the data and type "unzip your_file.zip".')
        print('To access the data on Windows, double-click the Zip file in File Explorer. To exract everything, click the Extract All button and enter the password.')
        

    def run(self):
        self.password = FileEncrypter._make_password() if self.password is None else self.password
        tmpdir = tempfile.mkdtemp(prefix='tmp.zipfile.', dir=os.getcwd())
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        try:
            tar = tarfile.open(self.infile, "r:gz")
            tar.extractall()
            tar.close()
        except:
            raise Error("Error extracting " + self.tarfile)
        files = os.listdir()
        if len(files) != 1:
            raise Error("expected 1 file. Got \n" + "\n".join(files))
        cmd = ' '.join([
            'zip',
            '-P', self.password,
            '-r',
            'tmp.zip',
            files[0] 
        ])
        
        try:
            subprocess.run(cmd, shell=True)
        except:
            raise Error("Error running command " + cmd)

        os.chdir(original_dir)
        zip_file = os.path.join(tmpdir, 'tmp.zip')
        assert os.path.exists(zip_file)
        cmd = 'rsync ' + zip_file + ' ' + self.outfile
        try:    
            subprocess.run(cmd, shell=True)
        except:
            raise Error("Error running rsync " + cmd)    
            

        shutil.rmtree(tmpdir)
        print('Password to decrypt is', self.password)
        self._print_email()