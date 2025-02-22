#!/usr/bin/env python

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/bxRepos/bisos-pip/sbom/py3/bin/exmpl-binsPerp.cs
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

""" #+begin_org
* Panel::  [[file:/bisos/panels/bisos-apps/lcnt/lcntScreencasting/subTitles/_nodeBase_/fullUsagePanel-en.org]]
* Overview and Relevant Pointers
#+end_org """


from bisos.sbom import pkgsSeed
ap = pkgsSeed.aptPkg
pp = pkgsSeed.pipPkg

aptPkgsList = [
    ap("djbdns"),
    ap("facter"),
    # ap("", instFn=someFunc),
]

pipPkgsList = [
    pp("bisos.marmee"),
]

pipxPkgsList = [
    pp("bisos.marmee"),
]

# print(aptPkgsList)

pkgsSeed.setup(
    aptPkgsList=aptPkgsList,
    pipPkgsList=pipPkgsList,
    pipxPkgsList=pipxPkgsList,
    # examplesHook=qmail_sbom.examples_csu,
)


# pkgsSeed.plant()

# __file__ = pkgsSeed.plantFile()
# with open(__file__) as f: exec(compile(f.read(), __file__, 'exec'))
