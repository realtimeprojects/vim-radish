import os
import traceback
import sys
import time

import vim
from vim import current, buffers
from radish import main, radish
from radish.config import Config

def _radish(featurefile, basedir=None):
    if basedir == None:
        basedir = os.getcwd()
    Config().basedir = basedir
    Config().feature_files = [ featurefile ]
    Config().vim_mode = True
    Config().no_colors = True
    Config().dry_run = True
    Config().with_traceback = True
    Config().marker = time.time()

    fp = radish.FeatureParser()
    fp.parse()

    # load terrain and steps
    loader = radish.Loader(fp.get_features())
    loader.load()

    runner = radish.Runner(fp.get_features())
    endResult = runner.run()

def main():
    try:
        print("current:%s" % dir(current.buffer))
        print("name:%s" % current.buffer.name)
        _radish(current.buffer.name, "../testfiles")
    except:
        print "Unexpected error:", sys.exc_info()[0]
        traceback.print_exc()

