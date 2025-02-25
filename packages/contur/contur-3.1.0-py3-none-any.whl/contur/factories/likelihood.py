"""
This module contains the implementation of the likelihood calculation, and various functions to manipulate test statistics.

Abstracted from the underlying ``YODA`` objects, this module defines
two ways to construct likelihood functions from numerical types:

    * :class:`~contur.factories.likelihood.Likelihood` -- The base likelihood building blocks, representing the information extracted from an underlying histogram of potentially correlated observables.

    * :class:`~contur.factories.likelihood.CombinedLikelihood` -- A shell to combine :class:`~contur.factories.likelihood.Likelihood` blocks into a full likelihood, automatically encodes assumption that the included blocks are uncorrelated.
"""
import sys
import logging
import numpy as np
import scipy.stats as spstat
from numpy import linalg as la
from scipy.optimize import minimize
import copy

import contur
import contur.config.config as cfg
import contur.data.static_db as cdb

class Likelihood(object):
    """Fundamental likelihood-block class and confidence-interval calculator

    This class defines the structure of a series of observables to be constructed into a hypothesis test

    :Keyword Arguments:
        * **calculate** (``bool``) -- Perform the statistics calculation (otherwise the input variables are just set up)
        * **ratio** (``bool``) -- Flag if data is derived from a ratio measurement (not general! caveat emptor!)
        * **profile** (``bool``) -- Flag if data is derived from a profile histogram measurement
        * **lumi** (``float``) -- the integrated luminosity in the units of the measurement. used to calculate expected stat uncertainty on signal
        * **lumi_fb** (``float``) -- the integrated luminosity for the measurement in fb. used to scale for HL-LHC
        * **sxsec** (``float``) -- Signal cross-section in picobarns, if non-null
        * **tags** (``string``) -- names of the histograms this is associated with  
        * **sm_values** (:class:`Observable_Values`) -- All the numbers for the SM prediction
        * **measured_values** (:class:`Observable_Values`) -- All the numbers for the measurement
        * **bsm_values** (:class:`Observable_Values`) -- All the numbers for the signal
        * **expected_values** (:class:`Observable_Values`) -- The SM prediction with data uncertainties.
        

    """
    
    def __init__(self, calculate=False,
                 ratio=False, profile=False, 
                 lumi=1.0, lumi_fb=1.0, sxsec=None, bxsec=None,
                 tags='',sm_values=None, measured_values=None, bsm_values=None, expected_values=None):

        self._covariances    = {}
        self._inverses       = {}
        self._ndof = {}

        
        self.measured_values = measured_values
        self.expected_values = expected_values
        self.sm_values       = sm_values
        self.bsm_values      = bsm_values
        
        if measured_values is not None:
            self._nbins = len(measured_values.central_values)                
        elif expected_values is not None:
            self._nbins = len(expected_values.central_values)
            
        self._lumi = lumi
        self._lumi_fb = lumi_fb
        self._sxsec = sxsec
        self._bxsec = bxsec

        self.ratio = ratio
        self.profile = profile

        # various statistics etc. 
        self._pval = {}
        self._sm_pval = None
        self._CLs = {}
        self._index  = {}
        self._ts_s_b = {}
        self._ts_b = {}      
        self._mu_upper_limit = {}  
        self._mu_hat = {}
        # attribute to hold chi-square test stats for cases where we have no covariance matrix
        self._test_stats = {}

        # A bool to work out whether the correlations should be used or not
        self._singleBin = False

        # the histogram names
        self._tags = tags
        # these are set later.
        self._pools = ''
        self._subpools = ''

        # spey statistical models
        self.spey_model = {}

        # for single bin mode, this holds a model for each bin
        self.spey_model_list = {}

        # do this if asked and if there is no BSM (doing SM test) or there are non-zero BSM entries
        #if (self.bsm_values is None or self.bsm_values.central_values.any()) and calculate:
        if calculate:
            # build the inverse covariance matrices.
            self.__buildCovinv()

            # build the spey models, or calculate the test stats the Contur way
            if cfg.use_spey:
                self.build_spey_models()
            else:
                try:
                    self.__build_stats()
                except Exception as ex:
                    cfg.contur_log.error("Error calculating test stats for {}: {}".format(self._tags,ex))
                    raise
                
    def __build_stats(self):
        """Internal function to trigger the calculation of the various statistical metrics on initialisation.
        """
        mu_null = 0.0
        # this is the master flag that says whether we will use a covariance matrix (diagonal or not) or the single-bin method.
        cfg.contur_log.debug("USING SINGLE BIN METHOD={}".format(self._singleBin))
        
        for stat_type in cfg.stat_types:

            # if there's no signal object, we're doing SM comparison so only do the SMBG version
            if self.bsm_values is None and stat_type != cfg.smbg:
                continue

            
            if self.bsm_values is not None:
                # the first part checks for histograms with all zero entries. The second checks for counters with nan (which is
                # what they are if never filled).
                if (not self.bsm_values.central_values.any()) or (len(self.bsm_values.central_values==1) and np.isnan(self.bsm_values.central_values[0])):     
                    # No signal in this plot.
                    # Do we treat this as "no information" or as "allowed". Choice based on cfg.look_elsewhere
                    if cfg.look_elsewhere:
                        if self._singleBin:
                            self._test_stats[stat_type] = 0.0, 0.0
                        else:   
                            self._ts_s_b[stat_type] = 0.0
                            self._ts_b[stat_type] = 0.0
                        continue
                    else:
                        # tests stats will be None
                        return

            # We keep all test stats when we don't have the covariance matrix, the
            # test stats we keep are then used by likelihood_blocks_find_dominant_ts method                    
            if self._singleBin:
                self._test_stats[stat_type] = self.__chisq(stat_type, mu_test=1.0, mu_null=mu_null)
                
            else:
                self._ts_s_b[stat_type], self._ts_b[stat_type] = self.__chisq(stat_type, mu_test=1.0, mu_null=mu_null)
                
                cfg.contur_log.debug("Test stats are {}, {} for {} stat type {}".format(self._ts_s_b[stat_type], self._ts_b[stat_type], self._tags, stat_type))
                if self._ts_s_b[stat_type] is not None and self._ts_b[stat_type] is not None:
                    if self._ts_s_b[stat_type] < self._ts_b[stat_type]:
                        cfg.contur_log.debug("BSM+SM is in better agreement with data for {}. Setting pvalues equal.".format(self._tags))
                        self._ts_s_b[stat_type] = 0.0
                        self._ts_b[stat_type] = 0.0
                    elif self._ts_s_b[stat_type] < 0.0 or self._ts_b[stat_type] < 0.0:
                        cfg.contur_log.warning("Negative test stat for {} (sb {}, b {}). This is probably a numerical precision issue. Setting both to zero, no exclusion from this plot.".format(self._tags,self._ts_s_b[stat_type],self._ts_b[stat_type]))
                        self._ts_s_b[stat_type] = 0.0
                        self._ts_b[stat_type] = 0.0

            # fill in the ndof too
            self.get_ndof(stat_type)
            
        # if this is a measurement where we always use the sm theory as background, copy the test stats over.
        if cdb.theoryComp(self.tags):
            if self._singleBin:
                self._test_stats[cfg.databg] = self._test_stats[cfg.smbg]
            else:
                self._ts_s_b[cfg.databg] = self._ts_s_b[cfg.smbg]
                self._ts_b[cfg.databg] = self._ts_b[cfg.smbg]
                
    def __buildBGCov(self):
        """
        Internal function to build theory background covariance matrices.
        """

        if self.sm_values is None:
            return # will cause test stats to be None for smbg and expected stat types

