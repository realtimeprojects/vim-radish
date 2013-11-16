import os
import traceback
import sys
import time

import vim
from vim import current, buffers
from radish import main, radish
from radish.config import Config
from radish.hookregistry import after, before

@before.each_step
def radish_print_before_step(step):
    print ("before: %d" % step.get_line_no())
    cmd = ":sign place %d line=%d name=radish_busy file=%s" % (step.get_line_no(), step.get_line_no(), Config().feature_files[0])
    vim.command(cmd)

@after.each_step
def radish_print_after_step(step):
    print ("after: %d" % step.get_line_no())
    if step.has_passed() == None:
        passed = "skipped"
    else:
        if step.has_passed() == True:
            passed = "passed"
        else:
            passed = "failed"

    cmd = ":sign place %d line=%d name=radish_%s file=%s" % (step.get_line_no(), step.get_line_no(), passed, Config().feature_files[0])
    vim.command(cmd)

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

def main(basedir=None):
    try:
        for i in range(0, 20):
            print("Hello World")

        _radish(current.buffer.name, basedir=basedir)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        traceback.print_exc()

vim.command(":highlight! RadishPassed ctermfg=green")
vim.command(":highlight! RadishFailed ctermfg=red")
vim.command(":sign define radish_passed linehl=RadishPassed")
vim.command(":sign define radish_failed linehl=RadishFailed")
vim.command(":sign define radish_busy linehl=Search")

