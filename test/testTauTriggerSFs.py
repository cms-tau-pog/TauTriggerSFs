#/usr/bin/env python
from __future__ import print_function

from TauAnalysisTools.TauTriggerSFs.getTauTriggerSFs import getTauTriggerSFs

def main():
    print("Testing readout of embedded efficiencies and SFs")
    for year in [2016, 2017, 2018]:
        for trigger in ["ditau", "mutau", "etau",]:
            for wp in ["vvvloose", "vvloose", "vloose", "loose", "medium", "tight", "vtight", "vvtight"]:
                for dm in [0, 1, 10, 11]:
                    sf_provider = getTauTriggerSFs(trigger, year=year, tauWP=wp, wpType="DeepTau", emb_sfs=True)
                    print("Printing embedded trigger efficiencies and SFs for the %s working point of the DeepTau ID "
                          "for the trigger in the %s channel in %i for decay mode %i of the hadronic tau lepton."
                          % (wp, trigger, year, dm))
                    print("pt\tdata eff \t Emb eff \t SF from division \t SF from file \t SF Up \t SF Down")
                    for pt in [45, 80, 120, 400]:
                        eff_emb_data = sf_provider.getTriggerEfficiencyData(pt, 1.3, 0.5, dm);
                        eff_emb = sf_provider.getTriggerEfficiencyMC(pt, 1.3, 0.5, dm);
                        sf_emb = sf_provider.getTriggerScaleFactor(pt, 1.3, 0.5, dm);
                        sf_emb_up = sf_provider.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Up");
                        sf_emb_down = sf_provider.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Down");
                        print("%i\t%f\t%f\t%f\t%f\t%f\t%f" % (pt, eff_emb_data, eff_emb, (eff_emb_data / eff_emb), sf_emb, sf_emb_up, sf_emb_down))

    print("Testing readout of simulated efficiencies and SFs")
    for year in [2016, 2017, 2018]:
        for trigger in ["ditau", "mutau", "etau",]:
            for wp in ["vloose", "loose", "medium", "tight", "vtight", "vvtight"]:
                for dm in [0, 1, 10]:
                    sf_provider = getTauTriggerSFs(trigger, year=year, tauWP=wp, wpType="MVAv2", emb_sfs=False)
                    print("Printing simulated trigger efficiencies and SFs for the %s working point of the MVAv2 ID "
                          "for the trigger in the %s channel in %i for decay mode %i of the hadronic tau lepton."
                          % (wp, trigger, year, dm))
                    print("pt\tdata eff \t Emb eff \t SF from division \t SF from file \t SF Up \t SF Down")
                    for pt in [45, 80, 120, 400]:
                        eff_mc_data = sf_provider.getTriggerEfficiencyData(pt, 1.3, 0.5, dm);
                        eff_mc = sf_provider.getTriggerEfficiencyMC(pt, 1.3, 0.5, dm);
                        sf_mc = sf_provider.getTriggerScaleFactor(pt, 1.3, 0.5, dm);
                        sf_mc_up = sf_provider.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Up");
                        sf_mc_down = sf_provider.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Down");
                        print("%i\t%f\t%f\t%f\t%f\t%f\t%f" % (pt, eff_mc_data, eff_mc, (eff_mc_data / eff_mc), sf_mc, sf_mc_up, sf_mc_down))
    return


if __name__ == "__main__":
    main()
