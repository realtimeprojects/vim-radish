import os
import traceback
import sys
import time
import StringIO
import tempfile

import vim
from vim import current, buffers
from radish import main, radish
from radish.config import Config
from radish.hookregistry import after, before

@before.each_step
def radish_print_before_step(step):
    cmd = ":sign place %d line=%d name=radish_busy file=%s" % (step.get_line_no(), step.get_line_no(), Config().feature_files[0])
    vim.command(cmd)
    cw = vim.current.window
    cw.cursor = (int(step.get_line_no()), 0)
    vim.command(":redraw")

@after.each_step
def radish_print_after_step(step):
    if step.has_passed() == None:
        passed = "skipped"
    else:
        if step.has_passed() == True:
            passed = "passed"
        else:
            passed = "failed"

    cmd = ":sign place %d line=%d name=radish_%s file=%s" % (step.get_line_no(), step.get_line_no(), passed, Config().feature_files[0])
    vim.command(cmd)
    vim.command(":redraw")

def _radish(featurefile, basedir=None):
    if basedir == None:
        basedir = os.getcwd()
    Config().basedir = basedir
    Config().feature_files = [ featurefile ]
    Config().vim_mode = True
    Config().no_colors = True
    Config().dry_run = False
    Config().with_traceback = True
    Config().marker = time.time()
    Config().no_indentation = False
    Config().no_numbers = False
    Config().no_duration = False
    Config().with_section_names = True
    Config().no_line_jump = True
    Config().no_overwrite = True
    Config().abort_fail = True
    Config().no_skipped_steps = True

    fp = radish.FeatureParser()
    fp.parse()

    # load terrain and steps
    loader = radish.Loader(fp.get_features())
    loader.load()

    runner = radish.Runner(fp.get_features())
    endResult = runner.run()

def clear():
    """ clean radish highlights in current buffer
    """
    vim.command(":sign unplace *");

def run(basedir=None):
    """ run radish with current buffer as feature file

        @param basedir The radish base directory (will
                        be passed as -b to radish
    """
    tmpfile = tempfile.NamedTemporaryFile(prefix="radish_run_", suffix="log", delete=False)
    try:
        sys.stdout = tmpfile
        clear()
        _radish(current.buffer.name, basedir=basedir)
        vim.command(":e %s" % tmpfile.name)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        traceback.print_exc()
        vim.command(":e %s" % tmpfile.name)

vim.command(":highlight! RadishPassed ctermfg=green")
vim.command(":highlight! RadishFailed ctermbg=red ctermfg=white")
vim.command(":highlight! RadishSkipped ctermbg=grey ctermfg=black")
vim.command(":sign define radish_passed linehl=RadishPassed")
vim.command(":sign define radish_failed linehl=RadishFailed")
vim.command(":sign define radish_skipped linehl=RadishSkipped")
vim.command(":sign define radish_busy linehl=Search")
vim.command("au BufNewFile,BufRead *.feature :com! -b -nargs=* Rrun :py vimradish.run(<args>)")
vim.command("au BufNewFile,BufRead *.feature :com! -b -nargs=* Rclear :py vimradish.clear()")

