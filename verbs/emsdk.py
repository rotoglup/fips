"""'emsdk' verb to setup and use emscripten SDK

emsdk setup
"""

from mod import log, emscripten, nacl, android

#-------------------------------------------------------------------------------
def run(fips_dir, proj_dir, args) :
    """run the 'emsdk' verb"""
    sdk_name = None
    if len(args) > 0 and args[0] == 'setup':
        _emsdk_setup(fips_dir, proj_dir)
    else :
        log.error("invalid command", args)

#-------------------------------------------------------------------------------
def help() :
    """print help text for init verb"""
    log.info(log.YELLOW +
             "fips emsdk setup\n"
             + log.DEF +
             "    setup emscripten SDK") 
    
#-------------------------------------------------------------------------------
def _emsdk_setup(fips_dir, proj_dir):
    log.info("setup")