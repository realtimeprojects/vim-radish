

:highlight! RadishPassed ctermfg=green
:highlight! RadishFailed ctermfg=red
:sign define radish_passed linehl=RadishPassed
:sign define radish_failed linehl=RadishFailed
:sign define radish_busy linehl=Search

au BufNewFile,BufRead *.feature :com! -b -nargs=* Rrun :py vimradish.run(<args>)
au BufNewFile,BufRead *.feature :com! -b -nargs=* Rclear :py vimradish.clear()

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

function! s:initVimRadish()
  if !has('python')
    echoe 'vim-radish No python support available.'
    echoe 'Compile vim with python support to use vim-radish'
    return 0
  endif

  " Only parse the python library once
  if !exists('s:vimradish_loaded')
    python import sys

    exe 'python sys.path = ["' . s:plugin_path . '/.."] + sys.path'
    "exe 'pyfile ' . fnameescape(s:plugin_path) . '/../vim-radish.py'
    python import vimradish

    let s:vimradish_loaded = 1

  endif
  return 1
endfunction

au FileType cucumber call <SID>initVimRadish()
