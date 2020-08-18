#include <iostream>
#include "boost/format.hpp"

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
    static const std::vector<int> decay_modes = { 0, 1, 10, 11 };

    for (std::string year: years)
    {
        const std::string inputFile = (boost::format("%s/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies%s_Embedded_deeptau.root") % std::getenv("CMSSW_BASE") % year).str();
        const std::string inputFileEmb = (boost::format("%s/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies%s_Embedded_deeptau.root") % std::getenv("CMSSW_BASE") % year).str();
        for (std::string chan: channels)
        {
            for (std::string wp: working_points)
            {
                TauTriggerSFs2017 sf_reader = TauTriggerSFs2017(inputFile, inputFileEmb, chan, year, wp, "DeepTau");
                for (int dm: decay_modes)
                {
                    std::cout << "Printing trigger efficiencies and SFs for the " << wp << " working point of the DeepTau ID ";
                    std::cout << "for the trigger in the " << chan << " channel in " << year << " for decay mode " << dm;
                    std::cout << " of the hadronic tau lepton." << std::endl;
                    std::cout << "pt\tdata eff \t Emb eff \t SF from division \t SF from file" << std::endl;
                    for (double pt: test_pts)
                    {
                        double eff_emb_data = sf_reader.getTriggerEfficiencyEmbData(pt, 1.3, 0.5, dm);
                        double eff_emb = sf_reader.getTriggerEfficiencyEmb(pt, 1.3, 0.5, dm);
                        double sf_emb = sf_reader.getTriggerScaleFactorEmb(pt, 1.3, 0.5, dm);
                        std::cout << boost::format("%s\t%s\t%s\t%s\t%s") % pt % eff_emb_data % eff_emb % (eff_emb_data / eff_emb) % sf_emb << std::endl;
                    }
                }
            }
        }
    }
    std::cout << "All readout tests performed successfully." << std::endl;
}
