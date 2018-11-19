#!/usr/bin/env python

'''
Class to get Tau Trigger SF based on 2017 Rereco data
and MCv2 (re-miniaod).

T. Ruggles
5 February, 2018
Updated 12 August, 2018
'''


import ROOT
import os

class getTauTriggerSFs :
    

    def __init__( self, tauWP='medium', wpType='MVA' ):

        # Default to loading the Tau MVA Medium ID based WPs
        self.tauWP = tauWP
        self.wpType = wpType
        assert( self.tauWP in ['vvloose', 'vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] ), "You must choose a WP from: vvloose, vloose, loose, medium, tight, vtight, or vvtight"
        assert( self.wpType in ['MVA', 'dR0p3'] ), "Choose from two provided ID types: 'MVA', 'dR0p3'. 'MVA' uses dR0p5, and 'dR0p3' is also an MVA-based ID."
        print "Loading Efficiencies for Tau %s ID WP %s" % (self.wpType, self.tauWP)

        # Assume this is in CMSSW with the below path structure
        base = os.environ['CMSSW_BASE']
        self.f_old = ROOT.TFile( base+'/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root', 'r' )
        self.f = ROOT.TFile( base+'/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017_New.root', 'r' )

        # Load the TH1s containing the bin by bin values
        self.diTauData = self.f.Get('hist_diTauTriggerEfficiency_%sTau%s_DATA' % (self.tauWP, self.wpType) )
        self.diTauMC = self.f.Get('hist_diTauTriggerEfficiency_%sTau%s_MC' % (self.tauWP, self.wpType) )
        self.eTauData = self.f.Get('hist_ETauTriggerEfficiency_%sTau%s_DATA' % (self.tauWP, self.wpType) )
        self.eTauMC = self.f.Get('hist_ETauTriggerEfficiency_%sTau%s_MC' % (self.tauWP, self.wpType) )
        self.muTauData = self.f.Get('hist_MuTauTriggerEfficiency_%sTau%s_DATA' % (self.tauWP, self.wpType) )
        self.muTauMC = self.f.Get('hist_MuTauTriggerEfficiency_%sTau%s_MC' % (self.tauWP, self.wpType) )
        

        # FIXME: Use the eta-phi efficiency corrections from pre-re-miniaod branch
        # Only medium, tight, and vtight are provided and they are from MVA ID
        tmpWP = self.tauWP
        if tmpWP in ['vvloose', 'vloose', 'loose'] : tmpWP = 'medium'
        if tmpWP == 'vvtight' : tmpWP = 'vtight'


        # Load the TH2s containing the eta phi efficiency corrections
        self.diTauEtaPhiData = self.f_old.Get('diTau_%s_DATA' % tmpWP )
        self.diTauEtaPhiMC = self.f_old.Get('diTau_%s_MC' % tmpWP )
        self.eTauEtaPhiData = self.f_old.Get('eTau_%s_DATA' % tmpWP )
        self.eTauEtaPhiMC = self.f_old.Get('eTau_%s_MC' % tmpWP )
        self.muTauEtaPhiData = self.f_old.Get('muTau_%s_DATA' % tmpWP )
        self.muTauEtaPhiMC = self.f_old.Get('muTau_%s_MC' % tmpWP )

        # Eta Phi Avg
        self.diTauEtaPhiAvgData = self.f_old.Get('diTau_%s_AVG_DATA' % tmpWP )
        self.diTauEtaPhiAvgMC = self.f_old.Get('diTau_%s_AVG_MC' % tmpWP )
        self.eTauEtaPhiAvgData = self.f_old.Get('eTau_%s_AVG_DATA' % tmpWP )
        self.eTauEtaPhiAvgMC = self.f_old.Get('eTau_%s_AVG_MC' % tmpWP )
        self.muTauEtaPhiAvgData = self.f_old.Get('muTau_%s_AVG_DATA' % tmpWP )
        self.muTauEtaPhiAvgMC = self.f_old.Get('muTau_%s_AVG_MC' % tmpWP )


    # Make sure we stay on our histograms
    def ptCheck( self, pt ) :
        if pt > 499 : pt = 499
        elif pt < 20 : pt = 21
        return pt

    def getEfficiency( self, pt, eta, phi, effHist, etaPhi, etaPhiAvg ) :
        pt = self.ptCheck( pt )
        eff = effHist.GetBinContent( effHist.FindBin( pt ) )

        # Adjust SF based on (eta, phi) location
        # keep eta barrel boundaries within SF region
        # but, for taus outside eta limits or with unralistic
        # phi values, return zero SF
        if eta == 2.1 : eta = 2.09
        elif eta == -2.1 : eta = -2.09

        etaPhiVal = etaPhi.GetBinContent( etaPhi.FindBin( eta, phi ) )
        etaPhiAvg = etaPhiAvg.GetBinContent( etaPhiAvg.FindBin( eta, phi ) )
        if etaPhiAvg <= 0.0 :
            print "One of the provided tau (eta, phi) values (%3.3f, %3.3f) is outside the boundary of triggering taus" % (eta, phi)
            print "Returning efficiency = 0.0"
            return 0.0
        eff *= etaPhiVal / etaPhiAvg
        if eff > 1. : eff = 1
        return eff


    # This is the efficiency for a single leg of the di-tau trigger
    def getDiTauEfficiencyData( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.diTauData, self.diTauEtaPhiData, self.diTauEtaPhiAvgData )


    # This is the efficiency for a single leg of the di-tau trigger
    def getDiTauEfficiencyMC( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.diTauMC, self.diTauEtaPhiMC, self.diTauEtaPhiAvgMC )


    # This is the SF for a single leg of the di-tau trigger
    def getDiTauScaleFactor( self, pt, eta, phi ) :
        pt = self.ptCheck( pt )
        effData = self.getDiTauEfficiencyData( pt, eta, phi )
        effMC = self.getDiTauEfficiencyMC( pt, eta, phi )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - DiTau Trigger SF for Tau ID: %s   WP: %s   pT: %f   eta: %s   phi: %f" % (self.wpType, self.tauWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0
        sf = effData / effMC
        return sf


    # This is the efficiency for the tau leg of the mu-tau trigger
    def getMuTauEfficiencyData( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.muTauData, self.muTauEtaPhiData, self.muTauEtaPhiAvgData )


    # This is the efficiency for the tau leg of the mu-tau trigger
    def getMuTauEfficiencyMC( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.muTauMC, self.muTauEtaPhiMC, self.muTauEtaPhiAvgMC )


    # This is the SF for the tau leg of the mu-tau trigger
    def getMuTauScaleFactor( self, pt, eta, phi ) :
        pt = self.ptCheck( pt )
        effData = self.getMuTauEfficiencyData( pt, eta, phi )
        effMC = self.getMuTauEfficiencyMC( pt, eta, phi )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - MuTau Trigger SF for Tau ID: %s   WP: %s   pT: %f   eta: %s   phi: %f" % (self.wpType, self.tauWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0
        sf = effData / effMC
        return sf



    # This is the efficiency for the tau leg of the e-tau trigger
    def getETauEfficiencyData( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.eTauData, self.eTauEtaPhiData, self.eTauEtaPhiAvgData )


    # This is the efficiency for the tau leg of the e-tau trigger
    def getETauEfficiencyMC( self, pt, eta, phi ) :
        return self.getEfficiency( pt, eta, phi, self.eTauMC, self.eTauEtaPhiMC, self.eTauEtaPhiAvgMC )


    # This is the SF for the tau leg of the e-tau trigger
    def getETauScaleFactor( self, pt, eta, phi ) :
        pt = self.ptCheck( pt )
        effData = self.getETauEfficiencyData( pt, eta, phi )
        effMC = self.getETauEfficiencyMC( pt, eta, phi )
        if effMC < 1e-5 :
            print "Eff MC is suspiciously low. Please contact Tau POG."
            print " - ETau Trigger SF for Tau ID: %s   WP: %s   pT: %f   eta: %s   phi: %f" % (self.wpType, self.tauWP, pt, eta, phi)
            print " - MC Efficiency = %f" % effMC
            return 0.0
        sf = effData / effMC
        return sf


