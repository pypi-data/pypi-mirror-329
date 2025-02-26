
###
### misc remaining builtins
###
register_builtin( [ "inp", "go", "casalog", "casatools", "casatasks" ] )
from casashell.private.builtin_mgr import unregister_builtin
unregister_builtin( [ "display" ] )

###
### cleanup global namespace
###
del register_builtin
del unregister_builtin

###
### Include the casatools/casatasks module version number at the end of the startup prompt
### If they are equal, just include one copy otherwise include both version numbers
###
try:
    import casalith as __casalith
    print("CASA %s -- Common Astronomy Software Applications [%s]" % (__casalith.version_string( ),casatasks.version_string( )))
    del __casalith
except:
    import casashell as __casashell
    print("CASA %s -- Common Astronomy Software Applications" % __casashell.version_string( ))
    del __casashell

###
### post any startup log messages
###

try:
    from casashell import startup_log
    for logTup in startup_log:
        casalog.post(logTup[0],logTup[1])
except:
    pass

###
### log the config files used
###
try:
   from casashell import casa_config_master
   for config_file in casa_config_master.load_success():
       casalog.post("loaded config file : %s" % config_file)
except:
    casalog.post("problem determining which config files were loaded","ERROR")
    import traceback
    traceback.print_exc()

### log what the data at measurespath appears to be (versions when possible)
msgs = []
problems = False
try:
    from casaconfig import get_data_info
    # use measurespath found in ctsys
    user_measurespath = casatools.ctsys.measurespath()
    data_info = get_data_info(user_measurespath, casalog)
    if data_info is None:
        msgs.append('Unable to determine any information about casarundata or measures versions.')
        problems = True
    else:
        rundataInfo = data_info['casarundata']
        if rundataInfo is None:
            msgs.append('Unable to determine version information for casarundata')
            problems = True
        else:
            if rundataInfo['version'] == "invalid":
                msgs.append('casarundata is invalid and likely to not contain any of the expected data.')
                problems=True
            elif rundataInfo['version'] == "unknown":
                msgs.append('casarundata version is unknown, this is probably a legacy version not installed by casaconfig')
            else:
                msgs.append('casarundata version : %s' % rundataInfo['version'])

        measuresInfo = data_info['measures']
        if measuresInfo is None:
            msgs.append('Unable to determine version information for measures')
            problems = True
        else:
            if measuresInfo['version'] == "invalid":
                msgs.append('measures is invalid and likely to not contain any of the expected data.')
                problems=True
            elif measuresInfo['version'] == "unknown":
                msgs.append('measures version is unknown, this is probably a legacy version not installed by casaconfig')
            else:
                msgs.append('measures version : %s' % measuresInfo['version'])

except Exception as e:
    print(e)
    msgs.append('There was an unexpected exception when determining the installed casarundata and measures versions')
    problems=True

###
### log the config values
###
from casaconfig import get_config   # list of config keyword = value formatted as strings to be printed
casalog.post('')
casalog.post('config values')
for configString in get_config():
    casalog.post('    ' + configString)
casalog.post('')
    
if problems:
    msgs.append('Other messages will have appeared before this that may help diagnose the problem.')
    msgs.append('CASA will probably be unusable until this is fixed.')

if problems:
    # print and log these as WARN messages
    print("\n")
    for msg in msgs:
        print(msg)

    for msg in msgs:
        casalog.post(msg,"WARN")

else:
    for msg in msgs:
        casalog.post(msg)
        
###
### Verify geodetic Measures tables
###

checkgeodetic()