#        cfg.contur_log.debug("MEAS uncertainty: {}".format(np.sqrt(np.diag(self.measured_values.covariance_matrix))))
#        cfg.contur_log.debug("SM uncertainty: {}".format(np.sqrt(np.diag(self.sm_values.diagonal_matrix))))

        
        if cfg.useTheoryCorr and self.sm_values.covariance_matrix is not None and len(self.sm_values.err_breakdown) >= cfg.min_num_sys_sm:
            if self.measured_values.covariance_matrix is not None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys:
                self._covariances["B1"] = self.measured_values.covariance_matrix+self.sm_values.covariance_matrix+self._statCov
                self._covariances["B2"] = self.measured_values.covariance_matrix+self.sm_values.covariance_matrix
                cfg.contur_log.debug("using theory correlations")
            else:
                try:
                    # we don't have valid data correlations, so add uncorrelated theory uncertainties.
                    self._covariances["B1"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix+self._statCov
                    self._covariances["B2"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix
                    cfg.contur_log.debug("not using theory correlations")
                except:
                    raise cfg.ConturError("Could not figure out how to combine theory and refdata uncertainties for {}".format(self._tags))

        elif self.sm_values.diagonal_matrix is not None:
            cfg.contur_log.debug("not using theory correlations")
            if self.measured_values.covariance_matrix is not None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys:
                # we aren't using theory correlations, but we do have data correlations.
                self._covariances["B1"] = self.measured_values.covariance_matrix+self.sm_values.diagonal_matrix+self._statCov
                self._covariances["B2"] = self.measured_values.covariance_matrix+self.sm_values.diagonal_matrix
            else:
                # we don't have data correlations or theory correlations, use diagonal matrices.
                try:
                    self._covariances["B1"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix+self._statCov
                    self._covariances["B2"] = self.measured_values.diagonal_matrix+self.sm_values.diagonal_matrix
                except:
                    raise cfg.ConturError("Could not figure out how to combine theory and refdata uncertainties for {}".format(self._tags))


        self._inverses["B1"] = la.inv(self._covariances["B1"])
        self._inverses["B2"] = la.inv(self._covariances["B2"])

        self._covariances["C1"] = self._covariances["B1"]
        self._inverses["C1"]    = self._inverses["B1"]
        self._covariances["C2"] = self._covariances["B2"]
        self._inverses["C2"]    = self._inverses["B2"]


        
    def __buildCovinv(self):
        """Internal function to take the covariance matrix and invert it for the chi square test

        In building the Cov matrix we note three cases
            * The matrix is built, and has det!=0, the variables have been built with a covariance that makes sense 
              and the nusiances can be correlated accordingly

            * The matrix has det==0, so we use the diagonal version of it, ignoring correlations
              
            * The diagonalised matrix also has det==0, this means one of the diagonals has 0 uncertainty, this bin should be 
              removed from HEPData. It is considered pathological so the whole entry is discarded

        We build several separate inverse matrices. 
        A- the "data=background" mode, where the non-signal uncertainties are those of the measurement
        B- the "SM=background" mode, where the SM background uncertainties and measurement uncertainties are both included
        C- the "expected limits" mode, where the matrix is identical to B.

        In each case we build two matrices, with the signal+background (1) and background only (2) covariance matrices for each case. 
        The former contains the uncertainties on the signal (MC stats and expected stats given the integrated lumi), the latter do not.
        
        So... six matrices built in total, but only four distinct ones since B1=C1 and B2=C2.

        """

        # Calculate the  covariance matrix for the signal. This is assumed uncorrelated
        # and so is diagonal (the signal errors are the stat errors from the MC generation
        # and the expected signal stat uncertainty from integrated lumi and cross section.
        # (If there are no BSM values, this means we are doing a SM-only test.)
        if self.bsm_values is not None:
            self._statCov = np.diag(self.bsm_values.err_breakdown**2)
        else:
            try:
                self._statCov = np.diag(np.zeros(self._nbins))
            except:
                cfg.contur_log.error("No bin number for this histo. Is your yoda file ok? {}.".format(self._tags))
                raise

            
        # If we have a covariance matrix, it has enough error sources, and the user has not turned off correlations, then use it.
        if self.measured_values.covariance_matrix is not None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys and not cfg.diag :
            try:                
                self._covariances["A1"] = self.measured_values.covariance_matrix + self._statCov
                self._covariances["A2"] = self.measured_values.covariance_matrix                
                self._inverses["A1"] = la.inv(self._covariances["A1"])
                self._inverses["A2"] = la.inv(self._covariances["A2"])
                #cfg.contur_log.debug("A1 {}".format(self._covariances["A1"]))

            except:
                cfg.contur_log.warning("Could not invert covariance matrices for: {}. Will diagonalise.".format(self._tags))
                # TODO: according to the logic described above, we should try the diagonal version
                self._covariances["A1"] = self.measured_values.diagonal_matrix + self._statCov
                self._covariances["A2"] = self.measured_values.diagonal_matrix                
                self._inverses["A1"] = la.inv(self._covariances["A1"])
                self._inverses["A2"] = la.inv(self._covariances["A2"])
                
        elif self.measured_values.diagonal_matrix is not None:

            cfg.contur_log.debug("Not using off-diagonal correlations. Flag is {}.".format(cfg.diag))

            self._covariances["A1"] = np.diag(self.measured_values.diagonal_matrix + self._statCov)
            self._covariances["A2"] = np.diag(self.measured_values.diagonal_matrix)

            # this is diagonal anyway so do quicker & more reliably
            if np.count_nonzero(self._covariances["A1"]) == len(self._covariances["A1"]):
                self._inverses["A1"] = np.diag(1.0 / (self._covariances["A1"]))
            else:
                cfg.contur_log.warning(
                    self._tags + " has at least one element with zero uncertainty. Can't invert. Data discarded.")
            
            if np.count_nonzero(self._covariances["A2"]) == len(self._covariances["A2"]):
                self._inverses["A2"] = np.diag(1.0 / (self._covariances["A2"]))
            else:
                cfg.contur_log.warning(
                    self._tags + " has at least one element with zero uncertainty. Can't invert. Data discarded.")

            # if errors are requested uncorrelated and the other criteria fail, use single bin method
            # otherwise, will use the diagonal matrix.
            if cfg.diag and not (self.measured_values.covariance_matrix is not
                                 None and len(self.measured_values.err_breakdown) >= cfg.min_num_sys):
                cfg.contur_log.debug("Using single bin method.")
                self._singleBin = True
            else:
                cfg.contur_log.debug("Using diagonal correlation matrix.")
                #cfg.contur_log.debug("A1 {}".format(self._covariances["A1"]))
                self._singleBin = False
        else:
            cfg.contur_log.warning(
                "Couldn't invert covariance matrix for " + self._tags + ". Data discarded.")

        # build the SM background/expected limit cases
        self.__buildBGCov()

            
    def __chisq(self, stat_type, mu_test, mu_null):
        """Internal function to calculate a pair of chi square test statistics corresponding to two input hypothesis values.

        :arg mu_test:
            The signal strength to test
        :type mu_test: ``float``
        :arg mu_null:
            The signal strength in the null hypothesis. If this is None, is is the same as being zero, unless
            we are minimising nuisance parameters, in which case None just saves some time.
        :type mu_null: ``float``
        
        :Requirements:
            * :func:`self.__buildCovinv` runs and populated `_covinv` and `_covBuilt` exist

        :return: (ts_tested,ts_null) ``float`` -- Returns a tuple of the test statistics corresponding to the requested signal strength parameters

        """


        # load the correct matrices.
        try:
            if stat_type==cfg.expected:
                covinv = self._inverses["C1"]
                covinv_bg_only = self._inverses["C2"]
                meas = self.expected_values.central_values
                bg = self.expected_values.central_values
            elif stat_type==cfg.hlexpected:
                if (cdb.get_pool(path=self._tags).beamid)=='13TeV':
                    sf = cfg.hllhc_intl_fb/self._lumi_fb
                else:
                    sf=1.0
                covinv = self._inverses["C1"]*sf
                covinv_bg_only = self._inverses["C2"]*sf
                meas = self.expected_values.central_values
                bg = self.expected_values.central_values
            elif stat_type==cfg.smbg:
                covinv = self._inverses["B1"]
                covinv_bg_only = self._inverses["B2"]
                bg = self.sm_values.central_values
                meas = self.measured_values.central_values
            elif stat_type==cfg.databg:
                covinv = self._inverses["A1"]
                covinv_bg_only = self._inverses["A2"]
                bg = self.measured_values.central_values
                meas = self.measured_values.central_values
            else:
                cfg.contur_log.warn("Unknown stat type {}".format(stat_type))
                return None, None

        except (KeyError, AttributeError):
            # This just means there wasn't info supplied for the requested stat type.
            return None, None

        if covinv is None:
            return None, None
            
        if self.bsm_values is not None:
            signal = self.bsm_values.central_values
        else:
            # this is when we're doing SM test.
            signal = np.zeros(len(meas))

        ## Handle different data types in addition to "normal" stacked histograms
        if self.ratio or cfg.sig_plus_bg:
            # First case: ratio plot.
            #   In general, a histogram ratio will be like (A_bkg + A_sig) / (B_bkg + B_sig), and can't be combined without RAW info
            #   Depending on the rivet analysis, this implementation may specific to ratios where the
            #   BSM enters the numerator only

            # Second case sig_plus_bg is set. This means the input histograms are SM plus BSM, not just the BSM.

            # The covariances use will already be fine, as long as the signal uncertainties only include
            # the uncertainties on the BSM part. Otherwise the SM uncertainties will be double-counted

            delta_mu_test = signal - meas  #< assumed mu_test = 1
            delta_mu_null = bg - meas      #< assumed mu_null = 0
        elif self.profile:
            # We use the SM cross-section from the database, the signal cross-section
            # read from YODA, and compute the new weighted mean
            assert self._bxsec is not None
            # Weighting fractions, assuming signal contribution with mu = 1
            # TODO: generalise to weightings with mu_test/null != {0,1}
            f_bkg = self._bxsec / (self._sxsec + self._bxsec)
            f_sig = self._sxsec / (self._sxsec + self._bxsec)
            # Deltas 
            # TODO: also update the covariance for the weighting?
            delta_mu_null = bg - meas
            delta_mu_test = (f_sig*signal + f_bkg*bg) - meas
            #print("***", self._bxsec, self._sxsec, f_bkg, f_sig, delta_mu_null, delta_mu_test)
        else:
            # The 'normal' situation where the delta is the sum of (mu*s + b + Delta) - data
            delta_mu_test = (mu_test * signal + bg) - meas
            if mu_null is not None:
                delta_mu_null = (mu_null * signal + bg) - meas
            else:
                delta_mu_null = np.zeros(len(meas))

        #cfg.contur_log.debug("delta for {} signal: {}".format(self._tags,delta_mu_test))
        #cfg.contur_log.debug("uncertainty: {}".format(1.0/np.sqrt(np.diag(covinv))))
        cfg.contur_log.debug("sig, bg, meas for {},{} signal: {} bg: {} meas:{}".format(self._tags,stat_type,signal,bg,meas))
        
        if self._singleBin:
            # do some magic to find the max single, and removing those where the BSM agrees better than SM
            ts_ts = zip([(x ** 2) * y for x, y in zip(delta_mu_test, np.diag(covinv))],
                        [(x ** 2) * y for x, y in zip(delta_mu_null, np.diag(covinv_bg_only))])
            cls_input = []
            for x, y in ts_ts:
                if y>x:
                    cls_input.append([0,0])
                else:
                    cls_input.append([x,y])
            return cls_input

        else:
            return (np.dot(delta_mu_test, np.dot(covinv, delta_mu_test)),
                    np.dot(delta_mu_null, np.dot(covinv_bg_only, delta_mu_null)))

    def build_spey_models(self):
        """
        Function to build an Spey statistical models for hypothesis testing.
        For each stat type, the model constructed is a multivariate Gaussian with one parameter, the signal strength.
        """

        import spey
        np.seterr(under='ignore', over='ignore')

        if self.ratio:
            cfg.contur_log.warning('Spey model not implemented for ratio plots, no models built for {}.'.format(self._tags))
            return


        if self.bsm_values is not None:
            signal = self.bsm_values.central_values
        else:
            # this is when we're doing SM test.
            signal = np.zeros(len(self.measured_values.central_values))

        for stat_type in cfg.stat_types:
            try:
                if stat_type==cfg.expected:
                    cov = self._covariances["C1"]
                    meas = self.expected_values.central_values
                    bg = self.expected_values.central_values
                elif stat_type==cfg.hlexpected:
                    if (cdb.get_pool(path=self._tags).beamid)=='13TeV':
                        sf = cfg.hllhc_intl_fb/self._lumi_fb
                    else:
                        sf=1.0
                    cov = self._covariances["C1"]/sf
                    meas = self.expected_values.central_values
                    bg = self.expected_values.central_values
                elif stat_type==cfg.smbg:
                    cov = self._covariances["B1"]
                    bg = self.sm_values.central_values
                    meas = self.measured_values.central_values
                elif stat_type==cfg.databg:
                    cov = self._covariances["A1"]
                    bg = self.measured_values.central_values
                    meas = self.measured_values.central_values
            except KeyError:
                cfg.contur_log.debug('Data missing for {}, stat type {}. Spey model not built.'.format(self._tags,stat_type))
                continue

            # spey needs 2D matrices
            if cov.ndim ==1:
                cov = np.diag(cov)

            
            if self._singleBin:
                # build a Gaussian distribution for each bin
                one_bin_wrapper = spey.get_backend('default.normal')
                uncertainties = np.sqrt(np.diag(cov))
                for bin_num, sig_bin, bg_bin, meas_bin, unc_bin in enumerate(zip(signal,bg,meas, uncertainties)):
                    model = one_bin_wrapper(
                        signal_yields = sig_bin,
                        background_yields = bg_bin,
                        data = meas_bin,
                        absolute_uncertainties=unc_bin,
                        analysis=self._tags+"/bin"+str(bin_num)
                    )
                    self.spey_model_list[stat_type].append(model)

            elif cfg.sig_plus_bg:
                raise NotImplementedError('Spey calculation for --signal-plus-background mode not currently implemented')
            elif self.profile:
                raise NotImplementedError('Spey profiling calculation not currently implemented')
            
            # 'normal' histogram is a multivariate Gaussian
            else:
                pdf_wrapper = spey.get_backend('default.multivariate_normal')

                self.spey_model[stat_type] = pdf_wrapper(
                    signal_yields=signal,
                    background_yields=bg,
                    data=meas,
                    covariance_matrix=cov,
                    analysis=self._tags
                )
            
    def spey_calculate_CLs(self,stat_type):
        """
        Use the statistical model to calculate the CLs exclusion.
        This is calculated from the profile likelihood ratio
        """
        try:
            model = self.spey_model[stat_type]
        except KeyError:
            return None
        
        try:
            CLs = model.exclusion_confidence_level(calculator='chi_square')[0]
            
        except (FloatingPointError,np.linalg.LinAlgError) as ex:
            
            cfg.contur_log.warning("Exception caught during spey CLs calc for {} stat type {}: {}".format(self._tags,stat_type,ex))
            cfg.contur_log.debug("The model type used was {}".format(type(model)))
            CLs = None
        
        return CLs
    
    def calculate_max_mu(self,stat_type):
        """
        Calculate the 95% CLs upper limit on the signal strength parameter mu.
        """
        if not cfg.use_spey:
            raise cfg.ConturError("Spey mode required to set upper limit on signal strength parameter")
        
        try:
            model = self.spey_model[stat_type]
        except KeyError:
            return None
        
        try:
            mu_upper_limit = model.chi2_test(limit_type='right')[0]
            
        except (FloatingPointError,np.linalg.LinAlgError) as ex:
            cfg.contur_log.warning("Exception caught during spey mu upper limit calc for {} stat type {}: {}".format(self._tags,stat_type,ex))
            #cfg.contur_log.warning("The model type used was {}".format(type(model)))
            #cfg.contur_log.warning("A: {}, {}".format(self._inverses["A1"],self._inverses["A2"]))
            #cfg.contur_log.warning("B: {}, {}".format(self._inverses["B1"],self._inverses["B2"]))
            #cfg.contur_log.warning("C: {}, {}".format(self._inverses["C1"],self._inverses["C2"]))
            mu_upper_limit = None
        
        return mu_upper_limit

    def calculate_mu_hat(self,stat_type):
        """
        Calculate maximum likelihood estimator of the signal strength parameter, mu_hat.
        """
        if not cfg.use_spey:
            raise cfg.ConturError("Spey mode required to set maximise likelihood.")
        
        try:
            model = self.spey_model[stat_type]
        except KeyError:
            return None
        
        try:
            mu_hat = model.maximize_likelihood(allow_negative_signal=True)[0]
            
        except (FloatingPointError,np.linalg.LinAlgError) as ex:
            cfg.contur_log.warning("Exception caught during spey muhat calc for {} stat type {}: {}".format(self._tags,stat_type,ex))
            cfg.contur_log.debug("The model type used was {}".format(type(model)))
            mu_hat = None
        
        return mu_hat

    def find_dominant_bin(self, stat_type):
        """
        Function to find the bin that gives the highest CLs for cases with no covariance matrix 
        (either the matrix has no invserse or has not been succesfully built)
        """
        # skip cases where we've built the covariance matrix
        if not self._singleBin:
            return

        if cfg.use_spey:
            # if in single bin mode, should have built a list of Gaussian models
            try:
                models = self.spey_model_list[stat_type]
            except KeyError:
                cfg.contur_log.debug('No single bin models for {}, stat type {}'.format(self._tags,stat_type))
                return
            if not isinstance(models,list):
                cfg.contur_log.error('Using single bin method for {}, should have a list of spey models but instead have {}'.format(self._tags,type(models)))
            
            # find the model that gives the best CLs
            max_CLs = 0.0
            for model in models:
                CLs = model.exclusion_confidence_level(poi_test=1.0,calculator='chi-square')[0]
                
                if CLs > max_CLs:
                    self.spey_model[stat_type] = model
                    max_CLs = CLs
        else:
            if stat_type not in self._test_stats:
                cfg.contur_log.debug('No test stats built for {}, stat_type {}, not finding dominant bin'.format(self._tags,stat_type))
                return

            try:
                test_stats_s_b, test_stats_b = zip(*self._test_stats[stat_type])
            except TypeError:
                cfg.contur_log.debug('Test stats are None for {} stat type {}, not finding dominant bin'.format(self._tags,stat_type))
                return

            max_CLs = 0.0
            for ts_s_b, ts_b in zip(test_stats_s_b,test_stats_b):
                CLs = ts_to_cls((ts_s_b,ts_b),self._tags)[0]

                if CLs > max_CLs: # use the largest CLs bin
                    self._ts_s_b[stat_type] = ts_s_b
                    self._ts_b[stat_type] = ts_b
                    max_CLs = CLs

    def cleanup_model_list(self):
        """
        Delete the single bin models, this can be done after the bin with the highest exclusion power is found
        """
        del self.spey_model_list

    def calculate(self,stat_type):
        """
        Default mode: Calculates the CLs exclusion for this histogram (and this stat type)

        Spey mode: Calculates several statistics using the spey statistical models, namely:
        - CLs exclusion
        - 95% CLs upper limit on the signal strength parameter mu
        - Maximum likelihood estimator of the signal strength parameter, muhat
    
        """
        
        # spey calculations
        if cfg.use_spey:
            self._CLs[stat_type] = self.spey_calculate_CLs(stat_type)
            self._mu_hat[stat_type] = self.calculate_mu_hat(stat_type)

            if self._CLs[stat_type] is not None and self._CLs[stat_type] > 0.0:
                self._mu_upper_limit[stat_type] = self.calculate_max_mu(stat_type)
            else:
                cfg.contur_log.debug("({}) No exclusion for {}, no upper limit on mu.".format(stat_type,self._tags))
                self._mu_upper_limit[stat_type] = None

        # default CLs calc
        else:
            # don't calculate CLs if there are no signal events, unless doing SM test
            if not (self.bsm_values.central_values.any() or self.bsm_values is None):

                # catch two special cases
                if  (((stat_type == cfg.smbg or stat_type == cfg.expected or stat_type == cfg.hlexpected) and self.sm_values is not None) or (stat_type == cfg.databg)):
                    # this should be zero if
                    # (i) there was a theory projection we would use, but there were no signal events or
                    # (ii) we were using data as background and there were no signal events.            
                    self._pval[stat_type] = 0.0
                    self._CLs[stat_type] = 0.0
                return

            if stat_type not in self._ts_s_b or stat_type not in self._ts_b:
                return # don't have test stats for this stat type
            
            if self._ts_s_b[stat_type] is not None and self._ts_b[stat_type] is not None:
                if  self._ts_s_b[stat_type] < 0.0:
                    cfg.contur_log.warning("ts_s_b = {} for {}. Setting to zero.".format(self._ts_s_b[stat_type],self._tags))
                    self._ts_s_b[stat_type] = 0.0
                if self._ts_b[stat_type] < 0.0:
                    cfg.contur_log.warning("ts_b = {} for {}. Setting to zero.".format(self._ts_b[stat_type],self._tags))
                    self._ts_b[stat_type] = 0.0

                # actually calculate the CLs
                self._CLs[stat_type] = ts_to_cls((self._ts_s_b[stat_type],self._ts_b[stat_type]),self._tags)[0]
            else:
                self._CLs[stat_type] = None


        if self._CLs[stat_type] is not None:
            self._pval[stat_type] = 1.0 - self._CLs[stat_type]
                
            if np.isnan(self._CLs[stat_type]):
                    self._CLs[stat_type] = None
                    cfg.contur_log.warning(
                        "CLs {} evaluated to nan, set to None. {} ".format(stat_type,self._tags))
         
        else: # CLs is None
            self._pval[stat_type] = None

            if stat_type == cfg.databg and self.sm_values is None:
                # warn, unless this is a measurement without SM theory and and that was required, in which
                # case it's normal.
                cfg.contur_log.warning("Could not evaluate CLs for {}, type {}".format(self._tags, stat_type))

        if cfg.use_spey:
            cfg.contur_log.debug("Reporting CLs {}, pval {} for {}, stat type {}:".format(self._CLs[stat_type], self._pval[stat_type], self._tags, stat_type))
        else:
            cfg.contur_log.debug("Reporting CLs {}, pval {}, ts_s_b {}, ts_b {} for {}:".format(self._CLs[stat_type], self._pval[stat_type], self._ts_s_b[stat_type], self._ts_b[stat_type], self._tags))

    @property
    def tags(self):
        """Name(s) of source histograms for this block

        *settable parameter*

        **type** (``string``)
        """
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def pools(self):
        """Pool that the test belongs to

        *settable parameter*

        **type** (``string``)
        """
        return self._pools

    @pools.setter
    def pools(self, value):
        self._pools = value

    @property
    def subpools(self):
        """Subpool the test belongs to

        *settable parameter*

        **type** (``string``)
        """
        return self._subpools

    @subpools.setter
    def subpools(self, value):
        self._subpools = value


    def getCLs(self,type):
        """
        CLs hypothesis test value (ratio of `p_s_b` and `p_b`)

        **type** (``float``)

        """
        try:
            CLs = self._CLs[type] 
        except KeyError:
            CLs = None
        return CLs
    
    def get_mu_upper_limit(self,type):
        """
        Upper limit on the signal strength parameter mu at 95% CLs

        **type** (``float``)

        """
        try:
            mu_upper_limit = self._mu_upper_limit[type] 
        except KeyError:
            mu_upper_limit = None
        return mu_upper_limit
    
    def get_mu_hat(self,type):
        """
        Maximum likelihood estimator of the signal strength parameter.

        **type** (``float``)

        """
        try:
            mu_hat = self._mu_hat[type] 
        except KeyError:
            mu_hat = None
        return mu_hat

    def get_ts_s_b(self,type):
        """Test statistic of the s+b hypothesis

        **type** (``float``)
        """
        try:
            ts_s_b = self._ts_s_b[type] 
        except KeyError:
            #raise cfg.ConturError("Asked for test statistic of type {} but it does not exist.".format(type))
            ts_s_b = None
        except:
            ts_s_b = self._ts_s_b

        return ts_s_b

    def get_ts_b(self,type):
        """Test statistic of b only hypothesis

        **type** (``float``)
        """
        try:
            ts_b = self._ts_b[type] 
        except KeyError:
            ts_b = None
            #            raise cfg.ConturError("Asked for test statistic of type {} but it does not exist.".format(type))
        except:
            ts_b = self._ts_b

        return ts_b

    def set_ts_b(self,type,value):
        self._ts_b[type]=value

    def set_ts_s_b(self,type,value):
        self._ts_s_b[type]=value

    def get_ndof(self,type):
        """
        estimate numbers of degree of freedom for this plot
        """
        
        try:
            return self._ndof[type]
        except KeyError:
            # calculate it            
            ndof = 0
            i = 0
            if type==cfg.smbg:
                try:
                    matrix = self._covariances["B1"]
                except KeyError:
                    self._ndof[type] = None
                    return None
            elif type==cfg.databg:
                try:
                    matrix = self._covariances["A1"]
                except KeyError:
                    self._ndof[type] = None
                    return None
            elif type==cfg.expected or type==cfg.hlexpected:
                try:
                    matrix = self._covariances["C1"]
                except KeyError:
                    self._ndof[type] = None
                    return None
            else:
                raise cfg.ConturError("unknown type in ndof request {}".format(type))
                               
#            for i in range(0,len(matrix)):
#                rsum = sum(matrix[i])
#                ndof = ndof + matrix[i][i]/rsum
            
#            self._ndof[type]=ndof
            self._ndof[type]=len(matrix)
            ndof = len(matrix)
            #print(self._ndof[type])
            return ndof

    def get_sm_pval(self):
        """
        Calculate the pvalue compatibility (using chi2 survival) for the SM prediction and this
        measurement
        """        
        try:
            ts = self.get_ts_b(cfg.smbg)
            ndof = self.get_ndof(cfg.smbg)
            #print(ts,ndof)
            self._sm_pval = np.exp(spstat.chi2.logsf(ts,ndof))
            #print("PVAL:",self._sm_pval)
            return self._sm_pval
        except:
            return None
        
    def __repr__(self):
        if not self.tags:
            tag = "Combined blocks"
        else:
            tag = self.pools + self.tags

        if cfg.use_spey:
            spey_CLs = "Spey CLs:"
            for stat_type in cfg.stat_types:
                spey_CLs = spey_CLs + "{} ({}); ".format(self.getCLs(stat_type),stat_type)

            return "{} from {}, {}".format(self.__class__.__name__, tag, spey_CLs)

        ts_vals = "Test stat values:"
        for stat_type in cfg.stat_types:
            ts_vals = ts_vals + "{} ({}); ".format(self.get_ts_s_b(stat_type),stat_type)
            
        return "{} from {}, {}".format(self.__class__.__name__, tag, ts_vals)


class CombinedLikelihood(Likelihood):
    """
    Shell to combine :class:`~contur.factories.likelihood.Likelihood` blocks

    This class is used to extract the relevant test statistic from each individual :class:`~contur.factories.likelihood.Likelihood` and combine them
    This is initialised with no arguments as it is just a shell to combine the individual components, and automatically encodes the fact that
    each block is uncorrelated with each other

    Two use cases: 
    1. Combining subpool likelihoods, where statistics are combined for all stat types.

    2. Building the full likelihood, which is done separately for each stat type. 
    This is because different histograms can provide the best exclusion in a pool 
    depending on the stat type.

    .. note:: Technically this could be constructed by building a :class:`~contur.factories.likelihood.Likelihood` with a master covariance matrix made forming block diagonals with each individual component. Avoiding this is faster but less rigourous

    """

    def __init__(self,stat_type="all"):
        super(self.__class__, self).__init__()

        if stat_type == "all": # subpool
            self.stat_types=cfg.stat_types
        elif stat_type in cfg.stat_types: # full likelihood
            self.stat_types=[stat_type]
        else:
            raise ValueError("Invalid stat type {} passed to CombinedLikelihood.".format(stat_type))

        
    def calc_cls(self):
        """Call the calculation of the CLs confidence interval

        Triggers the parent class calculation of the CLs interval based on the sum of test statistics added with the :func:`add_likelihood` method

        """

        for stat_type in self.stat_types:

            if cfg.use_spey:
                self.calculate(stat_type)

            else:
                try:
                    self._CLs[stat_type] = ts_to_cls([(self._ts_s_b[stat_type], self._ts_b[stat_type])],self._tags)[0]
                except (TypeError, KeyError):
                    self._CLs[stat_type] = None

    def add_likelihood(self, likelihood):
        """Add a :class:`~contur.factories.likelihood.Likelihood` block to this combination likelihood

        :arg likelihood: Instance of computed Likelihood
        :type likelihood: :class:`~contur.factories.likelihood.Likelihood`
        """
        cfg.contur_log.debug('Calling add_likelihood on {}'.format(self))
        cfg.contur_log.debug('Adding this on {}'.format(likelihood))
        for stat_type in self.stat_types:     
            cfg.contur_log.debug('Attempting to add for stat type {}'.format(stat_type))
            try:      
                if cfg.use_spey:
                    # don't add models that give no exclusion
                    if likelihood.getCLs(stat_type) is None:
                        cfg.contur_log.debug('No Exclusion, continuing')
                        continue
                    
                    # adding first likelihood block for this stat type
                    if stat_type not in self.spey_model_list.keys():
                        if isinstance(likelihood,CombinedLikelihood): # adding a subpool
                            self.spey_model_list[stat_type] = list(likelihood.spey_model_list[stat_type])

                        else:
                            self.spey_model_list[stat_type] = [likelihood.spey_model[stat_type]]

                    # not the first likelihood block for this stat type
                    else:
                        if isinstance(likelihood,CombinedLikelihood): # adding a subpool
                            self.spey_model_list[stat_type].extend(likelihood.spey_model_list[stat_type])
                        else:
                            self.spey_model_list[stat_type].append(likelihood.spey_model[stat_type])

                # normal test stat addition
                else:
                    # adding first likelihood block for this stat type
                    if stat_type not in self._ts_s_b.keys() and stat_type not in self._ts_b.keys():
                        self._ts_s_b[stat_type] = likelihood._ts_s_b[stat_type]
                        self._ts_b[stat_type] = likelihood._ts_b[stat_type]
                        self._ndof[stat_type] = likelihood._ndof[stat_type]

                    elif likelihood._ts_b[stat_type] is not None and likelihood._ts_s_b[stat_type] is not None:
                        self._ts_s_b[stat_type] += likelihood._ts_s_b[stat_type]
                        self._ts_b[stat_type] += likelihood._ts_b[stat_type]
                        self._ndof[stat_type] += likelihood._ndof[stat_type]

            except KeyError: 
                cfg.contur_log.debug('Caught an exception, moving on.....')
                # this is ok, just means there was no signal for this histo for this test stat.
                # TODO: handle the combinations here when we mix SM and Data, for example.
                continue
            
            cfg.contur_log.debug("Added {} to {}, using {}.".format(likelihood,self,stat_type))

    def combine_spey_models(self):
        """
        Combines a list of spey models into a single one.
        Assumes models are statistically uncorrelated
        """
        import spey
        from spey.combiner.uncorrelated_statistics_combiner import UnCorrStatisticsCombiner
        np.seterr(under='ignore', over='ignore')
        
        for stat_type in self.stat_types:
            if stat_type not in self.spey_model_list.keys():
                continue # no models for this stat type
            
            cfg.contur_log.debug('Combining {} models into a single Spey model, stat type {}'.format(len(self.spey_model_list[stat_type]),stat_type))

            try:
                models_copy = copy.deepcopy(self.spey_model_list[stat_type])
                self.spey_model[stat_type] = UnCorrStatisticsCombiner(*models_copy)
                cfg.contur_log.debug('Combined spey models to make this: {}'.format(self.spey_model[stat_type]))

                # make model list immutable
                self.spey_model_list[stat_type] = tuple(self.spey_model_list[stat_type])
            except spey.system.exceptions.AnalysisQueryError as ex:
                all_tags = [model.analysis for model in self.spey_model_list[stat_type]]
                cfg.contur_log.error('Error when combining spey_models: {}, tags in CombinedLikelihood ({}): {}'.format(ex,stat_type,all_tags))

    def getCLs(self,stat_type):
        """
        CLs hypothesis test value (ratio of `p_s_b` and `p_b`)

        **stat_type** (``str``)

        """
        if stat_type not in self.stat_types:
            raise KeyError("Tried to get CLs for stat type {}, which is not in {}".format(stat_type,self.stat_types))
        
        try:
            CLs = self._CLs[stat_type] 
        except KeyError:
            CLs = None
        
        return CLs 
    
    def get_mu_upper_limit(self,stat_type):
        """
        Upper limit on the signal strength parameter mu at 95% CLs

        **type** (``float``)

        """
        if stat_type not in self.stat_types:
            raise KeyError("Tried to get mu upper limit for stat type {}, which is not in {}".format(stat_type,self.stat_types))
        
        try:
            mu_upper_limit = self._mu_upper_limit[stat_type] 
        except KeyError:
            mu_upper_limit = None

        return mu_upper_limit
    
    def get_mu_hat(self,stat_type):
        """
        Maximum likelihood estimator of the signal strength parameter.
        **type** (``float``)

        """
        if stat_type not in self.stat_types:
            raise KeyError("Tried to get mu hat for stat type {}, which is not in {}".format(stat_type,self.stat_types))
        
        try:
            mu_hat = self._mu_hat[stat_type] 
        except KeyError:
            mu_hat = None

        return mu_hat
    
    def get_ts_s_b(self, stat_type):
        """Test statistic of the s+b hypothesis

        **stat_type** (``str``)
        """
        if stat_type not in self.stat_types:
            raise KeyError("Tried to get signal test stat for stat type {}, which is not in {}".format(stat_type,self.stat_types))

        try:
            ts_s_b = self._ts_s_b[stat_type] 
        except KeyError:
            #raise cfg.ConturError("Asked for test statistic of type {} but it does not exist.".format(type))
            ts_s_b = None

        return ts_s_b

    def get_ts_b(self, stat_type):
        """Test statistic of b only hypothesis

        **stat_type** (``str``)
        """
        if stat_type not in self.stat_types:
            raise KeyError("Tried to get signal test stat for stat type {}, which is not in {}".format(stat_type,self.stat_types))

        try:
            ts_b = self._ts_b[stat_type] 
        except KeyError:
            ts_b = None

        return ts_b

    def set_ts_b(self,stat_type, value):
        if stat_type not in self.stat_types:
            raise TypeError("Tried to set signal test stats for stat type {}, which is not in {}".format(stat_type,self.stat_types))
        
        self._ts_b[stat_type]=value

    
#    def setCLs(self,value):
#        self._CLs[self.stat_type]=value

    def __repr__(self):
        if not self.tags:
            tag = "Combined blocks"
        else:
            tag = self.pools + self.tags
        
        if cfg.use_spey:
            CLs = [self.getCLs(stat_type) for stat_type in self.stat_types]
            CLs_str = ", ".join("({}: {})".format(cl,stat) for cl, stat in zip(CLs,self.stat_types))
            return "{} from {}, Spey CLs ".format(self.__class__.__name__, tag)+CLs_str

        else:
            test_stats = [self.get_ts_s_b(stat_type) for stat_type in self.stat_types]
            test_stats_str = ", ".join("({}: {})".format(ts,stat) for ts, stat in zip(test_stats,self.stat_types))
            return "{} from {}, test stats ".format(self.__class__.__name__, tag)+test_stats_str

def pval_to_cls(pval_tuple):
    """
    Function to calculate a cls when passed background and signal p values.

    notes: we are not actually varying a parameter of interest (mu), just checking mu=0 vs mu=1

           the tail we integrate to get a p-value depends on whether you're looking for signal-like or background-like tails. 
           For the signal-like p-value we integrate over all the probability density less signal-like than was observed, i.e. to the right of the observed 
           test stat.

           For the background-like p-value we should integrate over the less background-like stuff, i.e. from -infty to t_obs... which is 1 - the t-obs...infty 
           integral.

           So CLs is the ratio of the two right-going integrals, which is nice and simple and symmetric, but looks asymmetric when written in terms of the 
           p-values because they contain complementary definitions of the integral limits 

           The code has implemented them both as right-going integrals, so does look symmetric, hence this comment to hopefully avoid future confusion.

    :arg pval_tuple: Tuple, first element p-value of signal hypothesis, second p-value of background
    :type pval_tuple: ``Tuple of floats``

    :return: CLs ``float`` -- Confidence Interval in CLs formalism

    """

    # convert to log for numerical stability.
    # this ignore error state means -inf will be passed for log of zero, which can be handled later
    with np.errstate(divide='ignore'):
        log_p_vals = np.log(pval_tuple)
        
    #list to hold computed confidence levels
    cls = []

    for ts_index in range(len(log_p_vals)):
        log_pval_b = log_p_vals[ts_index][1]
        log_pval_sb = log_p_vals[ts_index][0]

        cls_ts_index = 1 - np.exp(log_pval_sb - log_pval_b) #computed confidence level

        cfg.contur_log.debug("pval sb = {}, pval b = {}".format(pval_tuple[ts_index][0],pval_tuple[ts_index][1]))
            

        cfg.contur_log.debug(
                "CLs %e, log pval sb %e, log pval b %e:" % (cls_ts_index, log_pval_sb, log_pval_b))

        if (cls_ts_index is not None and cls_ts_index < 0):
            cfg.contur_log.debug("Negative CLs %f, setting to zero. BSM+SM is in better agreement with data." % (cls_ts_index))
            cls_ts_index = 0

        cls.append(cls_ts_index)

    return cls

def ts_to_pval(ts):
    """
    Method to convert test statistic to log pval

    :arg ts: Single or numpy array of test statistics to convert to a p-values with a Gaussian
    :type ts: ``float`` assuming n DoF=1

    :return: p-value ``float``

    """

    return spstat.norm.logsf(np.sqrt(ts))


def ts_to_cls(ts_tuple_list,tags):
    """
    Method to directly cast a list of tuples of test statistics (tuple 
    contains background and signal test stats) into a list of CLs values

    notes: we are not actually varying a parameter of interest (mu), just checking mu=0 vs mu=1

           the tail we integrate to get a p-value depends on whether you're looking for signal-like or background-like tails. 
           For the signal-like p-value we integrate over all the probability density less signal-like than was observed, i.e. to the right of the observed 
           test stat.

           For the background-like p-value we should integrate over the less background-like stuff, i.e. from -infty to t_obs... which is 1 - the t-obs...infty 
           integral.

           So CLs is the ratio of the two right-going integrals, which is nice and simple and symmetric, but looks asymmetric when written in terms of the 
           p-values because they contain complementary definitions of the integral limits 

           The code has implemented them both as right-going integrals, so does look symmetric, hence this comment to hopefully avoid future confusion.

    :arg ts_tuple_list: list of tuples of tests statistics (tuples of the form (test stat background, test stat background))
    :type ts_tuple_list: ``list``

    :return: CLs ``list`` -- List of Confidence Intervals in CLs formalism

    """
    if type(ts_tuple_list) == tuple:
        ts_tuple_list = [ts_tuple_list] #place in list

    log_p_vals = ts_to_pval(np.array(ts_tuple_list))
    cls = []

    for ts_index in range(len(log_p_vals)):
        log_pval_b = log_p_vals[ts_index][1]
        log_pval_sb = log_p_vals[ts_index][0]

        try:
            # have stayed with logs for as long as possible for numerical stability
            cls_ts_index = 1 - np.exp(log_pval_sb - log_pval_b)
        except FloatingPointError:
            cls_ts_index = 1
        cfg.contur_log.debug(
            "CLs %e, log pval sb %e, log pval b %e:" % (cls_ts_index, log_pval_sb, log_pval_b))

        if (cls_ts_index is not None and cls_ts_index < 0):
            cfg.contur_log.debug(
                "Negative CLs %f, setting to zero for %s. BSM+SM is in better agreement with data." % (cls_ts_index, tags))
            cls_ts_index = 0

        cls.append(cls_ts_index)


    return cls

def sort_blocks(likelihood_blocks, stat_type, omitted_pools= ""):
    """Function that sorts the list of likelihood blocks extracted from the ``YODA`` file

    This function implements the sorting algorithm to sort the list of all extracted :class:`~contur.factories.likelihood.Likelihood`
    blocks in the :attr:`likelihood_blocks` list, storing the reduced list in the :attr:`sorted_blocks` list

    :Keyword Arguments:
        * *stat_type* (``string``) --
          Which statisic (default, smbg, expected, hlexpected) to sort on.
    """
    cfg.contur_log.debug('Calling sort blocks')
    cfg.contur_log.debug('Initial number of blocks: {}'.format(len(likelihood_blocks)))

    # build the list of analysis pool which are represented in these likelihood blocks
    pools = []
    [pools.append(x) for x in [
        item.pools for item in likelihood_blocks] if x not in pools]
    cfg.contur_log.debug('Number of pools in these blocks: {}'.format(len(pools)))

    if likelihood_blocks is None or len(likelihood_blocks) == 0:
        raise ValueError('List of likelihood blocks passed is empty, the likelihood blocks list must contain at least one likelihood object')

    max_likelihood_per_pool = {}

    for likelihood in likelihood_blocks:
        if likelihood.pools in omitted_pools:
            continue

        CLs = likelihood.getCLs(stat_type)
        if CLs is None:
            continue

        # first entry in pool
        if likelihood.pools not in max_likelihood_per_pool.keys():
            max_likelihood_per_pool[likelihood.pools] = likelihood
            continue
            
        # replace the likelihood for the pool if we find a higher one
        if max_likelihood_per_pool[likelihood.pools].getCLs(stat_type) < CLs:
            max_likelihood_per_pool[likelihood.pools] = likelihood

    sorted_blocks = list(max_likelihood_per_pool.values())

    # check tags are unique (i.e no histo is appearing in two pools)
    tags = [l._tags for l in sorted_blocks]
    if len(tags) != len(set(tags)):
        raise cfg.ConturError("After sorting, found the same tag in more than one pool")
    
    cfg.contur_log.debug('Number of pools in the sorted blocks: {}'.format(len(max_likelihood_per_pool)))
    cfg.contur_log.debug('Difference in pools {}'.format(set(pools)-set(list(max_likelihood_per_pool.keys()))))

    return sorted_blocks

def combine_subpool_likelihoods(likelihood_blocks):
    """
    build combined likelihoods for any active subpools, and add them to the list of likelihood blocks.

    """

    # build the list of analysis pool which are represented in these likelihood blocks
    pools = []
    subpool_lh = []
    [pools.append(x) for x in [
        item.pools for item in likelihood_blocks] if x not in pools]

    #now loop over these pools
    for p in pools:

        # build the list of analyses associated with this pool
        anas = []
        [anas.append(x) for x in
         [cfg.ANALYSIS.search(item.tags).group() for item in likelihood_blocks if
          item.tags and item.pools == p] if
         x not in anas]

        for a in anas:
            subpools = []
            for item in likelihood_blocks:
                if item.pools == p and a in item.tags:
                    if item.subpools not in subpools and item.subpools is not None:
                        subpools.append(item.subpools)

            if len(subpools) > 0:
                result = {}
                for sp in subpools:
                    result[sp] = CombinedLikelihood()

                cfg.contur_log.debug('List of subpools for pool {}, analysis {}: {}'.format(p,a,result.keys()))
                for k, v in result.items():
                    cfg.contur_log.debug(f"building subpool {k} ")
                    # Remove the point if it ends up in a group
                    # Tags need to store which histo contribute to this point.
                    for y in likelihood_blocks:
                        if y.subpools == k and a in y.tags:
                            result[k].add_likelihood(y)
                            if len(result[k].tags) > 0:
                                result[k].tags += ","
                            result[k].tags += y.tags

                    if cfg.use_spey:
                        v.combine_spey_models()

                    cfg.contur_log.debug(f'Calculating subpool combined CLs for {v}')
                    v.calc_cls()
                    v.pools = p
                    v.tags = result[k].tags

                # add the max subpool back into the list of points with the pool tag set but no subpool
                [subpool_lh.append(v) for k, v in result.items()]  
#                [likelihood_blocks.append(v) for k, v in result.items()]  

    return subpool_lh

def build_full_likelihood(sorted_blocks, stat_type):
    """
    Function to build the full likelihood representing an entire ``YODA`` file

    This function takes the :attr:`sorted_likelihood_blocks` and combines them as statistically uncorrelated
    diagonal contributions to a :class:`~contur.factories.likelihood.CombinedLikelihood` instance which is stored
    as an attribute to this class as :attr:`likelihood`

    :Keyword Arguments:
        * *stat_type* (``string``) --
          Stat type to build full likelihood for

    """
    cfg.contur_log.debug('Building full likelihood from {} blocks ({}): {}'.format(len(sorted_blocks),stat_type,sorted_blocks))       

    if sorted_blocks is None:
        return None
    
    if len(sorted_blocks) == 0:
        raise ValueError('List of sorted blocks passed is empty, the sorted blocks list must contain at least one likelihood object')

    full_likelihood = CombinedLikelihood(stat_type)
    for x in sorted_blocks:
        full_likelihood.add_likelihood(x)

    if cfg.use_spey:
        full_likelihood.combine_spey_models()

    full_likelihood.calc_cls()
    return full_likelihood

def likelihood_blocks_ts_to_cls(likelihood_blocks,stat_type):
    """Function that calculates the confidence level for each
       likelihood block extracted from the ``YODA`` file using the signal
       and background test statistic for the block
    """
    if len(likelihood_blocks) == 0:
        raise ValueError('List of likelihood blocks passed is empty, the likelihood blocks list must contain at least one likelihood object')

    #Collect test statistics for each likelihood where the background
    test_stats = {}

    for number, likehood_object in enumerate(likelihood_blocks):
        try:
            if likehood_object._ts_s_b[stat_type] is not None:
                tssb = likehood_object._ts_s_b[stat_type]
                tsb = likehood_object._ts_b[stat_type]
                if tssb < 0.0:
                    cfg.contur_log.warning("ts_s_b = {} for {}. Setting to zero.".format(tssb,likehood_object._tags))
                    tssb = 0.0
                if tsb < 0.0:
                    cfg.contur_log.warning("ts_b = {} for {}. Setting to zero.".format(tsb,likehood_object._tags))
                    tsb = 0.0
                test_stats[number] = (likehood_object._ts_s_b[stat_type], likehood_object._ts_b[stat_type])
                test_stats[number] = (tssb,tsb)
                
        except KeyError:
            # this is ok, just means this stat wasn't used for this object
            pass
                
    #Convert test statistics into p values
    test_stat_list = list(test_stats.values())

    try:
        p_values = np.exp(spstat.norm.logsf(np.sqrt(test_stat_list)))
    except FloatingPointError:
        try:
            p_values = np.exp( np.clip(  spstat.norm.logsf(np.sqrt(test_stat_list)) ,-3.0e+02,3.0e-2))
        except FloatingPointError:
            cfg.contur_log.error("Problem getting CLs from ts. min test_stat_list is {}".format(min(test_stat_list)))
            raise
            
    #Loop over each likelihood block, where p value exists evaluate confidence level
    # and update value of the ._CLs attribute for the likelihood block
    count = 0
    for ts_index, like_ob in enumerate(likelihood_blocks):
        if like_ob.bsm_values is None or like_ob.bsm_values.central_values.any():
            #only do the below when we have signal events or are doing SM test

            if ts_index in test_stats.keys():
                p_s_b, p_b = p_values[count]
                count +=1
                like_ob._CLs[stat_type] = pval_to_cls([(p_s_b, p_b)])[0]
                if like_ob._CLs[stat_type] is not None:
                    like_ob._pval[stat_type] = 1.0-like_ob._CLs[stat_type]
            else:
                like_ob._pval[stat_type] = None
                like_ob._CLs[stat_type] = None

            if like_ob._CLs[stat_type] is not None:
                if cfg.contur_log.isEnabledFor(logging.DEBUG):
                    cfg.contur_log.debug("Reporting CLs {}, pval {}, p_sb {}, p_b {}, ts_s_b {}, ts_b {} for {}:".format(
                                           like_ob._CLs[stat_type], like_ob._pval[stat_type], p_s_b, p_b, like_ob._ts_s_b[stat_type], like_ob._ts_b[stat_type], like_ob._tags))

                if np.isnan(like_ob._CLs[stat_type]):
                    like_ob._CLs[stat_type] = None
                    cfg.contur_log.warning(
                        "CLs {} evaluated to nan, set to None. {} ".format(stat_type,like_ob._tags))
            else:
                if stat_type == cfg.databg and like_ob.sm_values is None:
                    # warn, unless this is a measurement without SM theory and and that was required, in which
                    # case it's normal.
                    cfg.contur_log.warning(
                        "Could not evaluate CLs for {}, type {}".format(like_ob._tags, stat_type))


        elif  (((stat_type == cfg.smbg or stat_type == cfg.expected or stat_type == cfg.hlexpected) and like_ob.sm_values is not None) or (stat_type == cfg.databg)):
            # this should be zero if
            # (i) there was a theory projection we would use, but there were no signal events or
            # (ii) we were using data as background and there were no signal events.            
            like_ob._pval[stat_type] = 0.0
            like_ob._CLs[stat_type] = 0.0



            
def likelihood_blocks_find_dominant_ts(likelihood_blocks,stat_type):
    """Function that finds the chi-square test statistic that gives the
       maximum confidence level for each likelihood block for which we
       don't have a valid covariance matrix (either the matrix has no
       invserse or has not been succesfully built)
    """
    if len(likelihood_blocks) == 0:
        raise ValueError('List of likelihood blocks passed is empty, the likelihood blocks list must contain at least one likelihood object')

    #Collect chi-square test statistics for all likelihood for blocks for
    # which ._test_stats is not none, in addition collect index for each
    # block (given by ._tags attribute) and the liklihood object block
    # itself
    chi_test = []
    likelihood_index = []
    like_blocks = {}

    for num, like_ob in enumerate(likelihood_blocks):
        try:
            #        if like_ob._test_stats[stat_type] is not None:
            chi_test = chi_test + like_ob._test_stats[stat_type]
            likelihood_index = likelihood_index + [num]*len(like_ob._test_stats[stat_type])
            like_blocks[num] = like_ob
        except:
            pass
            
    #Convert test stats first to p-value and then confidence level
    try:
        p_values = np.exp(spstat.norm.logsf(np.sqrt(chi_test)))
    except:
        cfg.contur_log.warning("Floating point error in when calculating p_values for {}. Clipping.".format(like_ob._tags))
        p_values = np.exp(np.clip(spstat.norm.logsf(np.sqrt(chi_test)),-3.0e+02,3.0e-2))


    cls_list = pval_to_cls(p_values)


    # For each likelihood block we want to find the test stats which give
    # the largest cls, we create a dictionary for both test stats and cls
    # where the keys are given by the likelihood block and each value is an
    # empty list
    test_stats = {}
    cls = {}
    for tag in set(likelihood_index):
        test_stats[tag] = []
        cls[tag] = []

    #Now populate each list with the test stats and cls for the block
    for num, tag in enumerate(likelihood_index):
        test_stats[tag].append(chi_test[num])
        cls[tag].append(cls_list[num])

    #Loop over the blocks, for each block we find the index of the maximum
    # cls, we then update ._ts_s_sb and .ts_b with the test stat value using
    # the cls index
    for tag in set(likelihood_index):
        like_ob = like_blocks[tag]
        like_ob._index[stat_type] = max(range(len(cls[tag])), key=cls[tag].__getitem__) + 1

#        if cfg.contur_log.isEnabledFor(logging.DEBUG):
#            cfg.contur_log.debug(
#                "n data?, {} signal, {} background {}, bin {} ".format(like_ob._n, like_ob._s, like_ob._bg, like_ob._index))
                                                                
        like_ob._ts_s_b[stat_type], like_ob._ts_b[stat_type] = test_stats[tag][like_ob._index[stat_type] - 1]
