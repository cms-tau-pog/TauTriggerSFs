#!/usr/bin/env python

'''
Class to get Tau Trigger SF based on 2017 Rereco data
and MCv2 (re-miniaod).

T. Ruggles
5 February, 2018
Updated 12 August, 2018
Updated 16 Feb, 2019
'''


import ROOT
import os
from math import sqrt

class getTauTriggerSFs :

    def __init__( self, trigger, year=2017, tauWP='medium', wpType='MVAv2', file_name=None, emb_sfs=False ):

        self.trigger = trigger
        assert( self.trigger in ['ditau', 'mutau', 'etau'] ), "Choose from: 'ditau', 'mutau', 'etau' triggers."
        self.year = year
        # Default to loading the Tau MVAv2 Medium ID based WPs
        self.tauWP = tauWP
        self.wpType = wpType
        self.provide_emb_sfs = emb_sfs
        assert( self.wpType in ['MVAv2', 'dR0p3', 'DeepTau'] ), "Choose from three provided ID types: 'MVAv2', 'dR0p3' and 'DeepTau'. 'MVAv2' uses dR0p5, and 'dR0p3' is also an MVA-based ID."
        assert( (self.wpType == "MVAv2" and self.tauWP in ['vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'])
                or (self.wpType == "DeepTau" and self.tauWP in ['vvvloose', 'vvloose', 'vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight']) ), "You must choose a WP from: vloose, loose, medium, tight, vtight, or vvtight for MVA Tau IDs and vvvloose, vvloose, vloose, loose, medium, tight, vtight, or vvtight for the DeepTau ID"
        assert( (self.wpType == 'MVAv2' and not self.provide_emb_sfs)
                or (self.wpType == 'DeepTau' and self.provide_emb_sfs) ), "Tau POG is currently only providing MC efficiencies for MVAv2 and embedded efficiencies for DeepTau, sorry."
        assert( self.year in [2016, 2017, 2018] ), "Choose which year trigger efficiencies you need."
        print "Loading Efficiencies for trigger %s usingTau %s ID WP %s for year %i based on %s samples" % (self.trigger, self.wpType, self.tauWP, self.year, "embedded" if self.provide_emb_sfs else "simulated")

        # Assume this is in CMSSW with the below path structure
        if file_name is None:
            base = os.environ['CMSSW_BASE']
            if self.provide_emb_sfs:
                self.f = ROOT.TFile( base+'/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies%i_Embedded_deeptau.root' % self.year, 'r' )
            else:
                self.f = ROOT.TFile( base+'/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies%i.root' % self.year, 'r' )
        else:
            self.f = ROOT.TFile( file_name, "r")


        if 'DeepTau' in self.wpType:
            self.available_dms = [0, 1, 10, 11]
        else:
            self.available_dms = [0, 1, 10]
        ## Load the TF1s containing the analytic best-fit results.
        ## This is done per decay mode: 0, 1, 10.
        self.fitDataMap = {}
        self.fitMCMap = {}
        hist_name = '%s_%s%s_dm%i_MC_fit'
        if self.provide_emb_sfs:
            hist_name = '%s_%s%s_dm%i_EMB_fit'
        for dm in self.available_dms:
            self.fitDataMap[ dm ] = ROOT.gDirectory.Get('%s_%s%s_dm%i_DATA_fit' % (self.trigger, self.tauWP, self.wpType, dm ) )
            self.fitMCMap[ dm ] = ROOT.gDirectory.Get(hist_name % (self.trigger, self.tauWP, self.wpType, dm ) )


        # Load the TH1s containing the analytic best-fit result in 1 GeV incriments and the associated uncertainty.
        # This is done per decay mode: 0, 1, 10.
        self.fitUncDataMap = {}
        self.fitUncMCMap = {}
        hist_name = hist_name.replace("fit", "errorBand")
        for dm in self.available_dms:
            self.fitUncDataMap[ dm ] = self.f.Get('%s_%s%s_dm%i_DATA_errorBand' % (self.trigger, self.tauWP, self.wpType, dm ) )
            self.fitUncMCMap[ dm ] = self.f.Get(hist_name % (self.trigger, self.tauWP, self.wpType, dm ) )

         # Load the TH1s containing the bin by bin values
        self.binnedSFMap = {}
        for dm in self.available_dms:
            self.binnedSFMap[ dm ] = self.f.Get('%s_%s%s_dm%i_CoarseBinSF' % (self.trigger, self.tauWP, self.wpType, dm) )

        # Because of low statistics in the problem region of the barrel, we apply the Eta-Phi corrections
        # based on taus firing mutau trigger and passing the vloose MVA WP. This provides the most statistically
        # robust measurement for the correction. Considering the three Eta-Phi regions should not have significantly
        # different SF adjustments for different MVA WPs, this should also be a safe choice.
        etaPhiWP = 'vloose'
        etaPhiTrigger = 'mutau'
        # Load the TH2s containing the eta phi efficiency corrections
        # This is done per decay mode: 0, 1, 10.
        self.effEtaPhiDataMap = {}
        self.effEtaPhiMCMap = {}
        hist_name = hist_name.replace("_errorBand", "")
        for dm in self.available_dms:
            self.effEtaPhiDataMap[ dm ] = self.f.Get('%s_%s%s_dm%i_DATA' % (etaPhiTrigger, etaPhiWP, self.wpType, dm) )
            self.effEtaPhiMCMap[ dm ] = self.f.Get(hist_name % (etaPhiTrigger, etaPhiWP, self.wpType, dm) )


        # Eta Phi Averages
        # This is done per decay mode: 0, 1, 10.
        self.effEtaPhiAvgDataMap = {}
        self.effEtaPhiAvgMCMap = {}
        hist_name = hist_name + "_AVG"
        for dm in self.available_dms:
            self.effEtaPhiAvgDataMap[ dm ] = self.f.Get('%s_%s%s_dm%i_DATA_AVG' % (etaPhiTrigger, etaPhiWP, self.wpType, dm) )
            self.effEtaPhiAvgMCMap[ dm ] = self.f.Get(hist_name % (etaPhiTrigger, etaPhiWP, self.wpType, dm) )


    # Make sure we stay on our histograms
    def ptCheck( self, pt ) :
        if pt > 450 : pt = 450
        elif pt < 20 : pt = 20
        return pt

    # Make sure to have only old DMs, DM0, DM1, DM10
    def dmCheck( self, dm ) :
        if dm == 2 : dm = 1   # Originally, DM=2 was included in oldDM, but with the dynamic strip clustering the second strip was reconstructed together with the first one. So it ends up to DM=1. But, there are still some cases where DM=2 survives.
        return dm

    def getEfficiency( self, pt, eta, phi, fit, uncHist, etaPhiHist, etaPhiAvgHist, uncert='Nominal') :
        pt = self.ptCheck( pt )
        eff = fit.Eval( pt )

        # Shift the pt dependent efficiency by the fit uncertainty if requested
        if uncert != 'Nominal' :
            assert( uncert in ['Up', 'Down'] ), "Uncertainties are provided using 'Up'/'Down'"
            if uncert == 'Up' :
                eff += uncHist.GetBinError( uncHist.FindBin( pt ) )
            else : # must be Down
                eff -= uncHist.GetBinError( uncHist.FindBin( pt ) )

        # Adjust SF based on (eta, phi) location
        # keep eta barrel boundaries within SF region
        # but, for taus outside eta limits or with unralistic
        # phi values, return zero SF
        if eta == 2.1 : eta = 2.09
        elif eta == -2.1 : eta = -2.09

        etaPhiVal = etaPhiHist.GetBinContent( etaPhiHist.FindBin( eta, phi ) )
        etaPhiAvg = etaPhiAvgHist.GetBinContent( etaPhiAvgHist.FindBin( eta, phi ) )
        if etaPhiAvg <= 0.0 :
            print "One of the provided tau (eta, phi) values (%3.3f, %3.3f) is outside the boundary of triggering taus" % (eta, phi)
            print "Returning efficiency = 0.0"
            return 0.0

        eff *= etaPhiVal / etaPhiAvg
        if eff > 1. : eff = 1.
        if eff < 0. : eff = 0. # Some efficiency fits go negative at very low tau pT, prevent that.
        return eff


    # return the data efficiency or the +/- 1 sigma uncertainty shifted efficiency
    def getTriggerEfficiencyData( self, pt, eta, phi, dm) :
        dm = self.dmCheck( dm )
        assert( dm in self.available_dms ), "Efficiencies only provided for DMs %s.  You provided DM %i" % (", ".join(map(str, self.available_dms)), dm)
        return self.getEfficiency( pt, eta, phi, self.fitDataMap[ dm ], self.fitUncDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Nominal')
    def getTriggerEfficiencyDataUncertUp( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in self.available_dms ), "Efficiencies only provided for DMs %s.  You provided DM %i" % (", ".join(map(str, self.available_dms)), dm)
        return self.getEfficiency(  pt, eta, phi, self.fitDataMap[ dm ], self.fitUncDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Up' )
    def getTriggerEfficiencyDataUncertDown( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in self.available_dms ), "Efficiencies only provided for DMs %s.  You provided DM %i" % (", ".join(map(str, self.available_dms)), dm)
        return self.getEfficiency( pt, eta, phi, self.fitDataMap[ dm ], self.fitUncDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Down' )


    # return the MC efficiency or the +/- 1 sigma uncertainty shifted efficiency
    def getTriggerEfficiencyMC( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in self.available_dms ), "Efficiencies only provided for DMs %s.  You provided DM %i" % (", ".join(map(str, self.available_dms)), dm)
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], self.fitUncMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Nominal')
    def getTriggerEfficiencyMCUncertUp( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in self.available_dms ), "Efficiencies only provided for DMs %s.  You provided DM %i" % (", ".join(map(str, self.available_dms)), dm)
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], self.fitUncMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Up'  )
    def getTriggerEfficiencyMCUncertDown( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in self.available_dms ), "Efficiencies only provided for DMs %s.  You provided DM %i" % (", ".join(map(str, self.available_dms)), dm)
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], self.fitUncMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Down' )


    def getBinnedScaleFactor (self, pt, dm, sfHisto) :
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        sf = 1
        if(sfHisto):
            sf = sfHisto.GetBinContent(sfHisto.FindBin( pt ))
        return sf

    def getBinnedScaleFactorUnc(self, pt,  dm, sfHisto) :
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        SFunc = 0
        if(sfHisto):
            SFunc = sfHisto.GetBinError( sfHisto.FindBin( pt ) )
        return SFunc

	# return the data/MC scale factor
    def getTriggerScaleFactor( self, pt, eta, phi, dm) :
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        effData = self.getTriggerEfficiencyData( pt, eta, phi, dm )
        effMC = self.getTriggerEfficiencyMC( pt, eta, phi, dm )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - %s Trigger SF for Tau ID: %s   WP: %s   pT: %f   eta: %s   phi: %f" % (self.trigger, self.wpType, self.tauWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0

        if(self.year == 2016):
            if(self.trigger == 'ditau'): pt_recommended = 40
            elif(self.trigger == 'mutau' or self.trigger  == 'etau'): pt_recommended = 25

            if( pt > pt_recommended):
                if(effMC!=0): sf = effData / effMC
                else:
                    sf = 0
                    print "The efficiency is zero in either Data or MC histogram, so SF is set to zero"
            else:
                sf = self.getBinnedScaleFactor(pt, dm, self.binnedSFMap[ dm])

        elif(self.year==2017 or self.year == 2018):
            if(effData!=0 and effMC!=0): sf = effData / effMC
            else:
                sf = 0
                print "The efficiency is zero in either Data or MC histogram, so SF is set to zero"

        return sf


    # return the data/MC scale factor with +1/-1 sigma uncertainty.
    # Data and MC fit uncertainties are treated as uncorrelated.
    # The calculated uncertainties are symmetric. Do error propagation
    # for simple division. Using getTriggerEfficiencyXXXUncertDown instead
    # of Up ensures we have the full uncertainty reported. Up sometimes
    # is clipped by efficiency max of 1.0.
    def getTriggerScaleFactorUncert( self, pt, eta, phi, dm, uncert) :
        assert( uncert in ['Up', 'Down'] ), "Uncertainties are provided using 'Up'/'Down'"
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        effData = self.getTriggerEfficiencyData( pt, eta, phi, dm )
        effDataDown = self.getTriggerEfficiencyDataUncertDown( pt, eta, phi, dm )
        if(effData!=0): relDataDiff = (effData - effDataDown) / effData

        effMC = self.getTriggerEfficiencyMC( pt, eta, phi, dm)
        effMCDown = self.getTriggerEfficiencyMCUncertDown( pt, eta, phi, dm )
        if effMC < 1e-5 :
            # already printed an error for the nominal case...
            return 0.0
        if(effMC!=0): relMCDiff = (effMC - effMCDown) / effMC

        sf_fit = effData / effMC
        sf_binned =  self.getBinnedScaleFactor(pt, dm, self.binnedSFMap[ dm])

        deltaSF_fit = sqrt( relDataDiff**2 + relMCDiff**2 )
        deltaSF_binned =  self.getBinnedScaleFactorUnc(pt, dm, self.binnedSFMap[ dm])

        if(effMC!=0): relMCDiff = (effMC - effMCDown) / effMC
        if(self.year == 2016):
            if(self.trigger == 'ditau'): pt_recommended = 40
            elif(self.trigger == 'mutau' or self.trigger  == 'etau'): pt_recommended = 25

            if( pt > pt_recommended):
                sf = sf_fit
                deltaSF = deltaSF_fit
            else:
                sf= sf_binned
                deltaSF = deltaSF_binned
        else:
            sf = sf_fit
            deltaSF = deltaSF_fit

        if uncert == 'Up' :
            return sf * (1. + deltaSF)
        else : # must be Down
            return sf * (1. - deltaSF)


