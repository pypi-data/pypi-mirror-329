# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os

import pwem
from pyworkflow import Config
from pyworkflow.utils import Environ

from .constants import *

__version__ = '3.2.2'
_logo = "salk_logo.jpg"
_references = ['tan2017']


class Plugin(pwem.Plugin):
    _homeVar = FSC3D_HOME
    _pathVars = [FSC3D_HOME]
    _supportedVersions = [V3_0]
    _url = "https://github.com/scipion-em/scipion-em-fsc3d"

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(FSC3D_HOME, 'fsc3D-3.0')
        cls._defineVar(FSC3D_ENV_ACTIVATION, DEFAULT_ACTIVATION_CMD)

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch 3DFSC. """
        environ = Environ(os.environ)
        if 'PYTHONPATH' in environ:
            # this is required for python virtual env to work
            del environ['PYTHONPATH']
        environ.update({'PATH': cls.getHome('ThreeDFSC')},
                       position=Environ.BEGIN)

        return environ

    @classmethod
    def getFSCEnvActivation(cls):
        activation = cls.getVar(FSC3D_ENV_ACTIVATION)
        scipionHome = Config.SCIPION_HOME + os.path.sep

        return activation.replace(scipionHome, "", 1)

    @classmethod
    def getActivationCmd(cls):
        """ Return the activation command. """
        return '%s %s' % (cls.getCondaActivationCmd(),
                          cls.getFSCEnvActivation())

    @classmethod
    def getDependencies(cls):
        """ Return a list of dependencies. Include conda if
        activation command was not found. """
        condaActivationCmd = cls.getCondaActivationCmd()
        neededProgs = []
        if not condaActivationCmd:
            neededProgs.append('conda')

        return neededProgs

    @classmethod
    def runProgram(cls, protocol, args, cwd=None):
        """ Return the program binary that will be used. """
        cmd = f'{cls.getActivationCmd()} && '
        cmd += cls.getHome('ThreeDFSC', 'ThreeDFSC_Start.py')
        protocol.runJob(cmd, args, env=cls.getEnviron(), cwd=cwd)

    @classmethod
    def defineBinaries(cls, env):
        for ver in cls._supportedVersions:
            ENV = f"fsc3D-{ver}"
            installCmds = [
                cls.getCondaActivationCmd(),
                f'cd ../ && rmdir {ENV} && '
                f'conda create -y -n {ENV} "python<3.12" cudatoolkit=11.8 && '
                f'conda activate {ENV} && ',
                'pip install numpy numba==0.58.0 scipy click h5py scikit-image matplotlib mrcfile && ',
                f'git clone https://github.com/azazellochg/fsc3D {ENV}'
            ]
            fsc_commands = [(" ".join(installCmds), 'ThreeDFSC/ThreeDFSC_Start.py')]
            env.addPackage('fsc3D', version=ver,
                           tar='void.tgz',
                           commands=fsc_commands,
                           neededProgs=cls.getDependencies(),
                           default=ver == V3_0)
