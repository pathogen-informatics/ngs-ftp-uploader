import unittest
import os
import filecmp
import zipfile
import shutil
from ngs_ftp_uploader import file_encrypter


modules_dir = os.path.dirname(os.path.abspath(file_encrypter.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')



    
    

class TestFileEncrypter(unittest.TestCase):
    def test_make_password(self):
        '''test _make_password'''
        got = file_encrypter.FileEncrypter._make_password()
        self.assertEqual(str, type(got))
        self.assertEqual(16, len(got)) 
        got = file_encrypter.FileEncrypter._make_password(17)
        self.assertEqual(str, type(got))
        self.assertEqual(17, len(got)) 
        
    def test_ftp_url_from_file(self):
        '''test ftp_url_from_file'''
        tests = [
            ('web-foo:/foo/bar', None),
            ('web-bfint:/foo/bar', None),
            ('web-bfint:/data/foo.zip', None),
            ('web-bfint:/data/scratch/foo.zip', None),
            ('web-bfint:/data/scratch/project/foo.zip', 'ftp://ngs.sanger.ac.uk/scratch/project/foo.zip'),
            #('web-bfint:/data/scratch/project/dir/foo.zip', 'ftp://ngs.sanger.ac.uk/scratch/project/dir/foo.zip'),
            #('web-bfint:/data/scratch/project/dir/f:oo.zip', 'ftp://ngs.sanger.ac.uk/scratch/project/dir/f:oo.zip')
        ]
        
        for filename, expected in tests:
            self.assertEqual(file_encrypter.FileEncrypter.ftp_url_from_file(filename), expected)
        

    def test_run(self):
        tarball = os.path.join(data_dir, "file_encrypter_run.tar.gz")
        expected_dir = os.path.join(data_dir, "file_encrypter_run")
        zip_file = "tmp.zip"
        
        
        def check_zip_ok(expected_dir, zip_file, password):
            tmpdir = "tmp.checkzip"
            os.mkdir(tmpdir)
            with zipfile.ZipFile(zip_file, 'r') as myzip:
                myzip.extractall(path=tmpdir, pwd=bytes(password, 'utf-8'))
            files = ['file_1.txt', 'file_2.txt', os.path.join('A', 'file3.txt')]
            for filename in files:
                expected = os.path.join(expected_dir, filename)
                got = os.path.join(tmpdir, 'file_encrypter_run', filename)
                self.assertTrue(filecmp.cmp(expected, got, shallow=False))
            shutil.rmtree(tmpdir)
        encrypter = file_encrypter.FileEncrypter(tarball, zip_file)
        encrypter.run()
        check_zip_ok(expected_dir, zip_file, encrypter.password)
        os.unlink(zip_file)
        encrypter = file_encrypter.FileEncrypter(tarball, zip_file, password='abc')
        encrypter.run()
        check_zip_ok(expected_dir, zip_file, 'abc')
        os.unlink(zip_file)



