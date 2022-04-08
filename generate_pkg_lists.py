#!/usr/bin/env python
## { alterEGO Linux: "Open the vault of knowledge" } ----------------------- ##
##                                                                           ##
## alterEGOlinux/installer/generate_pkg_lists.py                             ##
##   created        : 2022-04-08 00:29:47 UTC                                ##
##   updated        : 2022-04-08 00:29:55 UTC                                ##
##   description    : Generates package lists from installer.py              ##
## _________________________________________________________________________ ##

import installer

official = []
aur = []
for pkg in installer.packages:
    if pkg.repository == 'official':
        official.append(pkg.name)
    else:
        aur.append(pkg.name)

with open('official_pkgs.txt', 'w') as out:
    out.write(' '.join(official))

with open('aur_pkgs.txt', 'w') as out:
    out.write(' '.join(aur))
