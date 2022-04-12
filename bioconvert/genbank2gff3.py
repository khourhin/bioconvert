###########################################################################
# Bioconvert is a project to facilitate the interconversion               #
# of life science data from one format to another.                        #
#                                                                         #
# Authors: see CONTRIBUTORS.rst                                           #
# Copyright © 2018  Institut Pasteur, Paris and CNRS.                     #
# See the COPYRIGHT file for details                                      #
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
###########################################################################
"""Convert :term:`GENBANK` to :term:`GFF3` format"""

from bioconvert import ConvBase

__all__ = ["GENBANK2GFF3"]


class GENBANK2GFF3(ConvBase):
    """Convert :term:`GENBANK` file to :term:`GFF3` file

    Method based on biocode.

    """

    #: Default value
    _default_method = "biocode"

    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: input GENBANK file
        :param str outfile: output GFF3 filename

        """
        super(GENBANK2GFF3, self).__init__(infile, outfile)

    def _method_biocode(self, *args, **kwargs):
        """Uses scripts from biocode
        
        Please see `Main entry  <https://github.com/jorvis/biocode/>`_ and specific converter
        `here: <https://github.com/jorvis/biocode/blob/master/gff/convert_genbank_to_gff3.py>`_"""
        cmd = "convert_genbank_to_gff3.py -i {} -o {} --no_fasta".format(
            self.infile, self.outfile
        )
        self.execute(cmd)
