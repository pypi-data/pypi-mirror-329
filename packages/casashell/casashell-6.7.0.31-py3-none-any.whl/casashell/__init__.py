import os as _os
import sys as _sys
import argparse as _argparse
from traitlets.config.loader import Config

__name__ = 'casashell'
__all__ = [ "start_casa", "argv", "flags", "version", "version_string", "extra_task_modules" ]

extra_task_modules = [ ]

def version( ): return [ 6, 7, 0,31 ]
def version_string( ): return "6.7.0.31"

argv = _sys.argv

flags = [ ]

# these are the log messages generated during startup before the logger is available
startup_log = [ ]

from casaconfig import config as casa_config_master

def __init_config(config,flags,args):
    if flags.datapath is not None:
        # expand all of the datapath elements in the string, separated by a colon
        # and then only include abspath to the ones that are directories
        datap = list(map(_os.path.expanduser,list(flags.datapath.split(':'))))
        datap = list(map(_os.path.abspath,filter(_os.path.isdir,datap)))
        config.datapath = datap

    config.flags = flags
    config.args = args
    
def start_casa( argv ):
    moduledir = _os.path.dirname(_os.path.realpath(__file__))

    ###
    ### this will be used by inp/go which are introduced in init_subparam
    ###
    casa_inp_go_state = { 'last': None }

    ###
    ### this will be used by register_builtin for making casa builtins immutable
    ###
    casa_builtin_state = { }
    casa_nonbuiltin_state = { }    ### things that should be builtin but are not

    ##
    ## filled when -c <args> is used
    ##
    casa_eval_status = { 'code': 0, 'desc': 0 }

    init_scripts = [ "init_begin_startup.py",
                     "init_system.py",
                     "load_tasks.py",
                     "load_tools.py",
                     "init_subparam.py",
                     "init_doc.py",
    ]
    # optional user startup.py and init_welcome.py added later - after optional init_pipeline.py

    ##
    ## final interactive exit status...
    ## runs using "-c ..." exit from init_welcome.py
    ##
    _exit_status=0
    try:
        import casashell as _cs

        colorsChoices = ['Neutral', 'NoColor', 'Linux', 'LightBG']
        # defaultColor is only used here when the color in casa_config_master is invalid - assumed to be invalid in config.py
        defaultColor = 'Neutral' 

        from casaconfig.private.get_argparser import get_argparser

        parser = get_argparser(add_help=True)
        parser.prog = 'casa'
        parser.description = 'CASA bootstrap'
        parser.add_argument( "--startupfile",dest='startupfile',default=None,
                            help="path to user's startup.py")
        parser.add_argument( "--nostartupfile", dest='nostartupfile', action='store_const', const=True, default=False,
                             help='do not use any startup file')
        parser.add_argument( '--logfile',dest='logfile',default=None,help='path to log file' )
        parser.add_argument( "--log2term",dest='log2term',action='store_const',const=True,default=False,
                             help='direct output to terminal' )
        parser.add_argument( "--nologger",dest='nologger',action='store_const',const=True,default=False,
                             help='do not start CASA logger' )
        parser.add_argument( "--nologfile",dest='nologfile',action='store_const',const=True,default=False,
                             help='do not create a log file' )
        parser.add_argument( "--nogui",dest='nogui',action='store_const',const=True,default=False,
                             help='avoid starting GUI tools' )
        parser.add_argument( "--cachedir",dest='cachedir',default=None,
                             help="location for internal working files")
        parser.add_argument( '--colors', dest='prompt', default=None,
                             help='prompt color', choices=colorsChoices )
        parser.add_argument( "--pipeline",dest='pipeline',action='store_const',const=True,default=False,
                             help='start CASA pipeline run' )
        parser.add_argument( "--agg",dest='agg',action='store_const',const=True,default=False,
                             help='startup without graphical backend' )
        parser.add_argument( '--iplog',dest='ipython_log',default=False,
                             const=True,action='store_const',
                             help='create ipython log' )
        parser.add_argument( '--datapath',dest='datapath',default=None,
                             help='data path(s) [colon separated]' )
        parser.add_argument( '--reference-testing', dest='reference_testing',action='store_const',const=True,default=False,
                             help='force *measurespath* to contain the casarundata when this version was produced, used for testing purposes')
        parser.add_argument( '--no-auto-update', dest='no_auto_update',action='store_const',const=True,default=False,
                             help='turn off all auto updates')
        parser.add_argument( "--user-site",dest='user_site',default=False,
                             const=True,action='store_const',
                             help="include user's local site-packages lib in path" )
        parser.add_argument( "-v", "--version",dest='showversion',action='store_const',const=True,default=False,
                            help='show CASA version' )
        parser.add_argument( "-c",dest='execute',default=[],nargs=_argparse.REMAINDER,
                             help='python eval string or python script to execute' )

        # obsolete arguments still parsed here so that they now generate errors when invoked
        # help is suppressed to hide them in the usage output

        parser.add_argument( "--trace",dest='trace',action='store_const',const=True,default=False,
                             help=_argparse.SUPPRESS)
        
        # this was silently turned off several releases ago. It used to use "console" on macs due to perceived slowness of casalogger
        parser.add_argument( "--maclogger",dest='maclogger',action='store_const',const='console',
                             default='/does/this/still/make/sense',
                             help=_argparse.SUPPRESS )

        # these obsolate arguments are fatal errors when used
        # rcdir was renamed / repurposed as cachedir
        parser.add_argument( '--rcdir',dest='rcdir',default=None,help=_argparse.SUPPRESS )

        # norc was renamed as noconfig
        parser.add_argument( '--norc',dest='norc',default=None,help=_argparse.SUPPRESS )
        
        flags,args = parser.parse_known_args(argv)

        # version, show and exit, ignore everything else
        if flags.showversion:
            print("CASA %s " % version_string())
            _sys.exit(0)

        # watch for the discontinued arguments, just warn, these print statements are not logged
        if flags.trace:
            print("\nWARN: --trace is not available.\n")

        if flags.maclogger=='console':
            print("\nWARN: --maclogger is not available. The default casalogger will be used.\n")

        # these discontinued arguments are fatal
        if flags.rcdir is not None:
            print("\nERROR: --rcdir is no longer used, use --cachedir to select a different location of CASA cache files,")
            print("         use --configfile and --startupfile to specify locations of those files if not in ~/.casa")
            print("casa can not continue ...")
            _sys.exit(1)

        if flags.norc is not None:
            print("\nERROR: --norc is no longer used. Use --noconfig to turn off using the optional user's config.py")
            print("casa can not continue ...")
            _sys.exit(1)

        _cs.argv = argv
        _cs.flags = flags

        __init_config(_cs.casa_config_master,flags,args)

        # prepend startup_log with messages related to the configuration 
        try:
            # I think there should be at most 1 of these, but just in case
            user_config_list = _cs.casa_config_master.__user_config
            if len(user_config_list) > 0 :
                for user_config in user_config_list  :
                    # was it actually used
                    if user_config in _cs.casa_config_master.load_success():
                        _cs.startup_log.append(("Using user configuration file %s" % user_config, "INFO"))
                    else:
                        # no, if it exists, signal it was going to be used (matches behavior before casaconfig)
                        # all errors printed out and logged after this loop
                        if _os.path.exists(_os.path.abspath(_os.path.expanduser(user_config))):
                            _cs.startup_log.append(("Using user configuration file %s" % user_config, "INFO"))
                        else: 
                            # the only reason it gets to here is if the optional user config.py file was not found
                            startup_log.append(("optional configuration file not found, continuing CASA startup without it", "INFO"))
            else:
                # not used because of noconfig, I'm not sure if there are any other cases where this else block can happen
                if (_cs.casa_config_master.__flags.noconfig) :
                    startup_log.append(("noconfig flag used, skipping any user configuration file", "INFO"))

            # log any config errors
            loadFailures = _cs.casa_config_master.load_failure()
            for config_err in loadFailures:
                startup_log.append(("evaluation of %s failed" % config_err, "ERROR"))
                startup_log.append((loadFailures[config_err], "ERROR"))

        except:
            pass

        # print out any startup log messages in config - they've not yet been printed
        print("")
        if len(_cs.startup_log) > 0:
            for logTuple in _cs.startup_log:
                if logTuple[1] == 'INFO':
                    print(logTuple[0])
                else:
                    print("%s: %s" % (logTuple[1],logTuple[0]))

        # all of these values are known to exist in casa_config_master
        # make sure flags and corresponding casa_config_master values agree as appropriate

        if flags.startupfile is None:
            flags.startupfile = _cs.casa_config_master.startupfile
        else:
            flags.startupfile = _os.path.abspath(_os.path.expanduser(flags.startupfile))
            _cs.casa_config_master.startupfile = flags.startupfile
            if flags.nostartupfile:
                print("WARN: nostartupfile and startupfile command line options are both present, startupfile is ignored!")
                startup_log.append(("nostartupfile and startupfile command line options are both present, startup file will be ignored!", "WARN"))

        if flags.nostartupfile:
            # warning already given if startupfile is also present
            # turn off the startup file
            flags.startupfile = None
            _cs.casa_config_master.startupfile = None

        if flags.logfile is None:
            flags.logfile = _cs.casa_config_master.logfile
        else:
            flags.logfile = _os.path.abspath(_os.path.expanduser(flags.logfile))
            _cs.casa_config_master.logfile = flags.logfile

        if flags.log2term:
            _cs.casa_config_master.log2term = flags.log2term
        else:
            flags.log2term = _cs.casa_config_master.log2term

        if flags.nologger:
            _cs.casa_config_master.nologger = flags.nologger
        else:
            flags.nologger = _cs.casa_config_master.nologger

        if flags.nologfile:
            _cs.casa_config_master.nologfile = flags.nologfile
        else:
            flags.nologfile = _cs.casa_config_master.nologfile

        if flags.nogui:
            _cs.casa_config_master.nogui = flags.nogui
        else:
            flags.nogui = _cs.casa_config_master.nogui

        if flags.cachedir is None:
            flags.cachedir = _cs.casa_config_master.cachedir
        else:
            flags.cachedir = _os.path.abspath(_os.path.expanduser(flags.cachedir))
            _cs.casa_config_master.cachedir = flags.cachedir

        # colors is more complicated
        if flags.prompt is None:
            if _cs.casa_config_master.colors not in colorsChoices:
                msg = "colors value in config file is invalid: %s (choose from %s); using %s" % (_cs.casa_config_master.colors, colorsChoices,defaultColor)
                priority="WARN"
                _cs.startup_log.append((msg,priority))
                print("%s: %s" % (priority,msg))
                _cs.casa_config_master.colors = defaultColor
            flags.prompt = _cs.casa_config_master.colors
        else:
            _cs.casa_config_master.colors = flags.prompt

        if flags.pipeline:
            _cs.casa_config_master.pipeline =  flags.pipeline
        else:
            flags.pipeline = _cs.casa_config_master.pipeline

        if flags.agg:
            _cs.casa_config_master.agg = flags.agg
        else:
            flags.agg = _cs.casa_config_master.agg

        if flags.ipython_log:
            _cs.casa_config_master.iplog = flags.ipython_log
        else:
            flags.ipython_log = _cs.casa_config_master.iplog

        # datapath already handled elsewhere

        if flags.user_site:
            _cs.casa_config_master.user_site = flags.user_site
        else:
            flags.user_site = _cs.casa_config_master.user_site

        # some flags values imply other flags values, some flags values take precedence over others, sort that out next

        # nologfile implies --logfile /dev/null
        # also nologfile takes precedence over logfile argument
        if flags.nologfile:
            flags.logfile = "/dev/null"
            _cs.casa_config_master.logfile = flags.logfile

        # nogui implies no logger
        if flags.nogui:
            flags.nologger = True
            _cs.casa_config_master.nologger = flags.nologger

        if flags.pipeline:
            init_scripts += [ "init_pipeline.py" ]

        if flags.no_auto_update:
            _cs.casa_config_master.data_auto_update = False
            _cs.casa_config_master.measures_auto_update = False

        # this next step must come after config et al have been imported so that user_site is available if set in config.py
        # having the current working directory (an empty element) in sys.path can cause problems - protect the user here
        _sys.path = [p for p in _sys.path if len(p) > 0]
        # if user installs casatools into their local site packages it can cause problems
        if not flags.user_site:
            if _sys.platform == "darwin":
                _sys.path = [p for p in _sys.path if _os.path.join(_os.path.expanduser("~"),"Library/Python",) not in p]
            else:
                _sys.path = [p for p in _sys.path if _os.path.join(_os.path.expanduser("~"),".local","lib",) not in p]

            _os.environ['PYTHONNOUSERSITE'] = "1"
        else:
            # this makes no sense if PYTHONOOUSERSITE is already set
            if 'PYTHONNOUSERSITE' in _os.environ:
                print("\nERROR: --user-site has been used while PYTHONNOUSERSITE is set. Please unset PYTHONNOUSERSITE and try --user-site again.\n")
                _sys.exit(1)

        from IPython import __version__ as ipython_version
        configs = Config( )

        # does the optional startup.py exist at startupfile
        if _cs.casa_config_master.startupfile is not None:
            startupPath = _os.path.abspath(_os.path.expanduser(_cs.casa_config_master.startupfile))
            if _os.path.isfile(startupPath):
                # let the user know where startup.py is coming from
                # user's don't want to see a fully expanded path
                msg = "Using user-supplied startup.py at %s" % _cs.casa_config_master.startupfile
                _cs.startup_log.append((msg,"INFO"))
                print(msg)
                init_scripts += [ startupPath ]

        print("")

        # the use of the reference-testing options happens here so that the data is already in place before casatools is imported
        if flags.reference_testing:
            # this requires that measurespath exist
            if _cs.casa_config_master.measurespath is None or (not _os.path.exists(_cs.casa_config_master.measurespath)):
                print("\n\tERROR! measurespath is not set to an existing location : %s" % _cs.casa_config_master.measurespath)
                print("\nThe measurespath config value should be set to a directory that contains the expected data necessary to use CASA.")
                print("It should be set in site config file or the user's ~/.casa/config.py to a location containing that data.")
                print("If that location exists, but is empty and owned by the user, and data_auto_update and measures_auto_update are both true")
                print("then normal casa startup will download the data into that location.")
                print("\n")
                for config_file in _cs.casa_config_master.load_success():
                    print("\tloaded config file : %s" % config_file)
                    print("\nvisit https://casadocs.readthedocs.io/en/stable/notebooks/external-data.html for more information\n")
                _sys.exit(1)

            msg = "reference testing using pull_data and 'release' version into %s" % _cs.casa_config_master.measurespath
            print(msg)
            _cs.startup_log.append((msg,"INFO"))
            try:
                from casaconfig import pull_data, get_data_info
                hasReleaseInfo = get_data_info(_cs.casa_config_master.measurespath, type='release') is not None
                if not hasReleaseInfo:
                    msg = "no release data info is available, probably not a monolithic CASA, no changes to the installed data due to --reference-testing option"
                    _cs.startup_log.append((msg,"INFO"))
                    print(msg)
                else:
                    pull_data(_cs.casa_config_master.measurespath,'release')
            except:
                print("There was an unexpected exception in casaconfig.pull_data trying to set the casarundata to 'release', can not continue")
                #import traceback
                #traceback.print_exc()
                _sys.exit(1)

            if hasReleaseInfo:
                # this assumes the pull_data worked, make sure any auto updates don't undo that
                #  the check on timestamp should already stop that, but this makes sure
                _cs.casa_config_master.data_auto_update = False
                _cs.casa_config_master.measures_auto_update = False
                msg = "auto updates are turned off"
                print(msg)
                _cs.startup_log.append((msg,"INFO"))
                
            print('\n')
            
        init_scripts += [ "init_welcome.py" ]
        startup_scripts = filter( _os.path.isfile, map(lambda f: _os.path.join(moduledir,"private",f), init_scripts ) )

        cacheDirPath = _os.path.abspath(_os.path.expanduser(_cs.casa_config_master.cachedir))
        ipythonDirPath = _os.path.join(cacheDirPath, "ipython")
        _os.makedirs(ipythonDirPath, exist_ok=True)

        configs.TerminalInteractiveShell.ipython_dir = ipythonDirPath
        configs.TerminalInteractiveShell.banner1 = 'IPython %s -- An enhanced Interactive Python.\n\n' % ipython_version
        configs.TerminalInteractiveShell.banner2 = ''
        configs.HistoryManager.hist_file = _os.path.join(configs.TerminalInteractiveShell.ipython_dir,"history.sqlite")
        configs.InteractiveShellApp.exec_files = list(startup_scripts)
        configs.InteractiveShell.show_rewritten_input = False

        if flags.agg or flags.pipeline:
            configs.TerminalIPythonApp.matplotlib = 'agg'
            configs.InteractiveShellApp.matplotlib = 'agg'
            import matplotlib
            matplotlib.use('agg')

        else:
            # CAS-14370: Running these causes plots to fail with sigtrap when using matplotlib 3.8.3 or higher on Mac.
            # The error reads: "Secure coding for state restoration requested after it was initialized without. NSApplicationDelegate was probably established too late." 
            if _sys.platform != "darwin":
                configs.TerminalIPythonApp.matplotlib = 'auto'
                configs.InteractiveShellApp.matplotlib = 'auto'
       
        from IPython import start_ipython
        start_ipython( config=configs, argv= (['--logfile='+_cs.casa_config_master.iplogfile] if flags.ipython_log else []) + ['--ipython-dir='+ipythonDirPath, '--autocall=2', '--colors='+flags.prompt] + (["-i"] if len(flags.execute) == 0 else ["-c","__evprop__(%s)" % flags.execute]) )
      

    except Exception as exc:
        casa_eval_status['code'] = 1
        casa_eval_status['desc'] = f'unexpected exception raised in casashell init: {type(exc).__name__} {exc}'

    if casa_eval_status['code'] != 0:
        print(f'CASA exits with a non-zero status : {casa_eval_status["desc"]}')

    return casa_eval_status['code']
