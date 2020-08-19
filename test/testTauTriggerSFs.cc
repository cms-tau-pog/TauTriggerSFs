#include <iostream>

#include "TString.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/TauTriggerSFs2017.h"

int main()
{
    static const std::vector<std::string> years = { "2016", "2017", "2018" };
    static const std::vector<std::string> channels = { "ditau", "mutau", "etau" };
    static const std::vector<std::string> working_points = {
        "vvvloose", "vvloose", "vloose", "loose", "medium", "tight", "vtight", "vvtight"
    };
    static const std::vector<double> test_pts = { 45, 80, 120, 400 };
    static std::vector<int> decay_modes = { 0, 1, 10, 11 };

    std::cout << "Testing readout of embedded scale factors." << std::endl;
    for (std::string year: years)
    {
        for (std::string chan: channels)
        {
            for (std::string wp: working_points)
            {
                TauTriggerSFs2017 sf_reader = TauTriggerSFs2017(chan, year, wp, "DeepTau", true);
                for (int dm: decay_modes)
                {
                    std::cout << "Printing embedded trigger efficiencies and SFs for the " << wp << " working point of the DeepTau ID ";
                    std::cout << "for the trigger in the " << chan << " channel in " << year << " for decay mode " << dm;
                    std::cout << " of the hadronic tau lepton." << std::endl;
                    std::cout << "pt \t data eff \t Emb eff \t SF from division \t SF from file \t SF Up \t SF Down" << std::endl;
                    for (double pt: test_pts)
                    {
                        double eff_emb_data = sf_reader.getTriggerEfficiencyData(pt, 1.3, 0.5, dm);
                        double eff_emb = sf_reader.getTriggerEfficiencyMC(pt, 1.3, 0.5, dm);
                        double sf_emb = sf_reader.getTriggerScaleFactor(pt, 1.3, 0.5, dm);
                        double sf_emb_up = sf_reader.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Up");
                        double sf_emb_down = sf_reader.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Down");
                        std::cout << Form("%f \t %f \t %f \t %f \t %f \t %f \t %f", pt, eff_emb_data, eff_emb, (eff_emb_data / eff_emb), sf_emb, sf_emb_up, sf_emb_down) << std::endl;
                    }
                }
            }
        }
    }

    static const std::vector<std::string> mc_working_points = {
        "vloose", "loose", "medium", "tight", "vtight", "vvtight"
    };
    decay_modes.pop_back();
    std::cout << "Testing readout of simulated scale factors." << std::endl;
    for (std::string year: years)
    {
        for (std::string chan: channels)
        {
            for (std::string wp: mc_working_points)
            {
                TauTriggerSFs2017 sf_reader = TauTriggerSFs2017(chan, year, wp, "MVAv2", false);
                for (int dm: decay_modes)
                {
                    std::cout << "Printing simulated trigger efficiencies and SFs for the " << wp << " working point of the MVAv2 ID ";
                    std::cout << "for the trigger in the " << chan << " channel in " << year << " for decay mode " << dm;
                    std::cout << " of the hadronic tau lepton." << std::endl;
                    std::cout << "pt \t data eff \t Emb eff \t SF from division \t SF from file \t SF Up \t SF Down" << std::endl;
                    for (double pt: test_pts)
                    {
                        double eff_mc_data = sf_reader.getTriggerEfficiencyData(pt, 1.3, 0.5, dm);
                        double eff_mc = sf_reader.getTriggerEfficiencyMC(pt, 1.3, 0.5, dm);
                        double sf_mc = sf_reader.getTriggerScaleFactor(pt, 1.3, 0.5, dm);
                        double sf_mc_up = sf_reader.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Up");
                        double sf_mc_down = sf_reader.getTriggerScaleFactorUncert(pt, 1.3, 0.5, dm, "Down");
                        std::cout << Form("%.0f \t %f \t %f \t %f \t %f \t %f \t %f", pt, eff_mc_data, eff_mc, (eff_mc_data / eff_mc), sf_mc, sf_mc_up, sf_mc_down) << std::endl;
                    }
                }
            }
        }
    }

    std::cout << "All readout tests performed successfully." << std::endl;
}
