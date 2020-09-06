# Checkout Instructions

For the current tau trigger scale factors for 2018, 2017 data and MC do:
```
cd $CMSSW_BASE/src
mkdir TauAnalysisTools
git clone -b run2_SFs https://github.com/cms-tau-pog/TauTriggerSFs $CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs
scram b -j 8
```

The c++ interface require you to scram b after checkout. If you do not place the code in the above hierarchy within CMSSW
the python paths are not guaranteed to work.


# Tau Trigger Scale Factor Tool for 2018 Data & MC

Tau trigger SFs can be derived from the root file containing the pT dependent efficiency curves for the 3 provided trigger combinations `data/tauTriggerEfficiencies2018.root` :
   * Mu+Tau Cross Trigger:
      * HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1,   for Run < 317509
      * HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau**HPS**27_eta2p1_CrossL1,  for Run >= 317509

   * Elec+Tau Cross Trigger:
      * HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1, for Run < 317509
      * HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau**HPS**30_eta2p1_CrossL1,  for Run >= 317509

   * di-Tau Triggers: OR of all fully enabled triggers in 2017 data for Run < 317509 before HPS tau reconstruction is deployed, and use the single ditau trigger for Run >= 317509 after HPS is deployed
      * HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg, for Run < 317509
      * HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg
      * HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg
      * HLT_DoubleMediumChargedIsoPFTau**HPS**35_Trk1_eta2p1_Reg,  for Run >= 317509

Efficiencies and SF are measured on Full 2018 Data with 59.6 1/fb using SingleMuon dataset of 17Sep18 ReReco samples from RunA to RunC and of PromptReco samples for RunD. The 2018 SFs are provided including the analytic fit and uncertainties per decay mode in May 2019: https://indico.cern.ch/event/820066/contributions/3430600/attachments/1843348/3023303/TauTrigger2018SF_tauIDMeeting_hsert.pdf


# Tau Trigger Scale Factor Tool for 2017 Data & MC

Tau trigger SFs can be derived from the root file containing the pT dependent efficiency curves for the 3 provided trigger combinations `data/tauTriggerEfficiencies2017.root` :
   * Mu+Tau Cross Trigger:
      * HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1
   * Elec+Tau Cross Trigger:
      * HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1
   * di-Tau Triggers: OR of all fully enabled triggers in 2017 data
      * HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg
      * HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg
      * HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg

Original efficiencies and SF are measured on Full 2017 Data with 42 1/fb using SingleMuon dataset of 17Nov2018 ReReco samples. Further details can be found in Tau POG presentations such as: https://indico.cern.ch/event/700042/contributions/2871830/attachments/1591232/2527113/180129_TauPOGmeeting_TriggerEfficiency_hsert.pdf

Updated MCv2 uncertainties with MVAv2 presented in August 2018: https://indico.cern.ch/event/749815/contributions/3104487/attachments/1700196/2737887/Ruggles_TauTriggers_TauPOG_20180813_v1.pdf

*Most Current Results* Updated SFs are provided including the analytic fit and uncertainties February 2019: https://indico.cern.ch/event/799374/contributions/3323191/attachments/1797874/2931826/TauTrigger2017SFv3_TauID_hsert.pdf

# Tau Trigger Scale Factor Tool for Embedded 2016 & 2017 & 2018

Tau trigger SFs for the DeepTau ID in the embedded samples can be derived from the root files containing the pT dependent efficiency curves for the 3 provided trigger combinations `data/tauTriggerEfficiencies{2016,2017,2018}_Embedded_deeptau.root` :
   * Mu+Tau Cross Trigger:
      * HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1,    for 2016
      * HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1,   for 2017 and 2018 Run < 317509
      * HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau**HPS**27_eta2p1_CrossL1,  for 2018 Run >= 317509

   * Elec+Tau Cross Trigger:
      * HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1,    for 2016 Run < 276215
      * HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20,             for 2016 276214 < Run < 278270
      * HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30,             for 2016 Run > 278269
      * HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1, for 2017 and 2018 Run < 317509
      * HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau**HPS**30_eta2p1_CrossL1,  for 2018 Run >= 317509

   * di-Tau Triggers: OR of all fully enabled triggers in 2017 data for Run < 317509 before HPS tau reconstruction is deployed, and use the single ditau trigger for Run >= 317509 after HPS is deployed
      * HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg,               for 2016 Run B-G
      * HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg,       for 2016 Run H
      * HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg, for 2017 and 2018 Run < 317509
      * HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg
      * HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg
      * HLT_DoubleMediumChargedIsoPFTau**HPS**35_Trk1_eta2p1_Reg,  for 2018 Run >= 317509

