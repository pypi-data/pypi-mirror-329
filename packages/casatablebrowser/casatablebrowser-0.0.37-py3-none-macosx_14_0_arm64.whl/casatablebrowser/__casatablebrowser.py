##########################################################################
#
# Copyright (C) 2021,2022
# Associated Universities, Inc. Washington DC, USA.
#
# This script is free software; you can redistribute it and/or modify it
# under the terms of the GNU Library General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public
# License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#
# Correspondence concerning AIPS++ should be adressed as follows:
#        Internet email: casa-feedback@nrao.edu.
#        Postal address: AIPS++ Project Office
#                        National Radio Astronomy Observatory
#                        520 Edgemont Road
#                        Charlottesville, VA 22903-2475 USA
###########################################################################
'''``browsetable`` implementation'''
import os as __os
import subprocess
import atexit
import platform


def browsetable( tablename=None, cleanup=True ):
    '''Brings up a browser that can open and display any CASA table (MS, calibration table, image)

    The ``tablename`` can be specified at
    startup, or any table can be loaded after the browser GUI comes up.
    It is possible to edit any table and its contents using the "Edit"
    tab on the top bar, but be careful with this, and make a backup
    copy of the table before editing!

    The tab "table keywords" on the left side of the table browser
    will allow you to look at sub-tables by left-clicking and then
    view the desired sub-table. Another useful feature is to make a 2D
    plot of the values in two table columns.

    Use the "Close Tables and Exit" option from the Files menu to quit
    the ``casabrowser``.

    A detailed description on how to use the table browser can be
    found in the Chapter pages on `"Browsing through MeasurementSets
    and Calibration
    Tables" <https://casadocs.readthedocs.io/en/stable/notebooks/data_examination.html#Browse-MS/Calibration-Tables>`__.

    Parameters
    ----------

    tablename: str
        Path to the table directory on disk (MS, cal. table, image)
        default: none; example: tablename='ngc5921.ms'

    Examples
    --------
    To open the table browser and display the contents of table
    ``measurementset.ms``::

      browsetable(tablename='measurementset.ms')

    To get a plot of two table values, click on tools, then click on
    plot 2D.

    Example 1: to get a u-v plot, in the Plotter Option Gui::

      set Rows:  0   to  <Large Number>
      X Axis:  UVW      Slice  (set 0)
      Y Axis:  UVW      Slice  (set 1)
      click 'Clear and Plot' on right.

    Example 2: to get visibility plots::

      X Axis:  TIME
      Y Axis:  DATA     Slice Amplitude
      click 'Clear and Plot' on right.

    '''
    app_path = __os.path.abspath(__os.path.dirname(__file__))
    flavor = platform.system( )
    if flavor == 'Linux':
        app_path = __os.path.join( app_path, "__bin__","casatablebrowser-x86_64.AppImage" )
    elif flavor == 'Darwin':
        app_path = __os.path.join( app_path, '__bin__', 'casatablebrowser.app',
                                   'Contents', 'MacOS', 'casatablebrowser' )
    else:
        raise Exception('unsupported platform')

    args = [ app_path ]
    if tablename is not None:
        if __os.path.isdir(tablename):
            args.append( tablename )
        else:
            raise RuntimeError( '"tablename" parameter is not a directory' )

    try:
        proc = subprocess.Popen(args)
        if cleanup:

            @atexit.register
            def stop_casatablebrowser():
                proc.kill()

    except FileNotFoundError as error:
        print(f"Error: {error.strerror}")


if __name__ == "__main__":
    browsetable(False)
