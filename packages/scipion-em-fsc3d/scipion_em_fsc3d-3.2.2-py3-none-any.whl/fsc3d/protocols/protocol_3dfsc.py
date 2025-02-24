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
from enum import Enum

import pyworkflow.protocol.params as params
from pyworkflow.constants import PROD
from pyworkflow.utils import cleanPath
from pwem.protocols import ProtAnalysis3D
from pwem.emlib.image import ImageHandler
from pwem.objects import Volume

from .. import Plugin


class outputs(Enum):
    outputVolume = Volume


class Prot3DFSC(ProtAnalysis3D):
    """ Protocol to calculate 3D FSC.

    3D FSC is software tool for quantifying directional
    resolution using 3D Fourier shell correlation volumes.
     
    Find more information at https://github.com/nysbc/Anisotropy
    """
    _label = 'estimate resolution'
    _devStatus = PROD
    _possibleOutputs = outputs

    INPUT_HELP = """ Required input volumes for 3D FSC:
        1. First half map of 3D reconstruction. Can be masked or unmasked.
        2. Second half map of 3D reconstruction. Can be masked or unmasked.
        3. Full map of 3D reconstruction. Can be masked or unmasked, sharpened or unsharpened.
    """
    
    def __init__(self, **kwargs):
        ProtAnalysis3D.__init__(self, **kwargs)

    def _initialize(self):
        """ This function is mean to be called after the
        working dir for the protocol have been set. (maybe after recovery from mapper)
        """
        self._createFilenameTemplates()

    def _createFilenameTemplates(self):
        """ Centralize how files are called for iterations and references. """
        myDict = {
                  'input_volFn': self._getTmpPath('volume_full.mrc'),
                  'input_half1Fn': self._getTmpPath('volume_half1.mrc'),
                  'input_half2Fn': self._getTmpPath('volume_half2.mrc'),
                  'input_maskFn': self._getTmpPath('mask.mrc'),
                  'out_histogram': self._getExtraPath('Results_vol/histogram.png'),
                  'out_plot3DFSC': self._getExtraPath('Results_vol/Plotsvol.jpg'),
                  'out_plotFT': self._getExtraPath('Results_vol/FTPlotvol.jpg'),
                  'out_vol3DFSC': self._getExtraPath('Results_vol/vol.mrc'),
                  'out_vol3DFSC-th': self._getExtraPath('Results_vol/vol_Thresholded.mrc'),
                  'out_vol3DFSC-thbin': self._getExtraPath('Results_vol/vol_ThresholdedBinarized.mrc'),
                  'out_cmdChimera': self._getExtraPath('Results_vol/Chimera/3DFSCPlot_Chimera.cmd'),
                  'out_globalFSC': self._getExtraPath('Results_vol/ResEMvolOutglobalFSC.csv')
                  }

        self._updateFilenamesDict(myDict)

    # --------------------------- DEFINE param functions ----------------------

    def _defineParams(self, form):
        form.addHidden(params.USE_GPU, params.BooleanParam,
                       default=True,
                       label="Use GPU?")
        form.addHidden(params.GPU_LIST, params.StringParam,
                       default='0',
                       label="Choose GPU ID",
                       help="Each GPU has a unique ID. If you have only "
                            "one GPU, set ID to 0. 3DFSC can use only one GPU.")

        form.addSection(label='Input')
        form.addParam('inputVolume', params.PointerParam,
                      pointerClass='Volume',
                      label="Input volume", important=True,
                      help=self.INPUT_HELP)
        form.addParam('provideHalfMaps', params.BooleanParam,
                      default=False,
                      label="Provide half-maps separately?")
        form.addParam('volumeHalf1', params.PointerParam,
                      label="Volume half 1", important=True,
                      condition="provideHalfMaps",
                      pointerClass='Volume',
                      help=self.INPUT_HELP)
        form.addParam('volumeHalf2', params.PointerParam,
                      pointerClass='Volume',
                      condition="provideHalfMaps",
                      label="Volume half 2", important=True,
                      help=self.INPUT_HELP)

        form.addParam('applyMask', params.BooleanParam, default=False,
                      label="Mask input volume?",
                      help='If given, it would be used to mask the half maps '
                           'during 3DFSC generation and analysis.')
        form.addParam('maskVolume', params.PointerParam, label="Mask volume",
                      pointerClass='VolumeMask', condition="applyMask",
                      help='Select a volume to apply as a mask.')

        form.addSection(label='Extra params')
        form.addParam('dTheta', params.FloatParam, default=20,
                      label='Angle of cone (deg)',
                      help='Angle of cone to be used for 3D FSC sampling in '
                           'degrees. Default is 20 degrees.')
        form.addParam('fscCutoff', params.FloatParam, default=0.143,
                      label='FSC cutoff',
                      help='FSC cutoff criterion. 0.143 is default.')
        form.addParam('thrSph', params.FloatParam, default=0.5,
                      label='Sphericity threshold',
                      help='Threshold value for 3DFSC volume for calculating '
                           'sphericity. 0.5 is default.')
        form.addParam('hpFilter', params.FloatParam, default=200,
                      label='High-pass filter (A)',
                      help='High-pass filter for thresholding in Angstrom. '
                           'Prevents small dips in directional FSCs at low '
                           'spatial frequency due to noise from messing up '
                           'the thresholding step. Decrease if you see a '
                           'huge wedge missing from your thresholded 3DFSC '
                           'volume. 200 Angstroms is default.')
        form.addParam('numThr', params.IntParam, default=0,
                      label='Number of threshold for sphericity',
                      help='Calculate sphericities at different threshold '
                           'cutoffs to determine sphericity deviation across '
                           'spatial frequencies. This can be useful to '
                           'evaluate possible effects of overfitting or '
                           'improperly assigned orientations. 0 is default.')

    # --------------------------- INSERT steps functions ----------------------
    
    def _insertAllSteps(self):
        # Insert processing steps
        self._initialize()
        self._insertFunctionStep('convertInputStep')
        self._insertFunctionStep('run3DFSCStep')
        self._insertFunctionStep('createOutputStep')

    # --------------------------- STEPS functions -----------------------------
    
    def convertInputStep(self):
        """ Convert input volumes to .mrc as expected by 3DFSC."""
        ih = ImageHandler()
        if self.provideHalfMaps:
            fnHalf1 = self.volumeHalf1.get().getLocation()
            fnHalf2 = self.volumeHalf2.get().getLocation()
        else:
            fnHalf1, fnHalf2 = self.inputVolume.get().getHalfMaps().split(',')

        ih.convert(fnHalf1,
                   self._getFileName('input_half1Fn'))
        ih.convert(fnHalf2,
                   self._getFileName('input_half2Fn'))
        ih.convert(self.inputVolume.get().getLocation(),
                   self._getFileName('input_volFn'))
        if self.maskVolume.hasValue():
            ih.convert(self.maskVolume.get().getLocation(),
                       self._getFileName('input_maskFn'))

    def run3DFSCStep(self):
        args = self._getArgs()
        params = ' '.join(['%s=%s' % (k, str(v)) for k, v in args.items()])

        if self.useGpu:
            params += ' --gpu --gpu_id=%s' % self.gpuList.get()

        Plugin.runProgram(self, params, cwd=self._getExtraPath())
        if not os.path.exists(self._getFileName('out_vol3DFSC')):
            raise RuntimeError('3D FSC run failed!')

    def createOutputStep(self):
        if os.path.exists(self._getFileName('out_vol3DFSC')):
            inputVol = self.inputVolume.get()
            vol = Volume()
            vol.setObjLabel('3D FSC')
            vol.setFileName(self._getFileName('out_vol3DFSC'))
            vol.setSamplingRate(inputVol.getSamplingRate())

            # remove useless output
            cleanPath(self._getExtraPath('Results_vol/ResEMvolOut.mrc'))

            self._defineOutputs(**{outputs.outputVolume.name: vol})
            self._defineSourceRelation(self.inputVolume, vol)

    # --------------------------- INFO functions ------------------------------
    
    def _summary(self):
        summary = []
        if self.getOutputsSize() > 0:
            logFn = self.getLogPaths()[0]
            sph = self.findSphericity(logFn)
            summary.append(f'Sphericity: {sph:0.3f}')
        else:
            summary.append("Output is not ready yet.")

        return summary
    
    def _validate(self):
        errors = []

        if not self.provideHalfMaps and not self.inputVolume.get().hasHalfMaps():
            errors.append("Input volume has no associated half-maps.")
                
        return errors
    
    # --------------------------- UTILS functions -----------------------------
 
    def _getArgs(self):
        """ Prepare the args dictionary."""

        args = {'--halfmap1': os.path.relpath(self._getFileName('input_half1Fn'),
                                              self._getExtraPath()),
                '--halfmap2': os.path.relpath(self._getFileName('input_half2Fn'),
                                              self._getExtraPath()),
                '--fullmap': os.path.relpath(self._getFileName('input_volFn'),
                                             self._getExtraPath()),
                '--apix': self.inputVolume.get().getSamplingRate(),
                '--ThreeDFSC': 'vol',
                '--dthetaInDegrees': self.dTheta.get(),
                '--FSCCutoff': self.fscCutoff.get(),
                '--ThresholdForSphericity': self.thrSph.get(),
                '--HighPassFilter': self.hpFilter.get(),
                '--numThresholdsForSphericityCalcs': self.numThr.get(),
                '--histogram': 'histogram'
                }
        if self.applyMask and self.maskVolume:
            args['--mask'] = os.path.relpath(self._getFileName('input_maskFn'),
                                             self._getExtraPath())
        return args

    def findSphericity(self, fn):
        with open(fn, 'r') as f:
            sph = 0.
            for line in f:
                if 'Sphericity is ' in line:
                    sph = float(line.split()[2])

        return sph
