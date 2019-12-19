#include "TauAnalysisTools/TauTriggerSFs/interface/SFProvider.h"

#include <iostream>
#include <sstream>

int main()
{
    static const std::vector<int> years = { 2016, 2017, 2018 };
    static const std::vector<std::string> channels = { "ditau", "mutau", "etau" };
    static const std::vector<std::string> working_points = {
        "VVVLoose", "VVLoose", "VLoose", "Loose", "Medium", "Tight", "VTight", "VVTight"
    };

    static const std::vector<float> test_pts = { 45, 80, 120, 400 };
    static const std::vector<int> decay_modes = { 0, 1, 10, 11 };
    static const std::vector<int> unc_scales = { -1, 0, 1 };

    try {
        for(int year : years) {
            std::cout << "Testing tau trigger SF for " << year << std::endl;
            std::ostringstream ss_file_name;
            ss_file_name << "TauAnalysisTools/TauTriggerSFs/data/" << year << "_tauTriggerEff_DeepTau2017v2p1.root";
            const std::string file_name = ss_file_name.str();

            for(const auto& channel : channels) {
                for(const auto& wp : working_points) {
                    const tau_trigger::SFProvider sf_provider(file_name, channel, wp);
                    for(float pt : test_pts) {
                        for(int dm : decay_modes) {
                            for (int unc_scale : unc_scales) {
                                const float eff_data = sf_provider.getEfficiencyData(pt, dm, unc_scale);
                                const float eff_mc = sf_provider.getEfficiencyMC(pt, dm, unc_scale);
                                const float sf = sf_provider.getSF(pt, dm, unc_scale);
                                std::cout << "year=" << year << ", channel=" << channel << ", wp=" << wp
                                          << ", pt=" << pt << ", dm=" << dm << ", unc_scale=" << unc_scale
                                          << ", eff_data=" << eff_data << ", eff_mc=" << eff_mc
                                          << ", sf=" << sf << "\n";
                            }
                        }

                    }
                }
            }
        }
    } catch(std::exception& e) {
        std::cout << "ERROR: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "Tau trigger SF tests successfully finished." << std::endl;
    return 0;
}
