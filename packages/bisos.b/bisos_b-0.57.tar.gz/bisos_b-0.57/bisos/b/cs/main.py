# -*- coding: utf-8 -*-

""" #+begin_org
* *[Summary]* :: A =PyLib= for dispatching CS Main.
#+end_org """

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of Blee ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Libre-Halaal Foundation. Subject to AGPL.
** It is not part of Emacs. It is part of Blee.
** Best read and edited  with Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: NOTYET
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:python:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['main'], }
csInfo['version'] = '202209033323'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'main-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* /[[elisp:(org-cycle)][| Description |]]/ :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/PyFwrk/bisos.crypt/_nodeBase_/fullUsagePanel-en.org][PyFwrk bisos.crypt Panel]]
Module description comes here.
** Relevant Panels:
** Status: In use with blee3
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO complete fileName in particulars.
#+end_org """

####+BEGIN: b:prog:file/orgTopControls :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Controls |]] :: [[elisp:(delete-other-windows)][(1)]] | [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
#+end_org """
####+END:

####+BEGIN: b:python:file/workbench :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Workbench |]] :: [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: bx:cs:python:icmItem :itemType "=PyImports= " :itemTitle "*Py Library IMPORTS*"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =PyImports=  [[elisp:(outline-show-subtree+toggle)][||]] *Py Library IMPORTS*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:


import __main__

import types

import sys

from bisos.b import b_io
from bisos.b import cs
from bisos import b

####+BEGIN: b:py3:cs:func/typing :funcName "G_main" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /G_main/   [[elisp:(org-cycle)][| ]]
#+end_org """
def G_main(
####+END:
):
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] Replaces ICM dispatcher for other command line args parsings.
    #+end_org """
    pass

####+BEGIN: b:py3:cs:func/typing :funcName "classedCmndsDict" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /classedCmndsDict/   [[elisp:(org-cycle)][| ]]
#+end_org """
def classedCmndsDict(
####+END:
        importedCmndsModules,
) -> dict:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] Should be done here, can not be done in icm library because of the evals.
    =importedCmndsModules= is a list of modules.
    Returns a dictionary of ???
    #+end_org """

    from bisos.b.cs import inCmnd

    import importlib
    importedCmndsFilesList=[]
    importedTagsList=[]
    for moduleName in importedCmndsModules:
        #print(f"moduleName={moduleName}")
        moduleNameList = moduleName.split(".")
        importTag = moduleNameList.pop()
        importModule = ".".join(moduleNameList)
        #print(f"importTag= {importTag} -- moduleNameList={moduleNameList} -- importModule={importModule}")
        _tmp = importlib.import_module(importModule)
        exec(f"{importTag} = _tmp.{importTag}") # assignment is a statement
        #eval(f"print({importTag}.__file__)") # DEBUG
        eval(f"importedCmndsFilesList.append({importTag}.__file__)") # expression
        importedTagsList.append(importTag)

    for moduleName in ["bisos.b.cs.inCmnd", "bisos.b.cs.examples", "bisos.b.cs.rpyc", "bisos.b.cs.ro"]:
        #print(f"moduleName={moduleName}")
        moduleNameList = moduleName.split(".")
        importTag = moduleNameList.pop()
        importModule = ".".join(moduleNameList)
        #print(f"importTag= {importTag} -- moduleNameList={moduleNameList} -- importModule={importModule}")
        _tmp = importlib.import_module(importModule)
        exec(f"{importTag} = _tmp.{importTag}") # assignment is a statement
        #eval(f"print({importTag}.__file__)") # DEBUG
        eval(f"importedCmndsFilesList.append({importTag}.__file__)") # expression
        importedTagsList.append(importTag)


    #print(importedCmndsFilesList)
    #print(importedTagsList)

    rtInv = cs.RtInvoker.new_cmnd()
    outcome = b.op.Outcome()

    callDict = dict()
    for eachCmnd in inCmnd.cmndList_mainsMethods().cmnd(
            rtInv=rtInv,
            cmndOutcome=outcome,
            importedCmnds={}, # __main__.g_importedCmnds -- Being obsoleted
            mainFileName=__main__.__file__,
            importedCmndsFilesList=importedCmndsFilesList,
    ):
        #print(f"eachCmnd={eachCmnd}")
        try:
            callDict[eachCmnd] = eval("__main__.{}".format(eachCmnd))
        except AttributeError:
            #print(f"AttributeError -- __main__.{eachCmnd} -- ignored")
            pass
        except NameError:
            #print(f"NameError -- __main__.{eachCmnd} -- ignored")
            pass
        else:
            #print(f"Added __main__.{eachCmnd}")
            continue

        for importTag in importedTagsList:
            #print(f"trying {importTag}")
            try:
                #print(f"Evaling -- {importTag}.{eachCmnd}")
                eval(f"{importTag}.{eachCmnd}")
            except AttributeError:
                #print(f"AttributeError -- {importTag}.{eachCmnd}")
                continue
            try:
                callDict[eachCmnd] = eval(f"{importTag}.{eachCmnd}")
                #print(f"callDict -- {importTag}.{eachCmnd}")
                break
            except NameError:
                pass


    return callDict


# G = cs.globalContext.get()

# csInfo = G.csInfo()

# try:
#    __main__.csInfo
# except AttributeError:
#     pass
# else:
#     csInfo.update(__main__.csInfo)

#     csInfo['icmName'] = __main__.__icmName__
#     csInfo['version'] = __main__.__version__
#     csInfo['status'] = __main__.__status__
#     csInfo['credits'] = __main__.__credits__

#     G.csInfoSet(csInfo)
#

# g_examples = __main__.examples  # or None
# g_mainEntry = None  # or G_main
#

####+BEGIN: bx:cs:py3:func :funcName "g_csMain" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /g_csMain/  [[elisp:(org-cycle)][| ]]
#+end_org """
def g_csMain(
####+END:
        noCmndEntry=None,   # To Be Obsoleted
        extraParamsHook=None,
        importedCmndsModules=[],
        csPreCmndsHook=None,
        csPostCmndsHook=None,
        csInfo=None,
):
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] This ICM's specific information is passed to G_mainWithClass
    #+end_org """

    G = cs.globalContext.get()
    G.csInfoSet(csInfo)

    examples = None
    mainEntry = None

    if noCmndEntry:
        if type(noCmndEntry) is types.FunctionType:
            mainEntry = noCmndEntry
            # examples is None
        else:  # We then assume it is a Cmnd
            examples = noCmndEntry
            mainEntry = noCmndEntry

    sys.exit(
        cs.G_mainWithClass(
            inArgv=sys.argv[1:],                 # Mandatory
            #extraArgs=__main__.g_argsExtraSpecify,        # Mandatory
            extraArgs=extraParamsHook,
            G_examples=examples,               # Mandatory
            classedCmndsDict=classedCmndsDict(importedCmndsModules),   # Mandatory
            mainEntry=mainEntry,
            g_icmPreCmnds=csPreCmndsHook,
            g_icmPostCmnds=csPostCmndsHook,
        )
    )




#from bisos.cs import inCmnd


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :title " ~End Of Editable Text~ "
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _ ~End Of Editable Text~ _: |]]    [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:


####+BEGIN: b:prog:file/endOfFile :extraParams nil
""" #+begin_org
* *[[elisp:(org-cycle)][| END-OF-FILE |]]* :: emacs and org variables and control parameters
#+end_org """
### local variables:
### no-byte-compile: t
### end:
####+END:
