"""'emsdk' verb to setup and use emscripten SDK

'emsdk setup [version]' to download/update/install/activate emsdk, 'version' defaults to 'latest'
'emsdk [other]' to relay commands to 'emsdk' script once installed
"""

import os
import subprocess
import sys

if sys.version_info > (3, 0):
    import urllib.request as urllib
else:
    import urllib

from mod import log, emscripten, util

#-------------------------------------------------------------------------------
def run(fips_dir, proj_dir, args) :
    """run the 'emsdk' verb"""

    emsdk_dir = emscripten.get_emsdk_dir(fips_dir)

    if _emsdk_exists(emsdk_dir):
        # relay commands to emsdk script
        return _emsdk_command(emsdk_dir, args)

    if len(args) > 0 and args[0] == 'setup':

        if len(args) > 1:
            emsdk_version = args[1]
        else:
            emsdk_version = 'latest'

        _emsdk_setup(fips_dir, proj_dir, emsdk_version)
    
    else:
        log.error("invalid command", args)

#-------------------------------------------------------------------------------
def help() :
    """print help text for init verb"""
    log.info(log.YELLOW +
             "fips emsdk setup\n"
             + log.DEF +
             "    setup emscripten SDK") 


#-------------------------------------------------------------------------------
def _emsdk_exists(emsdk_dir):
    emsdk_file = os.path.join(emsdk_dir, 'emsdk')
    return os.path.isfile(emsdk_file)

#-------------------------------------------------------------------------------
def _emsdk_command(emsdk_dir, args):

    command = './emsdk'
    if util.get_host_platform() == 'win' :
        command = 'emsdk.bat'

    args = [command] + args
    _subprocess_call(args=args, cwd=emsdk_dir, shell=True)
    
#-------------------------------------------------------------------------------
def _emsdk_setup(fips_dir, proj_dir, emsdk_version):
    """setup the emscripten SDK from scratch"""
    log.colored(log.YELLOW, '=== setup emscripten SDK:')

    emscripten.ensure_sdk_dirs(fips_dir)

    # download SDK archive
    archive_path = emscripten.get_archive_path(fips_dir)
    archive_name = emscripten.get_archive_name()
    sdk_dir = emscripten.get_sdk_dir(fips_dir)
    emsdk_dir = emscripten.get_emsdk_dir(fips_dir)

    if not os.path.isfile(archive_path):
        log.info("downloading '{}'...".format(archive_name))
        urllib.urlretrieve(emscripten.get_sdk_url(), archive_path, util.url_download_hook)
    else :
        log.info("'{}' already exists".format(archive_name))

    # uncompress SDK archive
    log.info("\nuncompressing '{}'...".format(archive_name))
    emscripten.uncompress(archive_path, sdk_dir, 'emsdk-portable')

    # setup SDK
    log.info("setup emscripten SDK...")
    _finish(emsdk_dir, emsdk_version)

    log.colored(log.GREEN, "done.")


#-------------------------------------------------------------------------------
def _finish(emsdk_dir, emsdk_version) :
    """finish setting up the emscripten SDK
    """
    command = './emsdk'
    if util.get_host_platform() == 'win' :
        command = 'emsdk.bat'

    _subprocess_call(args=command+' update', cwd=emsdk_dir, shell=True)
    _subprocess_call(args=command+' install --shallow --disable-assertions {}'.format(emsdk_version), cwd=emsdk_dir, shell=True)
    _subprocess_call(args=command+' activate --embedded {}'.format(emsdk_version), cwd=emsdk_dir, shell=True)


#-------------------------------------------------------------------------------
def _subprocess_call(args, cwd, shell):

    log.info("calling " + str(args) + " in " + cwd)
    return subprocess.call(args=args, cwd=cwd, shell=shell)
