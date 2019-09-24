#ifndef TauTriggerSFs2017_h
#define TauTriggerSFs2017_h

/** \class TauTriggerSFs2017
 *
 * Class to access information on tau trigger efficiencies in data and MC and related data/MC scale-factors.
 * The trigger efficiencies are parametrized as function of pT, eta, and phi of the offline reconstructed tau,
 * cf. https://indico.cern.ch/event/700928/contributions/2883477/attachments/1596523/2529036/Ruggles_TauTriggers_TauPOG_20180207_v4.pdf
 *
 * \authors Tyler Ruggles, Wisconsin; Christian Veelken, Tallin
 *
 * \updated February2019 Francesco Brivio, Milano-Bicocca; Chiara Amendola, LLR
 * cf. https://indico.cern.ch/event/799374/contributions/3323191/attachments/1797874/2931826/TauTrigger2017SFv3_TauID_hsert.pdf
 *
 */

#include <TFile.h> // TFile
#include <TH1.h> // TH1
#include <TH2.h> // TH2
#include <TF1.h> // TF1

#include <string> // std::string
#include <map>    // std::map

class TauTriggerSFs2017
{
public:

  TauTriggerSFs2017(const std::string& inputFileName, const std::string& inputFileNameKIT, const std::string& trigger, const std::string& year, const std::string& tauWP = "medium", const std::string& wpType = "MVAv2");
  ~TauTriggerSFs2017();

  // Return the data efficiency or the +/- 1 sigma uncertainty shifted efficiency
  double getTriggerEfficiencyData(double pt, double eta, double phi, int dm) const;           // Nominal data efficiency
  double getTriggerEfficiencyDataUncertUp(double pt, double eta, double phi, int dm) const;   // Data efficiency +1 sigma uncertainty
  double getTriggerEfficiencyDataUncertDown(double pt, double eta, double phi, int dm) const; // Data efficiency -1 sigma uncertainty

  // Return the data efficiency or the +/- 1 sigma uncertainty shifted efficiency
  double getTriggerEfficiencyKITData(double pt, double eta, double phi, int dm) const;           // Nominal data efficiency
  double getTriggerEfficiencyKITDataUncertUp(double pt, double eta, double phi, int dm) const;   // Data efficiency +1 sigma uncertainty
  double getTriggerEfficiencyKITDataUncertDown(double pt, double eta, double phi, int dm) const; // Data efficiency -1 sigma uncertainty

  // Return the MC efficiency or the +/- 1 sigma uncertainty shifted efficiency
  double getTriggerEfficiencyMC(double pt, double eta, double phi, int dm) const;           // Nominal MC efficiency
  double getTriggerEfficiencyMCUncertUp(double pt, double eta, double phi, int dm) const;   // MC efficiency +1 sigma uncertainty
  double getTriggerEfficiencyMCUncertDown(double pt, double eta, double phi, int dm) const; // MC efficiency -1 sigma uncertainty

  // Return the EMB efficiency or the +/- 1 sigma uncertainty shifted efficiency
  double getTriggerEfficiencyEMB(double pt, double eta, double phi, int dm) const;           // Nominal EMB efficiency
  double getTriggerEfficiencyEMBUncertUp(double pt, double eta, double phi, int dm) const;   // EMB efficiency +1 sigma uncertainty
  double getTriggerEfficiencyEMBUncertDown(double pt, double eta, double phi, int dm) const; // EMB efficiency -1 sigma uncertainty

  // Return the Scale Factor or the +/- 1 sigma shifter Scale Factor
  double getTriggerScaleFactor(double pt, double eta, double phi, int dm) const;                           // Nominal Scale Factor
  double getTriggerScaleFactorUncert(double pt, double eta, double phi, int dm, const std::string& uncert) const; // Shifted Scale Factor

  // Return the EMB Scale Factor or the +/- 1 sigma shifter Scale Factor
  double getTriggerScaleFactorEMB(double pt, double eta, double phi, int dm) const;                           // Nominal Scale Factor
  double getTriggerScaleFactorEMBUncert(double pt, double eta, double phi, int dm, const std::string& uncert) const; // Shifted Scale Factor

protected:
  std::string inputFileName_;
  TFile* inputFile_;
  std::string inputFileNameKIT_;
  TFile* inputFileKIT_;

  std::string trigger_;
  std::string year_;
  std::string tauWP_;
  std::string wpType_;

  std::map<int, TF1*> fitDataMap_;
  std::map<int, TF1*> fitKITDataMap_;
  std::map<int, TF1*> fitMCMap_;
  std::map<int, TF1*> fitEMBMap_;
  std::map<int, TH1*> fitUncDataMap_;
  std::map<int, TH1*> fitUncKITDataMap_;
  std::map<int, TH1*> fitUncMCMap_;
  std::map<int, TH1*> fitUncEMBMap_;
  std::map<int, TH2*> effEtaPhiDataMap_;
  std::map<int, TH2*> effEtaPhiKITDataMap_;
  std::map<int, TH2*> effEtaPhiMCMap_;
  std::map<int, TH2*> effEtaPhiEMBMap_;
  std::map<int, TH2*> effEtaPhiAvgDataMap_;
  std::map<int, TH2*> effEtaPhiAvgKITDataMap_;
  std::map<int, TH2*> effEtaPhiAvgMCMap_;
  std::map<int, TH2*> effEtaPhiAvgEMBMap_;
};

#endif // TauTriggerSFs2017_h
