#/usr/bin/env python
from __future__ import print_function

from TauAnalysisTools.TauTriggerSFs.getTauTriggerSFs import getTauTriggerSFs

def main():
    for year in [2016, 2017, 2018]:
        for trigger in ["ditau", "mutau", "etau",]:
            for wp in ["vvvloose", "vvloose", "vloose", "loose", "medium", "tight", "vtight", "vvtight"]:
                for dm in [0, 1, 10, 11]:
                    sf_provider = getTauTriggerSFs(trigger, year=year, tauWP=wp, wpType="DeepTau", emb_sfs=True)
                    print("Printing trigger efficiencies and SFs for the %s working point of the DeepTau ID "
                          "for the trigger in the %s channel in %i for decay mode %i of the hadronic tau lepton."
                          % (wp, trigger, year, dm))
                    print("pt\tdata eff \t Emb eff \t SF from division \t SF from file")
                    for pt in [45, 80, 120, 400]:
                        eff_emb_data = sf_provider.getTriggerEfficiencyData(pt, 1.3, 0.5, dm);
                        eff_emb = sf_provider.getTriggerEfficiencyMC(pt, 1.3, 0.5, dm);
                        sf_emb = sf_provider.getTriggerScaleFactor(pt, 1.3, 0.5, dm);
                        print("%i\t%f\t%f\t%f\t%f" % (pt, eff_emb_data, eff_emb, (eff_emb_data / eff_emb), sf_emb))
    return


if __name__ == "__main__":
    main()
