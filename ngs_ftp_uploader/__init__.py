from pkg_resources import get_distribution

try:
    __version__ = get_distribution('ngs_ftp_uploader').version
except:
    __version__ = 'local'


__all__ = [
    'file_encrypter',
]
from ngs_ftp_uploader import *
