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
    cw.cursor = (step.get_line_no(), 0)
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
            vim.command(":echo \"radish step failed: %s\"" % step._fail_reason.get_reason())

    cmd = ":sign place %d line=%d name=radish_%s file=%s" % (step.get_line_no(), step.get_line_no(), passed, Config().feature_files[0])
    vim.command(cmd)
    vim.command(":redraw")

log_file = None

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
    Config().profile = ""

    fp = radish.FeatureParser()
    fp.parse()

    # load terrain and steps
    loader = radish.Loader(fp.get_features())
    loader.load()

    runner = radish.Runner(fp.get_features())
    endResult = runner.run()

    if endResult.have_all_passed():
      vim.command(":echo \"radish run was successful ;-)\"")

def openlog():
    global log_file
    if log_file:
        vim.command(":e %s" % log_file.name)

def clear():
    """ clean radish highlights in current buffer
    """
    vim.command(":sign unplace *");

def run(basedir=None):
    """ run radish with current buffer as feature file

        @param basedir The radish base directory (will
                        be passed as -b to radish
    """
    global log_file
    log_file = tempfile.NamedTemporaryFile(prefix="radish_run_", suffix="log", delete=False)
    try:
        sys.stdout = log_file
        clear()
        _radish(current.buffer.name, basedir=basedir)
    except radish.exceptions.RadishError as e:
        vim.command(":echo \"radish: %s\"" % e)
        if hasattr(e, "fileline"):
            filename, line_no = e.fileline()
            cmd = ":sign place %d line=%d name=radish_failed file=%s" % (line_no, line_no, filename)
            vim.command(cmd)
            cw = vim.current.window
            cw.cursor = (line_no, 0)
            vim.command(":redraw")

    log_file.close()

