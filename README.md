# Checkout Instructions

For the current best tau trigger scale factors for 2017 data and MC do:
```
cd $CMSSW_BASE/src
mkdir TauAnalysisTools
cd TauAnalysisTools
git clone -b final_2017_MCv2 git@github.com:truggles/TauTriggerSFs.git TauTriggerSFs
```
The c++ interface require you to scram b after checkout. If you do not place the code in the above hierarchy within CMSSW
the python paths are not guaranteed to work.

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

*Most Current Results* Updated SFs are provided including the analytic fit and uncertainties February 2019: https://indico.cern.ch/event/799374/contributions/3323191/attachments/1797874/2931506/TauTrigger2017SFv3_TauID_hsert.pdf

# Trigger Efficiency / SF Fit and Uncertainties

Starting with the 2017 dataset, we are attempting to provide trigger efficiency uncertainties based on the results of the analytic fit of the TGraphAsymmErrors. The fit function is a modified CrystalBall CDF: `fit = ROOT.TF1('fit', '[5] - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3])*([4])')`. 
The uncertainties are aimed to provide we well motivated description of the trigger efficiency uncertainty. We have not tested the results of this method against the previous standard method which was applying a flat log-normal uncertainty in an analysis workflow. The fit uncertainties tend to lead to larger relative uncertainty in the trigger turn-on region and smaller relative uncertainties in the plateau region.

Application of the efficiency and SF uncertainties should be considered _EXPERIMENTAL_ at the moment. We are curious to hear feedback.

# Accessing the Efficiencies and SFs

A helper class, `getTauTriggerSFs`, in `python/getTauTriggerSFs.py` can be used. It should be initialized with:
   * the desired trigger: `ditau`, `mutau`, `etau`
   * the data year: 2017 as an int (currently on 2017 provided)
   * the WP being used: `vloose`, `loose`, `medium`, `tight`, `vtight`, and `vvtight` (`vvloose` is not supported by the Tau POG)
   * the desired Tau ID type: `MVAv2` which uses dR0p5. The `dR0p3` WPs are not supported currently.

```
from TauAnalysisTools.TauTriggerSFs.getTauTriggerSFs import getTauTriggerSFs
tauSFs = getTauTriggerSFs('ditau', 2017, 'tight', 'MVAv2')
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

It is found that there is a slight barrel vs. end cap difference in tau trigger performance. To account for this, there are additional eta-phi adjustments made to the delivered SFs from `getTauTriggerSFs`. In additional to the barrel / end cap separation, we isolate a specific region in the barrel which had well known issues with deal pixel modules and varying tau reconstruction during 2017 data taking (0 < eta < 1.5, phi > 2.8). The eta-phi adjustements are provided in as TH2s in the main root file `data/data/tauTriggerEfficiencies2017.root` and are applied by default in `getTauTriggerSFs`.


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
