"""Global configuration class setting default behaviour, importing contur loads all of the following

:Module members:

Where these are settable from the command line. See ```contur --help``` for documentation.

    * **useTheoryCorr** (``bool``) see ```--xtc```
   
    * **offline** (``bool``) see ```--offline```

    * **vetoAnalyses** (``string``) see ```--ana-match```
    * **onlyAnalyses** (``string``) see ```--ana-unmatch```
    * **splitAnalysis** (``bool``) see ```--ana-split```

    * **exclude_met_ratio** (``bool``) see ```--xr```
    * **exclude_hgg** (``bool``) see ```--xhg```
    * **exclude_hww** (``bool``) see ```--xhw```
    * **exclude_awz** (``bool``) see ```--awz```
    * **exclude_b_veto** (``bool``) see ```--wbv```
    * **exclude_searches** (``bool``) see ```-s```
    * **exclude_soft_physics** (``bool``) see ```--soft_physics```
    * **tracks_only** (``bool``) see ```--tracks_only```

    * **gridMode** (``bool``) see ```-g```
    * **weight** (``string``) see ```--wn``

    * **binwidth** see ```--BW```
    * **binoffset** see ```--BO```
    * **blocklist** (default {"MASS","STOPMIX"}) see ```--S```


Stats/fitting, parameters, see ```contur --help```

    * **min_num_sys**
    * **look_elsewhere**

Batch system

    * using_condor
    * condor_os
    * **using_qsub** (Default)
    * using_slurm
    * seed (random number seed)

Presentation options for rivet

    * nostack If true, don't stack signal and background for display

These are used by ```contur-plot```

    * contour_colour
    * map_colorCycle (set to None, will be initialised from colour config if a pool name is unrecognised)
    * plot_format (pdf or png)

Default file names

    * mceg (default "herwig")
    * mceg_template (default "herwig.in")
    * paramfile (default "params.dat")
    * tag (default "runpoint")
    * unneeded_files (default ["herwig.run","Looptools.log", "py.py", "mgevents"])
      These files will be removed when runing ```contur-gridtool```
    * param_steering_file (default "param_file.dat")
    * summary_file (default Summary.txt)
    * output_dir (default ANALYSIS)
    * batch_output_dir (default myscan00)

These are used internally, set from other conditions.

    * **silenceWriter** (``bool``) --
      Disables a lot of plotting output, for when it is not needed (eg in grid mode).

    * **contur_log** (``logging.logger``) logger object

    * **stat_types** ["DATABG","SMBG","EXP","HLEXP"] This indexes different ways of evaluating a likelihood.
       DATABG: using the data as the background. This can always be done and is what has been used for most 
       contur results so far.
       SMBG: if we have the Standard Model prediction, we evaluate the exclusion using this as the background too.
       EXP: this is the expected limit. Evaluated by moving the data central value to the SM prediction (when we have one) 
       HLEXP: this is the expected limit. Evaluated as above, but reducing the uncertainties by sqrt of lumi ratio to the projected HL-LHC

"""
contur_log=None

logfile_name="contur.log"

# this will make numpy raise exceptions instead of printing warnings
import numpy
numpy.seterr(all="raise")

def setup_logger(filename=logfile_name, logstream=None, level="ERROR"):
    """
    set up the logger object

    :param filename: name of log file
    """

    import logging, sys
    import contur.config.config as cfg
    cfg.logfile_name=filename

    level = getattr(logging, level)

    #for some reason we can't supply a formatter to the basic config: https://stackoverflow.com/questions/34319521/python-logging-module-having-a-formatter-causes-attributeerror
    if logstream is None:
        try:
            logging.basicConfig(
                level=level,
                format='%(name)s - %(levelname)s - %(message)s',
                filemode="w",
                filename=cfg.logfile_name,
            )
        except:
            print("Can not write your logfile to {}. Writing to $CONTUR_USER_DIR instead".format(os.path.join(os.getcwd(),cfg.logfile_name)))
            cfg.logfile_name = os.path.join(paths.user_path(),cfg.logfile_name)
            logging.basicConfig(
                level=level,
                format='%(name)s - %(levelname)s - %(message)s',
                filemode="w",
                filename=cfg.logfile_name,
            )

    else:
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            stream=logstream
        )

    stream = logging.StreamHandler(sys.stdout)
    FMT=logging.Formatter('%(levelname)s - %(message)s')
    stream.setFormatter(FMT)

    file_handler = logging.FileHandler(cfg.logfile_name)
    file_handler.setFormatter(FMT)

    cfg.contur_log=logging.getLogger("contur")
    cfg.contur_log.addHandler(stream)
    cfg.contur_log.addHandler(file_handler)
    cfg.contur_log.propagate=False

# Setup some module level variable defaults
multi_p = True

graphics = True

# switch for input type. default is signal only, but can be switched to signal+SM combined
sig_plus_bg = False

# if true, only use the diagonal elements of the covariance matrices
diag=False
# treat theory systematics as correlated within a plot
useTheoryCorr=True

# run offline (dont query inspire db)
offline=False

