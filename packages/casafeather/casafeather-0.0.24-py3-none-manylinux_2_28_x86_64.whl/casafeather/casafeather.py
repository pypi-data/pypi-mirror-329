##########################################################################
#
# Copyright (C) 2019
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

import os as __os
import subprocess
import atexit
import platform
from casatools import ctsys as __ctsys


def casafeather(cleanup=True):
    """Start the casafeather application in a subprocess.

    For more information about casafeather, see the casafeather documentation in `CASAdocs <https://casadocs.readthedocs.io/en/stable/notebooks/image_combination.html#Visual-Interface-for-feather-(casafeather)>`_.

    Args:
        cleanup (bool): If True, the subprocess will be terminated when the Python session ends.
    """
    app_name = ""
    if platform.system() == "Darwin":
        app_name = "casafeather/__bin__/casafeather.app/Contents/MacOS/casafeather"
    elif platform.system() == "Linux":
        app_name = "casafeather/__bin__/casafeather-x86_64.AppImage"
    else:
        raise Exception("Unsupported platform")

    app_path = __os.path.join(
        __os.path.abspath(__os.path.join(__os.path.dirname(__file__), "..")),
        app_name,
    )

    try:
        print("Starting CASAfeather\n")
        env = __os.environ.copy( )
        env['CASADATA'] = __ctsys.rundata( )
        p = subprocess.Popen(app_path,env=env)
        if cleanup:

            @atexit.register
            def stop_casafeather():
                print("Exiting CASAfeather\n")
                p.kill()

    except FileNotFoundError as error:
        print(f"Error: {error.strerror}")


if __name__ == "__main__":
    casafeather(False)
