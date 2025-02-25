# make rivet plots

import os, sys, subprocess
from multiprocessing import cpu_count
import argparse
import re
import contur.factories.depot
import contur.factories.likelihood_point
import contur.config.config as cfg
import contur.util.utils as cutil
import contur.plot.html_utils as html
import contur.data.static_db as cdb
from contur.run.arg_utils import setup_common
import traceback


def main(args):

    setup_common(args)
    print("Writing log to {}".format(cfg.logfile_name))
    
    # run on maximum available cores
    numcores = cutil.get_numcores(args["NCORES"])

    cfg.input_dir = args["INPUTDIR"]
    cfg.plot_dir = os.path.join(cfg.input_dir,"plots")

    if args['ANAPATTERNS']:
        cfg.onlyAnalyses = args['ANAPATTERNS']
    if args['ANAUNPATTERNS']:
        cfg.vetoAnalyses = args['ANAUNPATTERNS']
        
    # try to open results database and fill a depot.
    file = os.path.join(cfg.input_dir,cfg.results_dbfile)
    cfg.script_dir = os.path.join(cfg.input_dir,"scripts")
    cfg.plot_dir = os.path.join(cfg.input_dir,"plots")
    try:

        # try parsing the runpoint argument to see if it is of the form beam/model_point
        runpoint=args["RUNPOINT"]
        if runpoint is not None:
            try:
                # try parsing the runpoint for a model point ID
                p = int(runpoint.split('/')[1])
                b = runpoint.split('/')[0]
                cfg.contur_log.info("Looking for model point {} for beam {}.".format(p,b))
            except:
                cfg.contur_log.error("Runpoint requested ({}) is not of the form beam/model_point. Terminating.".format(runpoint))
                sys.exit(1)
        else:
            cfg.contur_log.info("No run point specified, will read all points from DB.")
            
        # build a new depot class
        contur_depot = contur.factories.depot.Depot()

        # read only a single runpoint from db file into the depot if "--runpoint" is specified
        contur_depot.add_points_from_db(file,runpoint=runpoint)
        cfg.contur_log.info("Read DB file {}".format(file))

        # placeholder
        lh_point = contur_depot.points[0]
        matched=False

        if len(contur_depot.points) < 1:
            raise Exception 
        elif len(contur_depot.points) == 1 and runpoint is None:
            # this is the case when running on a single yoda.
            runpoint = ""
        else:
            if runpoint is None:           
                cfg.contur_log.warning("More than one model point found. Will use the first.")
                try:
                    first_yf = lh_point.yoda_files.split(",")[0]
                    beam_energy = first_yf.split("/")[-3]   # e.g. 13TeV
                    run_point_id = first_yf.split("/")[-2]  # e.g. 0023
                except:
                    raise
                    
                runpoint = os.path.join(beam_energy,run_point_id)

            else:
                beam_energy, run_point_id = runpoint.split("/")

                for i, depot_point in enumerate(contur_depot.points):
                    if depot_point.get_run_point()[0] == run_point_id:
                        lh_point = depot_point
                        matched = True
                        break
                if not matched:
                    # TODO error; when running on multiple beams it does not always work
                    # e.g. -b 13TeV,8TeV and then .db file only contains 13TeV points
                    cfg.contur_log.error(f"You specified runpoint {runpoint} but" \
                                            " it was not found in the DB file")
                    sys.exit(1)

            cfg.plot_dir = os.path.join(cfg.plot_dir,runpoint)
            cfg.script_dir = os.path.join(cfg.script_dir,runpoint)
            cutil.mkoutdir( cfg.plot_dir)
            cfg.contur_log.info("Looking for plot scripts in {}".format(cfg.script_dir))
 
    except Exception as e:
        raise
        print(e)
        cfg.contur_log.warning("Could not open results file {}. Some info will be missing".format(file))
        lh_point = contur.factories.likelihood_point.LikelihoodPoint()

    # build histograms dictionary containing plot paths
    # for each histogram and corresponding level of exclusion
    if args["OUTPUTDIR"] is None:
        cfg.output_dir = cfg.plot_dir

    cutil.mkoutdir(cfg.output_dir)
    histograms = {}
    pool_exclusions = {}
    histo_exclusions = {}
    pools = [cdb.get_pool(poolid=pdir) for pdir in os.listdir(cfg.script_dir)
             if os.path.isdir(os.path.join(cfg.script_dir,pdir))]
    for pool in pools:
        pool_exclusions[pool] = {}
        fullpooldir = os.path.join( cfg.script_dir, pool.id)
        histograms[pool] = {}
        pool_exclusions[pool] = {}
        for stat_type in cfg.stat_types:
            try:
                pool_exclusions[pool][stat_type] = lh_point.pool_exclusion_dict[stat_type][pool.id]
            except KeyError:
                # this means there's no exclusion for this stat_type. If this is because there's no
                # SM prediction, that's fine.
                cfg.contur_log.debug(traceback.format_exc())
                pool_exclusions[pool][stat_type] = None

        analyses = [cdb.get_analyses(analysisid=adir,filter=False)[0] for adir in os.listdir(fullpooldir)
                    if os.path.isdir(os.path.join(fullpooldir,adir))]
        for ana in analyses:
            fullanadir = os.path.join(fullpooldir, ana.name)
            histograms[pool][ana] = {}
            scripts = [script for script in os.listdir(fullanadir)
                       if os.path.isfile(os.path.join(fullanadir,script))
                       and script.endswith("py")
                       and not script.endswith("__data.py")]
            for script in scripts:
                h = script.split(".py")[0]

                try:
                    obs_exclusions = lh_point.obs_excl_dict[os.path.join("/",ana.name,h)]
                except KeyError:
                    cfg.contur_log.debug("no exclusions found for {}. {}".format(ana.name,traceback.format_exc()))
                    obs_exclusions = {}
                histograms[pool][ana][script] = obs_exclusions
                
    # decide which plots to generate based on --ana-match, --ana-unmatch and --CLS
    pyScripts, matchedPools, matchedAnalyses, matchedHistos = html.selectHistogramsForPlotting(histograms,pool_exclusions,args["CLS"],args["PRINTONLY"],args["INCLUDENONE"])
    full_exclusions = {}
    for stat_type in cfg.stat_types:
        try:
            ex = lh_point.combined_exclusion_dict[stat_type]
        except:
            traceback.print_exc()
            ex = None
        if ex is not None:
            full_exclusions[stat_type] = ex
        else:
            full_exclusions[stat_type] = 0.0
            
    # write HTML pages for matched analyses/pools
    html.writeIndexHTML(matchedPools, matchedAnalyses, matchedHistos, lh_point.param_point, full_exclusions)

    cutil.make_mpl_plots(pyScripts,numcores)
    cfg.contur_log.info("...done!")

