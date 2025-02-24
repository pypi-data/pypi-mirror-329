#!/usr/bin/env python

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/bxRepos/bisos-pip/facter/py3/bin/facter-cbs-is-p-sysd.cs
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

""" #+begin_org
* Panel::  [[file:/bisos/panels/bisos-apps/lcnt/lcntScreencasting/subTitles/_nodeBase_/fullUsagePanel-en.org]]
* Overview and Relevant Pointers
facter-cbs-is-p-sysd.cs
cbs: Capability Bundle Specification  -- Based on a cba-sysd.cs seed
is: An Independent Service  --- /Service Component/
p:  Platform    -- Materialization is based on Platform-BPO (Site-BPO is not used)
#+end_org """


from bisos.capability import cba_sysd_seed
from bisos.capability import cba_seed


cba_seed.setup(
    seedType="systemd",  # Extend using cba_sysd_seed.setup
    loader=None,
    sbom="facter-sbom.cs",
    assemble="facter-assemble.cs",
    materialize=None,
)

sysdUnitsListFacter = [
    cba_sysd_seed.sysdUnit("facter", "facter-roPerf-sysd.cs")
]

cba_sysd_seed.setup(
    sysdUnitsList=sysdUnitsListFacter,
)

cba_sysd_seed.plantWithWhich("cba-sysd.cs")