Due to ineffieciencies in the tau reconstruction at the HLT in the embedded samples in 2017 and 2018, the full trigger paths can not be used for these years. Instead the provided efficiencies are measured for previous filters in the HLT chain. Thus, in an analysis using the provided scale factors the used trigger decision should be based on the earlier filters and the match of the corresponding lepton of the cross triggers to the overlap filter must not be performed. The filters used for the matching are:
    * Mu+Tau Cross Trigger:
        * hltL1sMu18erTau24erIorMu20erTau24er,    for 2017 and 2018 Run < 317509
        * hltL1sBigORMu18erTauXXer2p1,            for 2018 Run >= 317509
    * Elec+Tau Cross Trigger:
        * hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3
    * di-Tau Trigger:
        * hltDoubleL2IsoTau26eta2p2

Efficiencies and SF are measured on the full 2016, 2017 and 2018 data sets with 35.9 1/fb, 41.5 1/fb and 59.6 1/fb, respectively, using the SingleMuon datasets of 17July2018 ReReco samples in 2016, 31Mar2018 ReReco samples in 2018 and 17Sep18 ReReco samples from Run2018A to Run2018C and of PromptReco samples for Run2018D. The SFs are provided including the analytic fit and uncertainties per decay mode in November 2019: https://indico.cern.ch/event/864131/contributions/3644102/attachments/1946592/3229746/TauTriggerEfficiencies_Embedded.pdf


# Trigger Efficiency / SF Fit and Uncertainties

Starting with the 2017 dataset, we are attempting to provide trigger efficiency uncertainties based on the results of the analytic fit of the TGraphAsymmErrors. The fit function is a modified CrystalBall CDF: `fit = ROOT.TF1('fit', '[5] - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3])*([4])')`. 
The uncertainties are aimed to provide we well motivated description of the trigger efficiency uncertainty. We have not tested the results of this method against the previous standard method which was applying a flat log-normal uncertainty in an analysis workflow. The fit uncertainties tend to lead to larger relative uncertainty in the trigger turn-on region and smaller relative uncertainties in the plateau region.

Application of the efficiency and SF uncertainties should be considered _EXPERIMENTAL_ at the moment. We are curious to hear feedback.

# Accessing the Efficiencies and SFs

A helper class, `getTauTriggerSFs`, in `python/getTauTriggerSFs.py` can be used. It should be initialized with:
   * the desired trigger: `ditau`, `mutau`, `etau`
   * the data year: `2017`, `2018` as an int
   * the WP being used: `vloose`, `loose`, `medium`, `tight`, `vtight`, and `vvtight` (`vvloose` was not provided in 2017, but it is provided for 2018. If you want to use this WP, please contact with us.)
   * the desired Tau ID type: `MVAv2` which uses dR0p5. The `dR0p3` WPs are not supported currently. The `DeepTau` WPs are currently only supported for the embedded samples with this interface.
   * a boolean flag indicating whether you want to read out the scale factors for simulated or embedded samples.

```
from TauAnalysisTools.TauTriggerSFs.getTauTriggerSFs import getTauTriggerSFs
tauSFs = getTauTriggerSFs('ditau', 2017, 'tight', 'MVAv2')
tauSFs_emb = getTauTriggerSFs('ditau', 2017, 'tight', 'DeepTau', emb_sfs=True) # to read out the scale factors for the embedded samples.
```

This class has a single methods to return the trigger SF for the triggers mentioned above. Additionally, this same function can be called with a 5th agrument requesting the shifted SF which represents a +/- 1 sigma shift in the fit function uncertainty:
   * getTriggerScaleFactor( pt, eta, phi, decayMode )
   * getTriggerScaleFactor( pt, eta, phi, decayMode, 'Up' )
   * getTriggerScaleFactor( pt, eta, phi, decayMode, 'Down' )

```
nominal_sf = tauSFs.getTriggerScaleFactor( tau.pt(), tau.eta(), tau.phi(), tau.decayMode() ) )
sf_up      = tauSFs.getTriggerScaleFactorUncert( tau.pt(), tau.eta(), tau.phi(), tau.decayMode(), 'Up' ) )
sf_down    = tauSFs.getTriggerScaleFactorUncert( tau.pt(), tau.eta(), tau.phi(), tau.decayMode(), 'Down' ) )
```

