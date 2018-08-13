# Checkout Instructions

For the current best tau trigger scale factors for 2017 data and MC do (this is a test branch for ReMiniaod)
```
git clone -b tauTriggers2017_reMiniaod_test git@github.com:truggles/TauTriggerSFs2017.git TauTriggerSFs2017
```
The c++ interface require you to scram b after checkout.

# Tau Trigger Scale Factor Tool for 2017 Data & MC

Tau trigger SFs can be derived from the root file containing the pT dependent efficiency curves for the 3 provided trigger combinations (data/tauTriggerEfficiencies2017.root) :
   * Mu+Tau Cross Trigger:
      * HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1
   * Elec+Tau Cross Trigger:
      * HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1
   * di-Tau Triggers: OR of all fully enabled triggers in 2017 data
      * HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg
      * HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg
      * HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg

The efficiencies and SF are measured on Full 2017 Data with 42 1/fb using SingleMuon dataset of 17Nov2017 ReReco samples. Further details can be found in Tau POG presentations such as: https://indico.cern.ch/event/700042/contributions/2871830/attachments/1591232/2527113/180129_TauPOGmeeting_TriggerEfficiency_hsert.pdf

# Accessing the Efficiencies and SFs

A helper class, "getTauTriggerSFs", in python/getTauTriggerSFs.py can be used. It should be initialized with the desired Tau ID type: "MVA" (dR0p5) or "dR0p3" (still an MVA-base ID), and WP being used. Currently supporting "vvloose", "vloose", "loose", "medium", "tight", "vtight", and "vvtight".

This class has three methods to return the trigger SF for each of the trigger groups mentioned above:
   * getDiTauScaleFactor( pt, eta, phi )
   * getETauScaleFactor( pt, eta, phi )
   * getMuTauScaleFactor( pt, eta, phi )

Additionally, if one needs the trigger efficiencies and not the SFs you can grab them as well. The trigger efficiencies will have the eta-phi adjustment already applied to them.
   * getDiTauEfficiencyData( pt, eta, phi )
   * getDiTauEfficiencyMC( pt, eta, phi )
   * getETauEfficiencyData( pt, eta, phi )
   * getETauEfficiencyMC( pt, eta, phi )
   * getMuTauEfficiencyData( pt, eta, phi )
   * getMuTauEfficiencyMC( pt, eta, phi )

There are currently no fits applied in this Git area. Fits will be considered for the final round of trigger SFs. Currently, "getTauTriggerSFs" fetches the efficiency of Data and MC from the associated bin value in TGraphAsymmErrors turned into TH1s for simplicity of access.

It is found that there is a slight barrel vs. end cap difference in tau trigger performance. To account for this, there are additional eta-phi adjustments made to the delivered SFs from "getTauTriggerSFs". In additional to the barrel / end cap separation, we isolate a specific region in the barrel which had well known issues with deal pixel modules and varying tau reconstruction during 2017 data taking (0 < eta < 1.5, phi > 2.8). The eta-phi adjustements are provided in a json file: data/tauTriggerEfficienciesEtaPhiMap2017.json and are applied by default in "getTauTriggerSFs".


# Example Code
For analysis using Tau MVA dR0p3 ID using Tight WP:
```
tauSFs = getTauTriggerSFs('tight', 'dR0p3')
diTauLeg1SF = tauSFs.getDiTauScaleFactor( pt1, eta1, phi1 )
diTauLeg2SF = tauSFs.getDiTauScaleFactor( pt2, eta2, phi2 )
```
For analysis using Tau MVA dR0p5 ID using Tight WP:
```
tauSFs = getTauTriggerSFs('tight', 'MVA')
```

# For Detailed Trigger Uncertainty Studies

The original efficiency TGraphAsymmErrors for the efficiencies are stored as RooHists in case people would like direct access to the most proper description of the uncertainties for each bin. The TGraphAsymmErrors --> TH1 process does not preserve proper uncertainties, this is why both are provided.