vetoAnalyses=[]
onlyAnalyses=[]
exclude_met_ratio=False
exclude_hgg=False
exclude_hww=True
exclude_b_veto=True
exclude_awz=True
exclude_searches=True
exclude_soft_physics=True
tracks_only=False
splitAnalysis=False

weight=""

# minimum number of systematic uncertainty contributions before they will be treated as correlated via NPs
min_num_sys=5
# only treat theory uncertainties as correlated if we have at least stat+4 scale variations for example.
min_num_sys_sm=5
# include null results in ll ratio
look_elsewhere=False
# use spey for test stat calculations
use_spey = False

found_ref = []
found_thy = []
silenceWriter=False #For API mode: disable file output

binwidth=-100.
binoffset=0.

using_condor=False
using_qsub  =True
using_slurm =False
seed = 101

condor_os = "CentOS7"
condor_jdl_extras = ["+JobFlavour = 'testmatch'"] #< needed for CERN lxbatch

mceg="herwig"
known_mcegs = ["herwig",  "madgraph","pbzpwp", "pythia8" ]
default_nev=30000
mceg_template=mceg+".in"
keep_hepmc=False


# Some default filenames
conturenv="conturenv.sh"
paramfile="params.dat"
tag="runpoint"
unneeded_files=["herwig.run","Looptools.log", "py.py", "mgevents"]
blocklist={"MASS","STOPMIX"}
csvfile=None
param_steering_file="param_file.dat"
summary_file="Summary.txt"

# current runpoint (the beam and the number identifying the param point, eg 13TeV/0001)
runpoint="" 

#####################
# Various directories
#####################
import os
import contur.config.paths as paths

# These directories are operational and can generally be changed from the command line
######################################################################################
# Top level directory where output of a contur run will be written
output_dir="ANALYSIS"
# Top level directory where output of a contur run will be read from
input_dir="ANALYSIS"
# Location of UFO file and analysis list (*.ana) input for contur-batch
run_info = "RunInfo"
# Top level directory containing a grid being processed.
grid=None



# These directories are operational but will be configured internally
#####################################################################
# Directory to write all plots and html to
plot_dir=os.path.join(output_dir,"plots")
# Directory to write plotting scripts to
script_dir=os.path.join(output_dir,"scripts")
# Configured from user environment. Location of analysis db and default analysis lists
share = paths.user_path()

# These directories are default values. They can't be changed but may be overridden
###################################################################################
# default directory to write all the SM plots to.
smdir = "sm_plots"
# directories to ignore when looking for yoda files.
hidden_directories=["mgevents","ANALYSIS"]
# Directory where the batch scripts will be written by contur-batch
batch_output_dir="myscan00"

# switch to tell contur whether it is running on a grid or on a single yoda file
gridMode=False
# file containing plain text summary of a grid run.
grid_summary_file="GridSummary.txt"

add_to_results_db=False
results_dbfile="contur_run.db"
models_dbfile="models.db"

import re
# This allows for the form EXPERIMENT_YEAR_INSPIRENUMBER or EXPERIMENT_PHYSICSGROUP_YEAR_ID
APATT=r'(([A-Z0-9]+_\d{4}_[IS]\d{5,8})|([A-Z0-9]+_[A-Z]{4}_\d{4}_[A-Z0-9]+)'
ANALYSISPATTERN = re.compile(APATT+r')')
ANALYSIS        = re.compile(r'('+APATT+r')[^/]*)')
ANALYSISHISTO   = ANALYSISHISTO   = re.compile(r'('+APATT+r')[^/]*)/((d\d+-x\d+-y\d+)|\w+)')

# reference data indexed by the yoda object path
refObj = {}
refCorr = {}
refUncorr = {}
refErrors = {}
# SM theory predictions indexed by analysis name
sm_prediction = {}
prediction_choice = "A"

# A one-off to hold objects that have been scaled in an unscaled form for plotting
plotObj = {}


# various types of statistic evaluations
databg = "DATABG"
smbg = "SMBG"
expected = "EXP"
hlexpected = "HLEXP"
stat_types = [databg,smbg,expected,hlexpected]
stat_to_human = {
    databg : "bkg=data",
    smbg : "bkg=SM",
    expected : "exp.",
    hlexpected : "exp. (HL-LHC)",
}
primary_stat = smbg
hllhc_intl_fb = 3000.0

# rivet histo display
nostack = False

# plotting config
contour_colour = {}
contour_colour[databg]="white"
contour_colour[smbg]="black"
contour_colour[expected]="black"
contour_colour[hlexpected]="red"
contour_style = {}
contour_style[databg]="solid"
contour_style[smbg]="solid"
contour_style[expected]="dotted"
contour_style[hlexpected]="dotted"
map_colorCycle=None
plot_format="pdf"

class _DuplicateFilter(object):
    """
    Private class to filter log messages so only one instance shows once, from:
    from https://stackoverflow.com/questions/31953272/python-logging-print-message-only-once
    """
    def __init__(self):
        self.msgs = set()

    def filter(self, record):
        rv = record.msg not in self.msgs
        self.msgs.add(record.msg)
        return rv

class ConturError(Exception):
    pass
