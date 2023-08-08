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
      hgcalTowerToken_(consumes<l1t::HGCalTowerBxCollection>(iConfig.getParameter<edm::InputTag>("hgcalTowers"))) {
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
  vector<l1tp2::Phase2L1CaloJet> halfBarrelJets, halfHgcalJets;
  halfBarrelJets.clear(); halfHgcalJets.clear();
  vector<l1tp2::Phase2L1CaloJet> allJets;
  allJets.clear();

/*
  for (int k = 0; k < 2; k++) {
    for (int iphi = 0; iphi < nTowerPhi; iphi++) {
      for (int ieta = 0; ieta < nTowerEta/2; ieta++) {
        if(k == 0) temporary[ieta][iphi] = GCTintTowers[ieta][iphi];
        else temporary[ieta][iphi] = GCTintTowers[nTowerEta/2 + ieta][iphi];
        //std::cout<<ieta<<"\t"<<iphi<<"\t"<<GCTintTowers[ieta][iphi]<<std::endl;
      }
    }

    GCTsupertower_t tempST[nSTEta][nSTPhi];
    makeST(temporary, tempST);

    jetInfo jet[10] ;
    halfJets.clear();

    for (int i = 0; i < 10; i++) {
      jet[i] = getRegion(tempST);
      //std::cout<<i<<" th jet energy: "<<jet[i].energy<<std::endl;

      l1tp2::Phase2L1CaloJet tempJet;
      tempJet.setJetEt(jet[i].energy);
      int gctjeteta = jet[i].etaCenter;
      int gctjetphi = jet[i].phiCenter;
      tempJet.setJetIEta(gctjeteta+k*nTowerEta/2);
      tempJet.setJetIPhi(gctjetphi);
      float jeteta = realEta[gctjeteta+k*nTowerEta/2][gctjetphi];
      float jetphi = realPhi[gctjeteta+k*nTowerEta/2][gctjetphi];
      tempJet.setJetEta(jeteta);
      tempJet.setJetPhi(jetphi);
      tempJet.setTowerEt(jet[i].energyMax);
      int gcttowereta = gctjeteta + jet[i].etaMax;
      int gcttowerphi = gctjetphi + jet[i].phiMax;
      tempJet.setTowerIEta(gcttowereta+k*nTowerEta/2);
      tempJet.setTowerIPhi(gcttowerphi);
      float towereta = realEta[gcttowereta+k*nTowerEta/2][gcttowerphi];
      float towerphi = realPhi[gcttowereta+k*nTowerEta/2][gcttowerphi];
      tempJet.setTowerEta(towereta);
      tempJet.setTowerPhi(towerphi);
      // add LorentzVector information
      reco::Candidate::PolarLorentzVector tempJetp4;
      tempJetp4.SetPt(tempJet.jetEt());
      tempJetp4.SetEta(tempJet.jetEta());
      tempJetp4.SetPhi(tempJet.jetPhi());
      tempJetp4.SetM(0.);
      tempJet.setP4(tempJetp4);

      halfJets.push_back(tempJet);
    }

    // Sort the leading 10 jets and take 6
    std::sort(halfJets.begin(), halfJets.end(), compareByEt);
    for (int i = 0; i < 6; i++) {
      allJets.push_back(halfJets.at(i));
    }
  }
*/

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
    int ieta = makeEndcapHwIEta(eta);
    float phi = it->phi();
    int iphi = makeEndcapHwIPhi(phi);
    if(it->etEm() + it->etHad() > 1.) hgcalTowers[ieta][iphi] = it->etEm() + it->etHad(); // suppress 1 GeV towers
  }

  //Assign ETs to each eta-half of the endcap region (18x72)
  //Then we create 6x24 super towers in each eta-half
  //Find 6 jets in each eta-half

  float temporary_hgcal[nHgcalEta/2][nHgcalPhi];

  for (int k = 0; k < 2; k++) {
    halfBarrelJets.clear();
    halfHgcalJets.clear();
    jetInfo jet[20] ;

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

    std::sort(halfBarrelJets.begin(), halfBarrelJets.end(), compareByEt);
    for (size_t i = 0; i < halfBarrelJets.size(); i++) {
      allJets.push_back(halfBarrelJets.at(i));
      if(i==5) break;
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

    std::sort(halfHgcalJets.begin(), halfHgcalJets.end(), compareByEt);
    for (size_t i = 0; i < halfHgcalJets.size(); i++) {
      allJets.push_back(halfHgcalJets.at(i));
      if(i==5) break;
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
