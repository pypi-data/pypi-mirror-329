# -*- python -*-

"""
Functions to deal with plotting yoda/rivet histograms

"""
import os
import contur
import contur.config.config as cfg
import contur.factories.likelihood as lh
import contur.util.utils as cutil
from rivet import stripOptions, mkStdPlotParser, getAnalysisPlotPaths
import rivet.plotting.make_plots as rivet_make_plots


def createYODAPlotObjects(observable, nostack=False, smtest=False):
    """
    Make YODA objects for theory, theory+BSM and/or data+BSM and return in-memory objects
    in a dictionary.

    :param nostack: flag saying whether to plot data along or stack it on the background (default)
    :type boolean:

    :param observable: dressed YODA ao
    :type observable: :class:`contur.factories.Observable`

    the output directory is determined by cfg.plot_dir

    """
    CLs = {}
    YODAinMemory = {}

    histopath = observable.signal.path()
    ## Check if we have reference data for this observable. If not, then abort.
    if not observable.ref:
        cfg.contur_log.warning("Not writing dat file for {}. No REF data.".format(observable.signal.path()))
        return

    # placeholders to include yoda strings later
    yodastr_sigback_databg = yodastr_theory = yodastr_sigback_smbg = None

    if (cfg.primary_stat == cfg.databg or observable.thyplot is None) and not smtest:
        show_databg = True
    else:
        show_databg = False

    # get the data and signal+data plots
    refdata = observable._refplot

    if nostack:
        # in this case we are just plotting signal, without stacking it on any background
        sigback_databg  = observable.sigplot
    else:
        sigback_databg = observable.stack_databg

    refdata.setAnnotation('Title', '{} Data'.format(observable.analysis.experiment()))
    refdata.setAnnotation('RatioPlot', True)

    # get analysis and histogram name
    ana = observable.analysis.name
    tag = observable.histo_name

    if smtest:
        tag += observable.sm_prediction.id
        refdata.setAnnotation('RatioPlotYLabel', 'SM/Data')
    else:
        refdata.setAnnotation('RatioPlotYLabel', 'Ratio to Data')


    # write data-as-background signal plot
    if show_databg:
        legendLabel = get_legend_label(observable, nostack, cfg.databg)

        # set annotations in the YODA object, used later to go on the legend label
        sigback_databg.setAnnotation('Title', legendLabel)
        YODAinMemory['Data as BG'] = {histopath : {'0' : sigback_databg}}

    # things we only do if there's a SM prediction.
    if observable.thyplot:

        # get theory histogram
        theory = observable._thyplot.clone()

        # identifier for the theory prediction that was used in this case.
        if nostack:
            # in this case we are just plotting signal, without stacking it on any background
            if smtest:
                sigback_smbg   = None
            else:
                sigback_smbg   = observable.sigplot
        else:
            sigback_smbg   = observable.stack_smbg

        # write theory.yoda file, for mpl based plotting
        theory.setPath(theory.path().split("/THY")[1]) # for mpl-based plotting, remove prepending THY in YODA
        YODAinMemory['Theory'] = {histopath : {'0' : theory}}

        # if we want to add SM plus BSM
        if not smtest:
            legendLabel = get_legend_label(observable, nostack, cfg.smbg)
            sigback_smbg.setAnnotation('Title', legendLabel)
            #outfstring = observable.signal.path()+ '_SMBG'
            #exclusions.write(f'exclusions["{outfstring}"] = {CLs}\n')
            YODAinMemory['SM as BG'] = {histopath : {'0' : sigback_smbg}}
        else:
            pval = observable.get_sm_pval()
            theory.setAnnotation('Title','{}, p = {:4.2f}'.format(theory.title(),pval))

    #exclusions.close()

    return YODAinMemory

def assemble_plotting_data(observable, yodaMCs, config_files=[], plotdirs=[]):
    """
    Contur version of rivet assemble_plotting_data, takes histogram path,
    YODA histograms and rivet references string as input, returns 'outputdict'
    which is the required input for rivet.script_generator

    :param hpath: string referring to the histogram path, normally of the form
        <ANALYSIS>/<OBSERVABLE> where rivet.stripOptions has been used to strip off
        the run mode of the analysis

    :param yodaMCs: dictionary containing MC YODA files, with either theory,
        theory+BSM or data+BSM. Is obtained from createYODAPLOTObjects and looks like:
        yodaMCs = {'Data as BG' : {'<hpath>' : {'0': <YODA 2D scatter>} } }

    :param thisRefYODA: YODA object for reference data

    """

    thisRefYODA = observable._refplot
    hpath = observable.signal.path()


    # find reference data, which is already loaded in config fileg
    refhistos = {stripOptions(hpath) : thisRefYODA}

    reftitle = thisRefYODA.title()

    # fetch plot options from .plot file for each analysis (e.g. Title, axis labels)
    plotparser = mkStdPlotParser(getAnalysisPlotPaths())
    plotoptions = {'PLOT' : plotparser.getPlot(stripOptions(hpath))}

    # set the title for YODA files to appear in the legend, including the exclusion
    for YODAtype, histogram in yodaMCs.items():
        plotoptions[YODAtype] = {'Title' : histogram[hpath]['0'].annotation('Title') }

    # make output dictionary which is used to write executable python scripts
    return rivet_make_plots._make_output(
            stripOptions(hpath), plotdirs, config_files, yodaMCs, refhistos,
            plotoptions, style='default', rc_params={}, mc_errs=False, nRatioTicks=1,
            showWeights=True, removeOptions=True, deviation=True, canvasText=None,
            refLabel = refhistos[stripOptions(hpath)].title(),
            ratioPlotLabel = refhistos[stripOptions(hpath)].annotation('RatioPlotYLabel'),
            showRatio=True, verbose=False
          )

