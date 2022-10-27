###########################################################################
# Bioconvert is a project to facilitate the interconversion               #
# of life science data from one format to another.                        #
#                                                                         #
# Copyright © 2018-2022  Institut Pasteur, Paris and CNRS.                #
#                                                                         #
# bioconvert is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# bioconvert is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program (COPYING file).                                 #
# If not, see <http://www.gnu.org/licenses/>.                             #
#                                                                         #
# Repository: https://github.com/bioconvert/bioconvert                    #
# Documentation: http://bioconvert.readthedocs.io                         #
###########################################################################
"""Convert :term:`CRAM` file to :term:`SAM` format"""
import os

import colorlog

from bioconvert import ConvBase
from bioconvert.core.base import ConvArg
from bioconvert.core.decorators import requires

logger = colorlog.getLogger(__name__)


class CRAM2SAM(ConvBase):
    """Convert :term:`CRAM` file to :term:`SAM` file

    The conversion requires the reference corresponding to the input file
    It can be provided as an argument with the standalone (*-\\-reference*).
    Otherwise, users are asked to provide it.

    Methods available are based on samtools [SAMTOOLS]_.
    """

    #: Default value
    _default_method = "samtools"
    _threading = True

    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: input CRAM file
        :param str outfile: output SAM filename

        """
        super(CRAM2SAM, self).__init__(infile, outfile, *args, **kargs)

    def _get_reference(self):
        # In case the --reference is not used
        msg = "Please enter the reference corresponding "
        msg += "to the input BAM file:"
        reference = input(msg)
        if os.path.exists(reference) is False:
            raise IOError("Reference required")
        else:
            logger.debug("Reference exists ({}).".format(reference))
        return reference

    @requires("samtools")
    def _method_samtools(self, *args, **kwargs):
        """Here we use the SAMtools tool.

        `SAMtools documentation <http://www.htslib.org/doc/samtools.html>`_"""
        # -h means include header in SAM output
        reference = kwargs.get("reference", None)
        if reference is None:
            reference = self._get_reference()

        cmd = "samtools view -@ {} -h -T {} {} > {}".format(self.threads, reference, self.infile, self.outfile)
        self.execute(cmd)

    @classmethod
    def get_additional_arguments(cls):
        yield ConvArg(
            names="--reference",
            default=None,
            help="the reference used (FASTA format). If not provided, prompt will appear",
        )
