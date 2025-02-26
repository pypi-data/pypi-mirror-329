###
### add configuration files for casatools and casatasks
###
import platform
import sys
import os

from casashell import argv
from casashell import casa_config_master as config
# casaconfig exceptions to catch
from casaconfig import BadLock, NoReadme, RemoteError, AutoUpdatesNotAllowed, NotWritable, UnsetMeasurespath

def __static__(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate


###
### ensure that the CASA modules are available within the shell
###

import casaconfig

# catch ImportError exceptions when importing casatools - likely measures data failure
try:
    import casatools
except (AutoUpdatesNotAllowed, NotWritable, NoReadme) as exc:
    # similar initial user errors
    print("")
    print(exc)
    print("")
    print("casaconfig is trying to download data to %s (measurespath)" % (config.measurespath))
    # slightly different messages here
    if isinstance(exc, AutoUpdatesNotAllowed):
        # two possibilities
        if os.path.exists(config.measurespath):
            # the problem is permissions
            print("but the directory is not owned by the current user.")
            print("Please change the directory ownership and re-start CASA.")
        else:
            print("but the directory does not exist.")
            print("To allow casa to download ~1GB of data to this path, please create this directory and re-start CASA.")
    elif isinstance(exc, NotWritable):
        print("but the current user does not have write permissions for that directory.")
        print("Please change the directory permissions and re-start CASA.")
    elif isinstance(exc, NoReadme):
        print("but that path does not contain the casaconfig files identifying it as a casaconfig-managed")
        print("copy of the casarundata. The given path is also not empty so casaconfig is unable to")
        print("extablish a copy of the casarundata there.")
        print("That location also does not appear to be a non-casaconfig-managed copy of the expected data.")
        print("Please empty that directory and re-start casa.")
    else:
        # this should never happen
        print("This is an unexpected exception. Hopefully the details of the exception offer some insight into how to proceed")
        print("Please report this problem to CASA. You should not be seeing this message.")
        print("To work around this please try using a different path.")
        
    print("If you would prefer to use a different path, please see the instructions in the External Data documentation here:")
    print("https://casadocs.readthedocs.io/en/stable/notebooks/external-data.html")
    print("")
    os._exit(1)
except UnsetMeasurespath as exc:
    print("")
    print(exc)
    print("")
    print("The value of measurespath is not set and casatools can not find the expected data in datapath.")
    print("casa can not continue.")
    print("set measurespath in your personal config.py file or use a site config file that has that value set appropriately for that site")
    print("For more details, please see the instructions in the External Data documentation here:")
    print("https://casadocs.readthedocs.io/en/stable/notebooks/external-data.html")
    print("")
    os._exit(1)    
except BadLock as exc:
    print("")
    print(exc)
    print("")
    print("The lock file associated with %s (measurespath) is not empty and castools was unable to start." % config.measurespath)
    print("This likely means that there was a problem during installation or update of casarundata or measures.")
    print("This also means that casatools was unable to find the expected IERS data in datapath (which includes measurespath)")
    print("This is best addressed by deleting measurespath and recreating it and reinstalling the data.")
    print("For more details, please see the instructions in the External Data documentation here:")
    print("https://casadocs.readthedocs.io/en/stable/notebooks/external-data.html")
    print("")
    os._exit(1)
except RemoteError as exc:
    print("")
    print(exc)
    print("")
    print("Either there is no network connection, there is no route to the remote server, or the remote server is offline.")
    print("No IERS data was found in datapath and casatools can not be imported. casashell can not continue.")
    print("")
    os._exit(1)
except ImportError as exc:
    print("")
    print(exc)
    print("")
    print("There were problems when importing casatools, casashell can not continue.")
    print("This is unexpected but the details of the excption (shown previously) may help.")
    print("If this seems to be a problem with the casarundata or measures data it may be necessary")
    print("to change measurespath or remove the data in measurespath so that that location is empty")
    print("and then restart CASA.")
    print("For more details, please see the instructions in the External Data documentation here:")
    print("https://casadocs.readthedocs.io/en/stable/notebooks/external-data.html")
    print("")
    os._exit(1)
    
import casatasks

###
### import legacy tools if available...
###
try:
    import casalith
except:
    pass

try:
    from casatablebrowser import browsetable
except:
    pass

try:
    from casafeather import casafeather
except:
    pass

try:
    from casalith import msuvbin
except:
    pass

try:
    from casaviewer.gotasks.imview import imview
except:
    try:
        from casaviewer import imview
    except:
        if platform.system( ) == "Darwin":
            def imview( *args, **kwargs ):
                try:
                    casalog.post(
                        "casaviewer is no longer available for macOS, for more information see: http://go.nrao.edu/casa-viewer-eol",
                        "WARN",
                        "imview",
                    )
                except: pass
                raise RuntimeError("imview is no longer available for macOS, for more information see: http://go.nrao.edu/casa-viewer-eol")

try:
    from casaviewer.gotasks.msview import msview
except:
    try:
        from casaviewer import msview
    except:
        if platform.system( ) == "Darwin":
            def msview( *args, **kwargs ):
                try:
                    casalog.post(
                        "casaviewer is no longer available for macOS, for more information see: http://go.nrao.edu/casa-viewer-eol",
                        "WARN",
                        "msview",
                    )
                except: pass
                raise RuntimeError("msview is no longer available for macOS, for more information see: http://go.nrao.edu/casa-viewer-eol")

try:
    from casaplotms.gotasks.plotms import plotms
except:
    try:
        from casaplotms import plotms
    except:
        pass

# When in monolithic CASA, the servers must start their serve() loop now
# (CAS-12799), after all the tasks, etc that might be used by the pipeline
# and/or advanded users of parallel mode that push imports to servers.
try:
    import importlib
    _clith_spec = importlib.util.find_spec("casalith")
    if _clith_spec is not None:
        import casampi.private.start_mpi
except ImportError:
    pass

###
### start logger if the executable can be found and the log file
### is writable... (this will need to be adjusted for MacOS)
###

### Try config.flags.nologger first, else look for it in argv
dologger = True
try:
    dologger = not config.flags.nologger
except:
    dologger = '--nologger' not in argv

if dologger:
    import os
    log = casatools.logsink( ).logfile( )
    if os.access( log, os.W_OK ):
        try:
            from casalogger import casalogger
            casalogger(log)
        except:
            pass

###
### execfile(...) is required by treaties and obligations (CAS-12222), but
### only in CASAshell...
###
def execfile(filename,globals=globals( ),locals=None):
    from runpy import run_path
    newglob = run_path( filename, init_globals=globals )
    for i in newglob:
        globals[i] = newglob[i]


###
### checkgeodetic() - verify the contents of the most important Measures tables
###
def checkgeodetic():
    """
    Verify the contents of the most important Measures tables
    """
    import os
    from casatools import ctsys
    from casatools import table as tbtool
    from casatools import quanta as qatool
    from casatasks import casalog
    rval = True
    geodeticdir = ctsys.rundata()+'/geodetic' #os.path.dirname(ctsys.resolve('geodetic/IERSpredict'))
    if not os.path.isdir(geodeticdir):
        casalog.post('Data repository directory not found. Cannot check Measures tables. Retrieved path was \"'+geodeticdir+'\"', 'WARN')
        rval = False
    else:
        casalog.post('\n', 'INFO')
        casalog.post('Checking Measures tables in data repository sub-directory '+geodeticdir, 'INFO')
        mytb = tbtool()
        mytables=['IERSeop2000', 'IERSeop97', 'IERSpredict', 'TAI_UTC']
        for mytable in mytables:
            if not os.path.isdir(geodeticdir+'/'+mytable):
                casalog.post('Measures table '+mytable+' does not exist. Expected at '+geodeticdir+'/'+mytable, 'WARN')
                rval = False
            else:
                mytb.open(geodeticdir+'/'+mytable)
                vsdate = mytb.getkeyword('VS_DATE')
                mjd = mytb.getcol('MJD')
                if len(mjd)>0:
                    myqa = qatool()
                    mydate = myqa.time({'value': mjd[-1], 'unit': 'd'}, form='ymd')[0]
                    casalog.post('  '+mytable+' (version date, last date in table (UTC)): '+vsdate+', '+mydate, 'INFO')
                else:
                    casalog.post(mytable+' contains no entries.', 'WARN')
                    rval = False
                mytb.close()
    return rval


###
### evaluate scriptpropogating errors out of ipython
###
def __evprop__(args):
    import os
    import sys
    from runpy import run_path
    exit_status = None
    if len(args) > 0:
        try:
            if os.path.isfile(args[0]):
                import sys
                exec_globals = globals( )
                exec_globals['sys'].argv = args
                run_path( args[0], init_globals=exec_globals, run_name='__main__' )
            else:
                for stmt in args:
                    exec(stmt)
        except SystemExit as err:
            exit_status = { 'code': err.code, 'desc': 'system exit called' }
        except:
            import traceback
            traceback.print_exc(file=sys.stderr)
            exit_status = { 'code': 1, 'desc': 'exception: %s' % sys.exc_info()[0] }
    else:
        exit_status = { 'code': 1, 'desc': 'no file or statement' }

    if exit_status is not None:
        import inspect
        frame = inspect.currentframe( )
        while frame is not None:
            if 'casa_eval_status' in frame.f_locals and \
               type(frame.f_locals['casa_eval_status']) is dict:
                status = frame.f_locals['casa_eval_status']
                for k in exit_status:
                    status[k] = exit_status[k]
                break
            frame = frame.f_back

###
### set the CASA prompt
###
from IPython.terminal.prompts import Prompts, Token

class _Prompt(Prompts):
     def in_prompt_tokens(self, cli=None):
         return [(Token.Prompt, 'CASA <'),
                 (Token.PromptNum, str(self.shell.execution_count)),
                 (Token.Prompt, '>: ')]

_ip = get_ipython()
try:
    ## generally thought to make tab completion faster...
    _ip.Completer.use_jedi = False
except: pass

_ip.prompts = _Prompt(_ip)

del __static__