def get_legend_label(observable, nostack=cfg.nostack, background=""):
    """
    return the figure of merit and an appropriate legend label.

    """

    if background == cfg.databg:
        legendLabel = "BSM+Data "
    elif background == cfg.smbg:
        legendLabel = "BSM+SM "
    elif background == 'SMTest':
        legendLabel = "SM Prediction"

    # set annotations for the data-as-background signal plot
    if background == cfg.databg:

        if cfg.use_spey:
            mu_upper_limit = observable.likelihood.get_mu_upper_limit(cfg.databg)

            if mu_upper_limit is not None:
                if observable.likelihood._index is not None and cfg.databg in observable.likelihood._index.keys():
                    indextag = r"Bin {}, upper $\mu$ = {:4.2f} @ 95\% $CL_s$".format(observable.likelihood._index[cfg.databg],mu_upper_limit)
                else:
                    indextag = r"upper $\mu$ = {:4.2f} @ 95\% $CL_s$ ".format(mu_upper_limit)
            else:
                indextag = "No exclusion"
        else:

            CLs = observable.likelihood.getCLs(cfg.databg)

            # add it to the legend.
            if CLs is not None and CLs > 0:
                if observable.likelihood._index is not None and cfg.databg in observable.likelihood._index.keys():
                    indextag=r"Bin {},excl. {:2.0f}\%".format(observable.likelihood._index[cfg.databg],100.*CLs)
                else:
                    indextag=r"excl. {:2.0f}\%".format(100.*CLs)
            else:
                indextag="No exclusion"

        legendLabel += indextag

    if observable.thyplot:
        # things we only do if there's a SM prediction.
        theory = observable.thyplot

        if background == 'SMTest':

            # Calculate the compatibility between SM and data, using chi2 survival for the number of points
            pval = observable.get_sm_pval()

            # add the SM vs data compatibility to the legend.
            if observable.likelihood._index is not None and cfg.smbg in observable.likelihood._index.keys():
                indextag="p (Bin {})={:4.2f}".format(observable.likelihood._index[cfg.smbg],pval)
            else:
                indextag="p = {:4.2f}".format(pval)
            theory.setAnnotation('Title','{}, {}'.format(theory.title(),indextag))
            legendLabel += f'{theory.title()}, {indextag}'

        elif background == cfg.smbg:

            if cfg.use_spey:
                mu_upper_limit = observable.likelihood.get_mu_upper_limit(cfg.smbg)
                mu_hat = observable.likelihood.get_mu_hat(cfg.smbg)
                excl = observable.likelihood.getCLs(cfg.smbg)
                
                mu_upper_limit_exp = observable.likelihood.get_mu_upper_limit(cfg.expected)
                mu_hat_exp = observable.likelihood.get_mu_hat(cfg.expected)
                
                if mu_upper_limit is not None and mu_upper_limit_exp is not None:
                    if observable.likelihood._index is not None and cfg.smbg in observable.likelihood._index.keys():
                        indextag = r"Bin {}, $\mu_{{\text{{max}}}}$ = {:4.2f} @ 95\% $\text{{CL}}_\text{{s}}$, $\hat\mu$ = {:4.2f} \newline (expected upper$\mu_{{\text{{max}}}}$ = {:4.2f} @ 95\% $\text{{CL}}_\text{{s}}$, $\hat\mu$ = {:4.2f})".format(observable.likelihood._index[cfg.smbg],mu_upper_limit,mu_hat,mu_upper_limit_exp,mu_hat_exp)
                    else:
                        indextag = r"$\mu_{{\text{{max}}}}$ = {:4.2f} @ 95\% $\text{{CL}}_\text{{s}}$, $\hat\mu$ = {:4.2f} \newline (expected $\mu_{{\text{{max}}}}$ = {:4.2f} @ 95\% $\text{{CL}}_\text{{s}}$, $\hat\mu$ = {:4.2f})".format(mu_upper_limit,mu_hat,mu_upper_limit_exp,mu_hat_exp)
                elif mu_upper_limit_exp is not None:
                    indextag = r"No upper limit; expected $\mu_{{\text{{max}}}}$ = {:4.2f} @ 95\% $\text{{CL}}_\text{{s}}$, $\hat\mu$ = {:4.2f}".format(mu_upper_limit_exp,mu_hat_exp)
                elif excl is not None and excl > 0.0:
                    indextag = "$\mu = 1$ disfavoured at {:4.2f}\%".format(100.*excl)
                else:
                    indextag = "No exclusion"

            else:
                # get the dominant test likelihood for this plot.
                CLs = observable.likelihood.getCLs(cfg.smbg)
                CLs_exp = observable.likelihood.getCLs(cfg.expected)

                # add them to the legend.
                if CLs is not None and CLs_exp is not None and CLs > 0:
                    if observable.likelihood._index is not None and cfg.smbg in observable.likelihood._index.keys():
                        indextag=r"Bin {},excl. {:2.0f}\% \newline ({:2.0f}\% expected)".format(observable.likelihood._index[cfg.smbg],100.*CLs,100.*CLs_exp)
                    else:
                        indextag=r"excl. {:2.0f}\% \newline ({:2.0f}\% expected)".format(100.*CLs,100.*CLs_exp)
                elif CLs_exp is not None:
                    indextag=r"No exclusion; expected exclusion was {:2.0f}\%".format(100.*CLs_exp)
                else:
                    indextag="No exclusion"

            # set annotations for the sm-as-background signal plot
            legendLabel += indextag

    return legendLabel

