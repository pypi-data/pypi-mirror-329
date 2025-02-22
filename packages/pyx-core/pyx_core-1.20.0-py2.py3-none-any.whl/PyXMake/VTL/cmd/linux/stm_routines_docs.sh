#!/bin/sh
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                    	     Shell script for Docker/Linux (x64)                                 %     
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Bash script for creating legacy STM-Routines documentation
# Created on 13.06.2021
# 
# Version: 1.0
# -------------------------------------------------------------------------------------------------
#    Requirements and dependencies:
#        - 
#
#     Changelog:
#        - 
#
# -------------------------------------------------------------------------------------------------
rm -f ~/.gitconfig
git config --global http.sslverify false
git config --global core.ignorecase false
git config --global credential.helper store
git config --global user.name "${GIT_USER}" && git config --global user.password "${GIT_PASSWORD}"
git config --global url."https://${GIT_USER}:${GIT_PASSWORD}@gitlab.dlr.de/".insteadOf "https://gitlab.dlr.de/"
cd src && /opt/conda/envs/stmlab/bin/python -c "import PyCODAC" && cd ..
export PATH=/opt/conda/bin:$PATH
conda env create -n stmdocs -f src/PyCODAC/Plugin/PyXMake/Build/config/stm_docu.yml
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
# Backwards compatibility. 
export GIT_PASSWORD=${GIT_CREDENTIALS:-$GIT_PASSWORD}
cd src/PyCODAC/VTL/scratch
svn --trust-server-cert --non-interactive --username $GIT_USER --password $GIT_PASSWORD co --force --ignore-externals --quiet https://svn.dlr.de/STM-Routines/
cp STM-Routines/Analysis_Tools/BEOS/trunk/doc/buildDocumentation.py STM-Routines/Analysis_Tools/BEOS/trunk/src/buildDocumentation.py
cp STM-Routines/Analysis_Tools/BoxBeam/trunk/doc/buildDocumentation.py STM-Routines/Analysis_Tools/BoxBeam/trunk/src/buildDocumentation.py
cd STM-Routines/0_MainDoc/trunk/src
conda run -n stmdocs python buildDocumentation.py -CBH && cd ..
cp doc/_build/html/documentation.html doc/_build/html/index.html