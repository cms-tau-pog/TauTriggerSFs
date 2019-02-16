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
    

    def __init__( self, trigger, year=2017, tauWP='medium', wpType='MVAv2' ):

        self.trigger = trigger
        assert( self.trigger in ['ditau', 'mutau', 'etau'] ), "Choose from: 'ditau', 'mutau', 'etau' triggers."
        self.year = year
        # Default to loading the Tau MVAv2 Medium ID based WPs
        self.tauWP = tauWP
        self.wpType = wpType
        assert( self.tauWP in ['vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] ), "You must choose a WP from: vloose, loose, medium, tight, vtight, or vvtight"
        assert( self.wpType in ['MVAv2', 'dR0p3'] ), "Choose from two provided ID types: 'MVAv2', 'dR0p3'. 'MVAv2' uses dR0p5, and 'dR0p3' is also an MVA-based ID."
        assert( self.wpType == 'MVAv2' ), "Tau POG is currently only providing efficiencies for MVAv2, sorry."
        assert( self.year == 2017 ), "Only 2017 trigger efficiencies currently provided in this tool. Stay tuned..."
        print "Loading Efficiencies for trigger %s usingTau %s ID WP %s for year %i" % (self.trigger, self.wpType, self.tauWP, self.year)

        # Assume this is in CMSSW with the below path structure
        base = os.environ['CMSSW_BASE']
        self.f = ROOT.TFile( base+'/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies%i.root' % self.year, 'r' )


        ## Load the TF1s containing the analytic best-fit results.
        ## This is done per decay mode: 0, 1, 10.
        #self.fitDataMap = {}
        #self.fitMCMap = {}
        #self.fitDataMap[ 0 ] = self.f.Get('%s_%s%s_dm0_DATA_fit' % (self.trigger, self.tauWP, self.wpType ) )
        #self.fitDataMap[ 1 ] = self.f.Get('%s_%s%s_dm1_DATA_fit' % (self.trigger, self.tauWP, self.wpType ) )
        #self.fitDataMap[ 10 ] = self.f.Get('%s_%s%s_dm10_DATA_fit' % (self.trigger, self.tauWP, self.wpType ) )
        #self.fitMCMap[ 0 ] = self.f.Get('%s_%s%s_dm0_MC_fit' % (self.trigger, self.tauWP, self.wpType ) )
        #self.fitMCMap[ 1 ] = self.f.Get('%s_%s%s_dm1_MC_fit' % (self.trigger, self.tauWP, self.wpType ) )
        #self.fitMCMap[ 10 ] = self.f.Get('%s_%s%s_dm10_MC_fit' % (self.trigger, self.tauWP, self.wpType ) )
        

        # Load the TH1s containing the analytic best-fit result in 1 GeV incriments and the associated uncertainty.
        # This is done per decay mode: 0, 1, 10.
        self.fitDataMap = {}
        self.fitMCMap = {}
        self.fitDataMap[ 0 ] = self.f.Get('%s_%s%s_dm0_DATA_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitDataMap[ 1 ] = self.f.Get('%s_%s%s_dm1_DATA_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitDataMap[ 10 ] = self.f.Get('%s_%s%s_dm10_DATA_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitMCMap[ 0 ] = self.f.Get('%s_%s%s_dm0_MC_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitMCMap[ 1 ] = self.f.Get('%s_%s%s_dm1_MC_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitMCMap[ 10 ] = self.f.Get('%s_%s%s_dm10_MC_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        

        # Load the TH2s containing the eta phi efficiency corrections
        # This is done per decay mode: 0, 1, 10.
        self.effEtaPhiDataMap = {}
        self.effEtaPhiMCMap = {}
        self.effEtaPhiDataMap[ 0 ] = self.f.Get('%s_%s%s_dm0_DATA' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiDataMap[ 1 ] = self.f.Get('%s_%s%s_dm1_DATA' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiDataMap[ 10 ] = self.f.Get('%s_%s%s_dm10_DATA' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiMCMap[ 0 ] = self.f.Get('%s_%s%s_dm0_MC' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiMCMap[ 1 ] = self.f.Get('%s_%s%s_dm1_MC' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiMCMap[ 10 ] = self.f.Get('%s_%s%s_dm10_MC' % (self.trigger, self.tauWP, self.wpType) )


        # Eta Phi Averages
        # This is done per decay mode: 0, 1, 10.
        self.effEtaPhiAvgDataMap = {}
        self.effEtaPhiAvgMCMap = {}
        self.effEtaPhiAvgDataMap[ 0 ] = self.f.Get('%s_%s%s_dm0_DATA_AVG' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiAvgDataMap[ 1 ] = self.f.Get('%s_%s%s_dm1_DATA_AVG' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiAvgDataMap[ 10 ] = self.f.Get('%s_%s%s_dm10_DATA_AVG' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiAvgMCMap[ 0 ] = self.f.Get('%s_%s%s_dm0_MC_AVG' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiAvgMCMap[ 1 ] = self.f.Get('%s_%s%s_dm1_MC_AVG' % (self.trigger, self.tauWP, self.wpType) )
        self.effEtaPhiAvgMCMap[ 10 ] = self.f.Get('%s_%s%s_dm10_MC_AVG' % (self.trigger, self.tauWP, self.wpType) )


    # Make sure we stay on our histograms
    def ptCheck( self, pt ) :
        if pt > 450 : pt = 450
        elif pt < 20 : pt = 20
        return pt

    def getEfficiency( self, pt, eta, phi, effHist, etaPhiHist, etaPhiAvgHist, uncert='Nominal' ) :
        pt = self.ptCheck( pt )
        eff = effHist.GetBinContent( effHist.FindBin( pt ) )

        # Shift the pt dependent efficiency by the fit uncertainty if requested
        if uncert != 'Nominal' :
            assert( uncert in ['Up', 'Down'] ), "Uncertainties are provided using 'Up'/'Down'"
            if uncert == 'Up' :
                eff += effHist.GetBinError( effHist.FindBin( pt ) )
            else : # must be Down
                eff -= effHist.GetBinError( effHist.FindBin( pt ) )

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
        if eff > 1. : eff = 1
        return eff


    # return the data efficiency or the +/- 1 sigma uncertainty shifted efficiency
    def getTriggerEfficiencyData( self, pt, eta, phi, dm ) :
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ])
    def getTriggerEfficiencyDataUncertUp( self, pt, eta, phi, dm ) :
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Up' )
    def getTriggerEfficiencyDataUncertDown( self, pt, eta, phi, dm ) :
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Down' )


    # return the MC efficiency or the +/- 1 sigma uncertainty shifted efficiency
    def getTriggerEfficiencyMC( self, pt, eta, phi, dm ) :
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ])
    def getTriggerEfficiencyMCUncertUp( self, pt, eta, phi, dm ) :
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Up' )
    def getTriggerEfficiencyMCUncertDown( self, pt, eta, phi, dm ) :
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Down' )


    # return the data/MC scale factor
    def getTriggerScaleFactor( self, pt, eta, phi, dm ) :
        pt = self.ptCheck( pt )
        effData = self.getTriggerEfficiencyData( pt, eta, phi, dm )
        effMC = self.getTriggerEfficiencyMC( pt, eta, phi, dm )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - %s Trigger SF for Tau ID: %s   WP: %s   pT: %f   eta: %s   phi: %f" % (self.trigger, self.wpType, self.tauWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0
        sf = effData / effMC
        return sf


    # return the data/MC scale factor with +1/-1 sigma uncertainty.
    # Data and MC fit uncertainties are treated as uncorrelated.
    # The calculated uncertainties are symmetric. Do error propagation
    # for simple division.
    def getTriggerScaleFactorUncert( self, pt, eta, phi, dm, uncert ) :
        assert( uncert in ['Up', 'Down'] ), "Uncertainties are provided using 'Up'/'Down'"
        pt = self.ptCheck( pt )

        effData = self.getTriggerEfficiencyData( pt, eta, phi, dm )
        effDataUp = self.getTriggerEfficiencyDataUncertUp( pt, eta, phi, dm )
        relDataDiff = (effDataUp - effData) / effData

        effMC = self.getTriggerEfficiencyMC( pt, eta, phi, dm )
        effMCUp = self.getTriggerEfficiencyMCUncertUp( pt, eta, phi, dm )
        if effMC < 1e-5 :
            # already printed an error for the nominal case...
            return 0.0
        relMCDiff = (effMCUp - effMC) / effMC

        deltaSF = sqrt( relDataDiff**2 + relMCDiff**2 )
        sf = (effData / effMC)
        if uncert == 'Up' :
            return sf * (1. + deltaSF)
        else : # must be Down
            return sf * (1. - deltaSF)