Additionally, if one needs the trigger efficiencies and not the SFs you can grab them as well. The trigger efficiencies will have the eta-phi adjustment already applied to them. There are additionally extra functions for the uncertainty shifts.
   * getTriggerEfficiencyData( pt, eta, phi, dm )
   * getTriggerEfficiencyDataUncertUp( pt, eta, phi, dm )
   * getTriggerEfficiencyDataUncertDown( pt, eta, phi, dm )
   * getTriggerEfficiencyMC( pt, eta, phi, dm )
   * getTriggerEfficiencyMCUncertUp( pt, eta, phi, dm )
   * getTriggerEfficiencyMCUncertDown( pt, eta, phi, dm )

The MC functions return the efficiencies for the embedded samples if the emb_sfs flag is set to `True` during the creation of the readout class.

It is found that there is a slight barrel vs. end cap difference in tau trigger performance. To account for this, there are additional eta-phi adjustments made to the delivered SFs from `getTauTriggerSFs`. 

In 2017, in additional to the barrel / end cap separation, we isolate a specific region in the barrel which had well known issues with deal pixel modules and varying tau reconstruction during 2017 data taking (0 < eta < 1.5, phi > 2.8). The eta-phi adjustements are provided in as TH2s in the main root file `data/data/tauTriggerEfficiencies2017.root` and are applied by default in `getTauTriggerSFs`.

In 2018, in additional to the barrel / end cap separation, we isolate a specific region in the endcap which had well known issues with broken HCAL modules ((-2.1 < tauEta < -1.5) && (-1.6 < tauPhi < -0.8). The eta-phi adjustements are provided in as TH2s in the main root file `data/data/tauTriggerEfficiencies2018.root` and are applied by default in `getTauTriggerSFs`.

# Example Code
For analysis using Tau MVAv2 dR0p5 ID using Tight WP:
```
from TauAnalysisTools.TauTriggerSFs.getTauTriggerSFs import getTauTriggerSFs
tauSFs = getTauTriggerSFs('ditau', 2017, 'tight', 'MVAv2')

nominal_sf = tauSFs.getTriggerScaleFactor( tau.pt(), tau.eta(), tau.phi(), tau.decayMode() ) )
sf_up      = tauSFs.getTriggerScaleFactorUncert( tau.pt(), tau.eta(), tau.phi(), tau.decayMode(), 'Up' ) )
sf_down    = tauSFs.getTriggerScaleFactorUncert( tau.pt(), tau.eta(), tau.phi(), tau.decayMode(), 'Down' ) )
```

# For Detailed Trigger Uncertainty Studies

Please contact the Tau POG trigger experts who can help point you towards the original NTuples used to make the fits and TGraphAsymmErrors distributions.


# For use with C++ interface

Thank you to Christian Veelken and Artur Gottmann who have both contributed here.  
The C++ interface requires you to have the proper directory structure from the initial checkout instructions.  
You will need to update your `BuildFile.xml` to include `<use name="TauTriggerSFs2017/TauTriggerSFs2017" />`.
For an example of how to use the code in an EDProducer see Artur/KIT's code here:
   * `TauTrigger2017EfficiencyProducer.h`: https://github.com/KIT-CMS/KITHiggsToTauTau/blob/reduced_trigger_objects/interface/Producers/TauTrigger2017EfficiencyProducer.h
   * `TauTrigger2017EfficiencyProducer.cc`: https://github.com/KIT-CMS/KITHiggsToTauTau/blob/reduced_trigger_objects/src/Producers/TauTrigger2017EfficiencyProducer.cc

# For Recreating Efficiency ROOT File for Other Years
There are some simple python scripts available to create the ROOT file used by `python/getTauTriggerSFs.py`. These are current set up to take the Tau POG style ntuples and the fit files created by Hale. Important files:
   * `makeEtaPhiJson.py`: create eta-phi efficiency maps. If detector conditions were perfect, these could be used to account for differences in eta efficiencies between barrel and endcap. As it is, in 2017 the eta-phi mapping targets the 2017 pixel problem region. This should be edited for delivery of 2018 eta-phi efficiencies.
   * `makeEtaPhiFiles.py`: converts the output JSON file from `makeEtaPhiJson.py` into a ROOT file with TH2s representing the eta-phi efficiencies.
   * `copyEfficiencies.py`: copies and renames the needed portions of the resulting fit ROOT file to use by the tool.

```
python python/makeEtaPhiJson.py
python python/makeEtaPhiFiles.py
python python/copyEfficiencies.py
hadd data/tauTriggerEfficiencies2017.root data/tauTriggerEfficiencies2017_FINAL.root data/tauTriggerEfficienciesEtaPhi2017_FINAL.root
```
