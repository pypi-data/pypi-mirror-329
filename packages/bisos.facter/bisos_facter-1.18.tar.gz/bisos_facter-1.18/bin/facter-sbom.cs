#!/usr/bin/env python

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/auth/bxRepos/bisos-pip/facter/py3/bin/facter-sbom.cs
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

from bisos.sbom import pkgsSeed
ap = pkgsSeed.aptPkg

aptPkgsList = [
    ap("facter"),
]

pkgsSeed.setup(
    aptPkgsList=aptPkgsList,
)
