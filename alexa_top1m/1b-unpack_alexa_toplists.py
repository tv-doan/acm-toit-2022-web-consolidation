import urllib
from calendar import monthrange
import glob
import tarfile
import os

#############################
directory = './data/openintel-alexa1m/toplists/'

yyyy = '2019'
mm = '12'
#############################


def unpack_tars():
    files = glob.glob('%s/*.tar.gz' % directory)

    print(files)

    for f in files:
        with tarfile.open(f, "r:gz") as tar_ref:
            tar_ref.extractall(path='%s/' % directory)
        os.rename('%s/top-1m.csv' % (directory),
                  '%s/%s.csv' % (directory, f.split('/')[-1][6:-7]))

if __name__ == "__main__":
     unpack_tars()
