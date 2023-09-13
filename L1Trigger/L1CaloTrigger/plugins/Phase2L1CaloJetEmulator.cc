// -*- C++ -*-
//
// Package:    L1Trigger/L1CaloTrigger
// Class:      Phase2L1CaloJetEmulator
//
/**\class Phase2L1CaloJetEmulator Phase2L1CaloJetEmulator.cc L1Trigger/L1CaloTrigger/plugins/Phase2L1CaloJetEmulator.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Pallabi Das
//         Created:  Tue, 11 Apr 2023 11:27:33 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/L1TCalorimeterPhase2/interface/CaloCrystalCluster.h"
#include "DataFormats/L1TCalorimeterPhase2/interface/CaloTower.h"
#include "DataFormats/L1TCalorimeterPhase2/interface/CaloPFCluster.h"
#include "DataFormats/L1TCalorimeterPhase2/interface/Phase2L1CaloJet.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/L1THGCal/interface/HGCalTower.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "SimDataFormats/CaloHit/interface/PCaloHitContainer.h"
#include "CalibFormats/CaloTPG/interface/CaloTPGTranscoder.h"
#include "CalibFormats/CaloTPG/interface/CaloTPGRecord.h"
#include "L1Trigger/L1TCalorimeter/interface/CaloTools.h"

#include <ap_int.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdio.h>
#include "L1Trigger/L1CaloTrigger/interface/Phase2L1CaloJetEmulator.h"

//
// class declaration
//

class Phase2L1CaloJetEmulator : public edm::stream::EDProducer<> {
public:
  explicit Phase2L1CaloJetEmulator(const edm::ParameterSet&);
  ~Phase2L1CaloJetEmulator() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  // ----------member data ---------------------------
  edm::EDGetTokenT<l1tp2::CaloTowerCollection> caloTowerToken_;
  edm::EDGetTokenT<l1t::HGCalTowerBxCollection> hgcalTowerToken_;
  edm::EDGetTokenT<HcalTrigPrimDigiCollection> hfToken_;
  edm::ESGetToken<CaloTPGTranscoder, CaloTPGRecord> decoderTag_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
Phase2L1CaloJetEmulator::Phase2L1CaloJetEmulator(const edm::ParameterSet& iConfig)
    : caloTowerToken_(consumes<l1tp2::CaloTowerCollection>(iConfig.getParameter<edm::InputTag>("gctFullTowers"))),
      hgcalTowerToken_(consumes<l1t::HGCalTowerBxCollection>(iConfig.getParameter<edm::InputTag>("hgcalTowers"))),
      hfToken_(consumes<HcalTrigPrimDigiCollection>(iConfig.getParameter<edm::InputTag>("hcalDigis"))),
      decoderTag_(esConsumes<CaloTPGTranscoder, CaloTPGRecord>(edm::ESInputTag("", ""))) {
  produces<l1tp2::Phase2L1CaloJetCollection>("GCTJet");
}

Phase2L1CaloJetEmulator::~Phase2L1CaloJetEmulator() {}

//
// member functions
//

// ------------ method called to produce the data  ------------
void Phase2L1CaloJetEmulator::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  std::unique_ptr<l1tp2::Phase2L1CaloJetCollection> jetCands(make_unique<l1tp2::Phase2L1CaloJetCollection>());

  edm::Handle<std::vector<l1tp2::CaloTower>> caloTowerCollection;
  if (!iEvent.getByToken(caloTowerToken_, caloTowerCollection))
    edm::LogError("Phase2L1CaloJetEmulator") << "Failed to get towers from caloTowerCollection!";

  iEvent.getByToken(caloTowerToken_, caloTowerCollection);
  float GCTintTowers[nTowerEta][nTowerPhi];
  float realEta[nTowerEta][nTowerPhi];
  float realPhi[nTowerEta][nTowerPhi];
  for (const l1tp2::CaloTower& i : *caloTowerCollection) {

    int ieta = i.towerIEta();
    int iphi = i.towerIPhi();
    if(i.ecalTowerEt() > 1.) GCTintTowers[ieta][iphi] = i.ecalTowerEt(); // suppress <= 1 GeV towers
    else GCTintTowers[ieta][iphi] = 0;
    //GCTintTowers[ieta][iphi] = i.ecalTowerEt();
    realEta[ieta][iphi] = i.towerEta();
    realPhi[ieta][iphi] = i.towerPhi();
  }

  //Assign ETs to each eta-half of the barrel region (17x72 --> 18x72 to be able to make 3x3 super towers)
  //Then we create 6x24 super towers in each eta-half
  //Find 6 jets in each eta-half

  float temporary[nTowerEta/2][nTowerPhi];

  // HGCal info
  edm::Handle<l1t::HGCalTowerBxCollection> hgcalTowerCollection;
  if (!iEvent.getByToken(hgcalTowerToken_, hgcalTowerCollection))
    edm::LogError("Phase2L1CaloJetEmulator") << "Failed to get towers from hgcalTowerCollection!";
  l1t::HGCalTowerBxCollection hgcalTowerColl;
  iEvent.getByToken(hgcalTowerToken_, hgcalTowerCollection);
  hgcalTowerColl = (*hgcalTowerCollection.product());
  float hgcalTowers[nHgcalEta][nHgcalPhi];
  float hgcalEta[nHgcalEta][nHgcalPhi];
  float hgcalPhi[nHgcalEta][nHgcalPhi];

  for(int iphi = 0; iphi < nHgcalPhi; iphi++) {
    for(int ieta = 0; ieta < nHgcalEta; ieta++) {
      hgcalTowers[ieta][iphi] = 0;
      if(ieta < nHgcalEta/2) hgcalEta[ieta][iphi] = -2.95775 + ieta*0.0845;
      else hgcalEta[ieta][iphi] = 1.52125 + (ieta-18)*0.0845;
      hgcalPhi[ieta][iphi] = - M_PI + (iphi*M_PI/36) + (M_PI/72);
    }
  }
  
  for (auto it = hgcalTowerColl.begin(0); it != hgcalTowerColl.end(0); it++) {
    float eta = it->eta();
    int ieta;
    if(eta < 0) ieta = 17 - it->id().iEta();
    else ieta = 18 + it->id().iEta();
    int iphi = it->id().iPhi();
    if(it->etEm() + it->etHad() > 1.) hgcalTowers[ieta][iphi] = it->etEm() + it->etHad(); // suppress <= 1 GeV towers
  }

  //Assign ETs to each eta-half of the endcap region (18x72)
  //Then we create 6x24 super towers in each eta-half
  //Find 6 jets in each eta-half

  float temporary_hgcal[nHgcalEta/2][nHgcalPhi];

  // HF info
  edm::Handle<HcalTrigPrimDigiCollection> hfHandle;
  if (!iEvent.getByToken(hfToken_, hfHandle))
    edm::LogError("Phase2L1CaloJetEmulator") << "Failed to get HcalTrigPrimDigi for HF!";
  iEvent.getByToken(hfToken_, hfHandle);
  float hfTowers[nHfEta][nHfPhi];
  float hfEta[nHfEta][nHfPhi];
  float hfPhi[nHfEta][nHfPhi];

  for(int iphi = 0; iphi < nHfPhi; iphi++) {
    for(int ieta = 0; ieta < nHfEta; ieta++) {
      hfTowers[ieta][iphi] = 0;
      int temp = ieta;
      if(ieta < 12) temp = ieta - 41;
      else temp = ieta - 12 + 30;
      hfEta[ieta][iphi] = l1t::CaloTools::towerEta(temp);
      hfPhi[ieta][iphi] = - M_PI + (iphi*M_PI/36) + (M_PI/72);
      //hfPhi[ieta][iphi] = l1t::CaloTools::towerPhi(temp, iphi);
      //std::cout<<hfEta[ieta][iphi]<<"\t"<<hfPhi[ieta][iphi]<<std::endl;
    }
  }

  const auto& decoder = iSetup.getData(decoderTag_);
  for (const auto& hit : *hfHandle.product()) {
    double et = decoder.hcaletValue(hit.id(), hit.t0());
    //std::cout<<hit.id().ieta()<<"\t"<<hit.id().iphi()<<"\t"<<et<<std::endl;
    int ieta = 0;
    if (abs(hit.id().ieta()) < l1t::CaloTools::kHFBegin) continue;
    if (abs(hit.id().ieta()) > l1t::CaloTools::kHFEnd) continue;
    if (hit.id().ieta() <= -30) {
      ieta = hit.id().ieta() + 41;
    }
    else if (hit.id().ieta() >= 30) {
      ieta = 12 + (hit.id().ieta() - 30);
    }
    //int iphi = hit.id().iphi();
    int iphi = 0;
    if (hit.id().iphi() <= 36) iphi = hit.id().iphi() + 35;
    else if (hit.id().iphi() > 36) iphi = hit.id().iphi() - 37;
    if(et > 1.) hfTowers[ieta][iphi] = et; // suppress <= 1 GeV towers
  }

  //Assign ETs to each eta-half of the endcap region (12x72)
  //Then we create 4x24 super towers in each eta-half
  //Find 6 jets in each eta-half

  float temporary_hf[nHfEta/2][nHfPhi];

  //Begin creating jets

  vector<l1tp2::Phase2L1CaloJet> halfBarrelJets, halfHgcalJets, halfHfJets;
  halfBarrelJets.clear(); halfHgcalJets.clear(); halfHfJets.clear();
  vector<l1tp2::Phase2L1CaloJet> allJets;
  allJets.clear();

  for (int k = 0; k < 2; k++) {
    halfBarrelJets.clear();
    halfHgcalJets.clear();
    halfHfJets.clear();
    jetInfo jet[30] ;

    // BARREL
    for (int iphi = 0; iphi < nTowerPhi; iphi++) {
      for (int ieta = 0; ieta < nTowerEta/2; ieta++) {
        if(k == 0) temporary[ieta][iphi] = GCTintTowers[ieta][iphi];
        else temporary[ieta][iphi] = GCTintTowers[nTowerEta/2 + ieta][iphi];
      }
    }

    GCTsupertower_t tempST[nSTEta][nSTPhi];
    makeST(temporary, tempST);

    for (int i = 0; i < 10; i++) {
      jet[i] = getRegion(tempST);
      l1tp2::Phase2L1CaloJet tempJet;
      tempJet.setJetEt(jet[i].energy);
      tempJet.setTauEt(jet[i].tauEt);
      int gctjeteta = jet[i].etaCenter;
      int gctjetphi = jet[i].phiCenter;
      tempJet.setJetIEta(gctjeteta+k*nTowerEta/2);
      tempJet.setJetIPhi(gctjetphi);
      float jeteta = realEta[gctjeteta+k*nTowerEta/2][gctjetphi];
      float jetphi = realPhi[gctjeteta+k*nTowerEta/2][gctjetphi];
      tempJet.setJetEta(jeteta);
      tempJet.setJetPhi(jetphi);
      tempJet.setTowerEt(jet[i].energyMax);
      int gcttowereta = jet[i].etaMax;
      int gcttowerphi = jet[i].phiMax;
      tempJet.setTowerIEta(gcttowereta+k*nTowerEta/2);
      tempJet.setTowerIPhi(gcttowerphi);
      float towereta = realEta[gcttowereta+k*nTowerEta/2][gcttowerphi];
      float towerphi = realPhi[gcttowereta+k*nTowerEta/2][gcttowerphi];
      tempJet.setTowerEta(towereta);
      tempJet.setTowerPhi(towerphi);
      reco::Candidate::PolarLorentzVector tempJetp4;
      tempJetp4.SetPt(tempJet.jetEt());
      tempJetp4.SetEta(tempJet.jetEta());
      tempJetp4.SetPhi(tempJet.jetPhi());
      tempJetp4.SetM(0.);
      tempJet.setP4(tempJetp4);

      if(jet[i].energy > 0.) halfBarrelJets.push_back(tempJet);
    }

    // ENDCAP
    for (int iphi = 0; iphi < nHgcalPhi; iphi++) {
      for (int ieta = 0; ieta < nHgcalEta/2; ieta++) {
        if(k == 0) temporary_hgcal[ieta][iphi] = hgcalTowers[ieta][iphi];
        else temporary_hgcal[ieta][iphi] = hgcalTowers[nHgcalEta/2 + ieta][iphi];
      }
    }

    GCTsupertower_t tempST_hgcal[nSTEta][nSTPhi];
    makeST_hgcal(temporary_hgcal, tempST_hgcal);
    for (int i = 10; i < 20; i++) {
      jet[i] = getRegion(tempST_hgcal);
      l1tp2::Phase2L1CaloJet tempJet;
      tempJet.setJetEt(jet[i].energy);
      tempJet.setTauEt(jet[i].tauEt);
      int hgcaljeteta = jet[i].etaCenter;
      int hgcaljetphi = jet[i].phiCenter;
      tempJet.setJetIEta(hgcaljeteta+k*nHgcalEta/2);
      tempJet.setJetIPhi(hgcaljetphi);
      float jeteta = hgcalEta[hgcaljeteta+k*nHgcalEta/2][hgcaljetphi];
      float jetphi = hgcalPhi[hgcaljeteta+k*nHgcalEta/2][hgcaljetphi];
      tempJet.setJetEta(jeteta);
      tempJet.setJetPhi(jetphi);
      tempJet.setTowerEt(jet[i].energyMax);
      int hgcaltowereta = jet[i].etaMax;
      int hgcaltowerphi = jet[i].phiMax;
      tempJet.setTowerIEta(hgcaltowereta+k*nHgcalEta/2);
      tempJet.setTowerIPhi(hgcaltowerphi);
      float towereta = hgcalEta[hgcaltowereta+k*nHgcalEta/2][hgcaltowerphi];
      float towerphi = hgcalPhi[hgcaltowereta+k*nHgcalEta/2][hgcaltowerphi];
      tempJet.setTowerEta(towereta);
      tempJet.setTowerPhi(towerphi);
      reco::Candidate::PolarLorentzVector tempJetp4;
      tempJetp4.SetPt(tempJet.jetEt());
      tempJetp4.SetEta(tempJet.jetEta());
      tempJetp4.SetPhi(tempJet.jetPhi());
      tempJetp4.SetM(0.);
      tempJet.setP4(tempJetp4);

      if(jet[i].energy > 0.) halfHgcalJets.push_back(tempJet);
    }

    // HF
    for (int iphi = 0; iphi < nHfPhi; iphi++) {
      for (int ieta = 0; ieta < nHfEta/2; ieta++) {
        if(k == 0) temporary_hf[ieta][iphi] = hfTowers[ieta][iphi];
        else temporary_hf[ieta][iphi] = hfTowers[nHfEta/2 + ieta][iphi];
      }
    }

    GCTsupertower_t tempST_hf[nSTEta][nSTPhi];
    makeST_hf(temporary_hf, tempST_hf);
    for (int i = 20; i < 30; i++) {
      jet[i] = getRegion(tempST_hf);
      l1tp2::Phase2L1CaloJet tempJet;
      tempJet.setJetEt(jet[i].energy);
      tempJet.setTauEt(jet[i].tauEt);
      int hfjeteta = jet[i].etaCenter;
      int hfjetphi = jet[i].phiCenter;
      tempJet.setJetIEta(hfjeteta+k*nHfEta/2);
      tempJet.setJetIPhi(hfjetphi);
      float jeteta = hfEta[hfjeteta+k*nHfEta/2][hfjetphi];
      float jetphi = hfPhi[hfjeteta+k*nHfEta/2][hfjetphi];
      tempJet.setJetEta(jeteta);
      tempJet.setJetPhi(jetphi);
      tempJet.setTowerEt(jet[i].energyMax);
      int hftowereta = jet[i].etaMax;
      int hftowerphi = jet[i].phiMax;
      tempJet.setTowerIEta(hftowereta+k*nHfEta/2);
      tempJet.setTowerIPhi(hftowerphi);
      float towereta = hfEta[hftowereta+k*nHfEta/2][hftowerphi];
      float towerphi = hfPhi[hftowereta+k*nHfEta/2][hftowerphi];
      tempJet.setTowerEta(towereta);
      tempJet.setTowerPhi(towerphi);
      reco::Candidate::PolarLorentzVector tempJetp4;
      tempJetp4.SetPt(tempJet.jetEt());
      tempJetp4.SetEta(tempJet.jetEta());
      tempJetp4.SetPhi(tempJet.jetPhi());
      tempJetp4.SetM(0.);
      tempJet.setP4(tempJetp4);

      if(jet[i].energy > 0.) halfHfJets.push_back(tempJet);
    }

    // Stitching:
    // if the jet eta is at the boundary: for HB it should be within 0-1 in -ve eta, 32-33 in +ve eta; for HE it should be within 0-1/16-17 in -ve eta, 34-35/18-19 in +ve eta; for HF it should be within 10-11 in -ve eta, 12-13 in +ve eta
    // then get the phi of that jet and check if there is a neighbouring jet with the same phi, then merge to the jet that has higher ET
    // in both eta/phi allow a maximum of one tower between jet centers for stitching

    for (size_t i = 0; i < halfHgcalJets.size(); i++) {
      if (halfHgcalJets.at(i).jetIEta() > 15 && halfHgcalJets.at(i).jetIEta() < 20) {
        float hgcal_ieta = k*nTowerEta + halfHgcalJets.at(i).jetIEta();
        for (size_t j = 0; j < halfBarrelJets.size(); j++) {
          float barrel_ieta = nHgcalEta/2 + halfBarrelJets.at(j).jetIEta();
          if (abs(barrel_ieta - hgcal_ieta) < 3 && abs(halfBarrelJets.at(j).jetIPhi() - halfHgcalJets.at(i).jetIPhi()) < 3) {
            float totalet = halfBarrelJets.at(j).jetEt() + halfHgcalJets.at(i).jetEt();
            float totalTauEt = halfBarrelJets.at(j).tauEt() + halfHgcalJets.at(i).tauEt();
            if (halfBarrelJets.at(j).jetEt() > halfHgcalJets.at(i).jetEt()) {
              halfHgcalJets.at(i).setJetEt(0.);
              halfHgcalJets.at(i).setTauEt(0.);
              halfBarrelJets.at(j).setJetEt(totalet);
              halfBarrelJets.at(j).setTauEt(totalTauEt);
              reco::Candidate::PolarLorentzVector tempJetp4;
              tempJetp4.SetPt(totalet);
              tempJetp4.SetEta(halfBarrelJets.at(j).jetEta());
              tempJetp4.SetPhi(halfBarrelJets.at(j).jetPhi());
              tempJetp4.SetM(0.);
              halfBarrelJets.at(j).setP4(tempJetp4);
            }
            else {
              halfHgcalJets.at(i).setJetEt(totalet);
              halfHgcalJets.at(i).setTauEt(totalTauEt);
              halfBarrelJets.at(j).setJetEt(0.);
              halfBarrelJets.at(j).setTauEt(0.);
              reco::Candidate::PolarLorentzVector tempJetp4;
              tempJetp4.SetPt(totalet);
              tempJetp4.SetEta(halfHgcalJets.at(i).jetEta());
              tempJetp4.SetPhi(halfHgcalJets.at(i).jetPhi());
              tempJetp4.SetM(0.);
              halfHgcalJets.at(i).setP4(tempJetp4);
            }
          }
        }
      }
      else if (halfHgcalJets.at(i).jetIEta() < 2 || halfHgcalJets.at(i).jetIEta() > 33) {
        float hgcal_ieta = k*nTowerEta + nHfEta/2 + halfHgcalJets.at(i).jetIEta();
        for (size_t j = 0; j < halfHfJets.size(); j++) {
          float hf_ieta = k*nTowerEta + k*nHgcalEta + halfHfJets.at(j).jetIEta();
          if(abs(hgcal_ieta - hf_ieta) < 3 && abs(halfHfJets.at(j).jetIPhi() - halfHgcalJets.at(i).jetIPhi()) < 3) {
            float totalet = halfHfJets.at(j).jetEt() + halfHgcalJets.at(i).jetEt();
            float totalTauEt = halfHfJets.at(j).tauEt() + halfHgcalJets.at(i).tauEt();
            if (halfHfJets.at(j).jetEt() > halfHgcalJets.at(i).jetEt()) {
              halfHgcalJets.at(i).setJetEt(0.);
              halfHgcalJets.at(i).setTauEt(0.);
              halfHfJets.at(j).setJetEt(totalet);
              halfHfJets.at(j).setTauEt(totalTauEt);
              reco::Candidate::PolarLorentzVector tempJetp4;
              tempJetp4.SetPt(totalet);
              tempJetp4.SetEta(halfHfJets.at(j).jetEta());
              tempJetp4.SetPhi(halfHfJets.at(j).jetPhi());
              tempJetp4.SetM(0.);
              halfHfJets.at(j).setP4(tempJetp4);
            }
            else {
              halfHgcalJets.at(i).setJetEt(totalet);
              halfHgcalJets.at(i).setTauEt(totalTauEt);
              halfHfJets.at(j).setJetEt(0.);
              halfHfJets.at(j).setTauEt(0.);
              reco::Candidate::PolarLorentzVector tempJetp4;
              tempJetp4.SetPt(totalet);
              tempJetp4.SetEta(halfHgcalJets.at(i).jetEta());
              tempJetp4.SetPhi(halfHgcalJets.at(i).jetPhi());
              tempJetp4.SetM(0.);
              halfHgcalJets.at(i).setP4(tempJetp4);
            }
          }
        }
      }
    }

    std::sort(halfBarrelJets.begin(), halfBarrelJets.end(), compareByEt);
    for (size_t i = 0; i < halfBarrelJets.size(); i++) {
      if (halfBarrelJets.at(i).jetEt() > 0. && i < 6) allJets.push_back(halfBarrelJets.at(i));
    }

    std::sort(halfHgcalJets.begin(), halfHgcalJets.end(), compareByEt);
    for (size_t i = 0; i < halfHgcalJets.size(); i++) {
      if (halfHgcalJets.at(i).jetEt() > 0. && i < 6) allJets.push_back(halfHgcalJets.at(i));
    }

    std::sort(halfHfJets.begin(), halfHfJets.end(), compareByEt);
    for (size_t i = 0; i < halfHfJets.size(); i++) {
      if (halfHfJets.at(i).jetEt() > 0. && i < 6) allJets.push_back(halfHfJets.at(i));
    }

  }

  std::sort(allJets.begin(), allJets.end(), compareByEt);
  for (size_t i = 0; i < allJets.size(); i++) {
    jetCands->push_back(allJets.at(i));
  }  

  iEvent.put(std::move(jetCands), "GCTJet");
}

// ------------ method called when starting to processes a run  ------------
/*
void
Phase2L1CaloJetEmulator::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void
Phase2L1CaloJetEmulator::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void
Phase2L1CaloJetEmulator::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
Phase2L1CaloJetEmulator::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void Phase2L1CaloJetEmulator::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Phase2L1CaloJetEmulator);
