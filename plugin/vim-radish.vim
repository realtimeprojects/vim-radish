
:highlight! RadishBusy ctermbg=darkblue
:highlight! RadishPassed ctermbg=darkgreen
:highlight! RadishFailed ctermbg=darkred
:highlight! RadishSkipped ctermbg=darkgrey
:sign define radish_passed linehl=Normal
:sign define radish_failed linehl=RadishFailed
:sign define radish_skipped linehl=RadishSkipped
:sign define radish_busy linehl=RadishBusy
au BufNewFile,BufRead *.feature :com! -b -nargs=* Rrun :py vimradish.run(<args>)
au BufNewFile,BufRead *.feature :com! -b -nargs=* Rclear :py vimradish.clear()
au BufNewFile,BufRead *.feature :com! -b -nargs=* Rlog :py vimradish.openlog()

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

    if exists('s:radish_basepath')
      exe 'python sys.path = ["' . s:radish_basepath . '"] + sys.path'
    endif

    python import vimradish

    let s:vimradish_loaded = 1
  endif
  return 1
endfunction

au FileType cucumber call <SID>initVimRadish()
