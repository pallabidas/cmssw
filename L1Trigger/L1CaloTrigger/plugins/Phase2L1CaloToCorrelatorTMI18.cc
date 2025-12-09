/* AS */

// system include files
#include <ap_int.h>
#include <array>
#include <cmath>
#include <typeinfo>
// #include <cstdint>
#include <iostream>
#include <fstream>
#include <memory>
#include <vector>
#include <TLorentzVector.h>
#ifdef __MAKECINT__
#pragma link C++ class vector<TLorentzVector>+;
#endif

// user include files
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "L1Trigger/L1CaloTrigger/interface/Phase2L1CaloToCorrelatorTMI18.h"

#include "DataFormats/L1TCalorimeterPhase2/interface/DigitizedClusterCorrelatorTMI18.h"
#include "DataFormats/L1TCalorimeterPhase2/interface/DigitizedPFClusterCorrelatorTMI18.h"
#include "DataFormats/L1TCalorimeterPhase2/interface/DigitizedCaloToCorrelatorTMI18.h"


class Phase2L1CaloToCorrelatorTMI18 : public edm::stream::EDProducer<> {
public:
  explicit Phase2L1CaloToCorrelatorTMI18(const edm::ParameterSet&);
  ~Phase2L1CaloToCorrelatorTMI18() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;
  edm::EDGetTokenT<l1tp2::DigitizedClusterCorrelatorCollectionTMI18> egDigitizedToCorrelatorTMI18Src_ ;
  edm::EDGetTokenT<l1tp2::DigitizedPFClusterCorrelatorCollectionTMI18> pfDigitizedToCorrelatorTMI18Src_ ;

};


Phase2L1CaloToCorrelatorTMI18::Phase2L1CaloToCorrelatorTMI18( const edm::ParameterSet & cfg ) :
  egDigitizedToCorrelatorTMI18Src_(consumes<l1tp2::DigitizedClusterCorrelatorCollectionTMI18>(cfg.getParameter<edm::InputTag>("egtocorr18"))),
  pfDigitizedToCorrelatorTMI18Src_(consumes<l1tp2::DigitizedPFClusterCorrelatorCollectionTMI18>(cfg.getParameter<edm::InputTag>("pftocorr18")))
{
produces<l1tp2::DigitizedCaloToCorrelatorCollectionTMI18>("DigitizedCaloToCorrelatorTMI18");
 }

void Phase2L1CaloToCorrelatorTMI18::produce( edm::Event& evt, const edm::EventSetup& es )
 {
	 using namespace edm;

  std::unique_ptr<l1tp2::DigitizedCaloToCorrelatorCollectionTMI18> caloCandsTMI18(std::make_unique<l1tp2::DigitizedCaloToCorrelatorCollectionTMI18>());

  int cntr03pos = 0 ;
  int cntr03neg = 0 ;
  int cntr01pos = 0 ;
  int cntr01neg = 0 ;

  int cntr13pos = 0 ;
  int cntr13neg = 0 ;
  int cntr11pos = 0 ;
  int cntr11neg = 0 ;

  int cntr23pos = 0 ;
  int cntr23neg = 0 ;
  int cntr21pos = 0 ;
  int cntr21neg = 0 ;

  ap_uint<64> mydata = 0 ;
  ap_uint<64> dataToCL1Card0[162] = {0} ;
  ap_uint<64> dataToCL1Card1[162] = {0} ;
  ap_uint<64> dataToCL1Card2[162] = {0} ;

  edm::Handle<l1tp2::DigitizedPFClusterCorrelatorCollectionTMI18> pftocorr18;
  if(evt.getByToken(pfDigitizedToCorrelatorTMI18Src_, pftocorr18)) {

//	  std::cout << " PF SizeOK:" << pftocorr18->size() <<  std::endl;

    for(const auto & pf : *pftocorr18){


       mydata = pf.data() ;

       if(pf.slrNumber() == 3 && pf.etaPositive() == 1) goto slr3posp ;
       if(pf.slrNumber() == 3 && pf.etaPositive() == 0) goto slr3negp ;
       if(pf.slrNumber() == 1 && pf.etaPositive() == 1) goto slr1posp ;
       if(pf.slrNumber() == 1 && pf.etaPositive() == 0) goto slr1negp ;

slr3posp:  ;

       if(pf.cardNumber() == 0 && cntr03pos < 24){
       dataToCL1Card0[17+cntr03pos] = mydata ;  
       cntr03pos++ ;  
	goto fillendp ;
       } 
       if(pf.cardNumber() == 1 && cntr13pos < 24){
       dataToCL1Card1[17+cntr13pos] = mydata ;
       cntr13pos++ ;
	goto fillendp ;
       } 
       if(pf.cardNumber() == 2 && cntr23pos < 24){
       dataToCL1Card2[17+cntr23pos] = mydata ;
       cntr23pos++ ;
	goto fillendp ;
       } 
	goto fillendp ;

slr3negp:  ;

       if(pf.cardNumber() == 0 && cntr03neg < 24){
       dataToCL1Card0[57+cntr03neg] = mydata ;
       cntr03neg++ ;
	goto fillendp ;
       } 
       if(pf.cardNumber() == 1 && cntr13neg < 24){
       dataToCL1Card1[57+cntr13neg] = mydata ;
       cntr13neg++ ;
	goto fillendp ;
       } 
       if(pf.cardNumber() == 2 && cntr23neg < 24){
       dataToCL1Card2[57+cntr23neg] = mydata ;
       cntr23neg++ ;
	goto fillendp ;
       } 
	goto fillendp ;

slr1posp:  ;


       if(pf.cardNumber() == 0 && cntr01pos < 24){
       dataToCL1Card0[81+17+cntr01pos] = mydata ;
       cntr01pos++ ;
	goto fillendp ;
       } 
       if(pf.cardNumber() == 1 && cntr11pos < 24){
       dataToCL1Card1[81+17+cntr11pos] = mydata ;
       cntr11pos++ ;
	goto fillendp ;
       } 
       if(pf.cardNumber() == 2 && cntr21pos < 24){
       dataToCL1Card2[81+17+cntr21pos] = mydata ;
       cntr21pos++ ;
	goto fillendp ;
       } 
	goto fillendp ;

slr1negp:  ;

       if(pf.cardNumber() == 0 && cntr01neg < 24){
       dataToCL1Card0[81+57+cntr01neg] = mydata ;
       cntr01neg++ ;
	goto fillendp ;
       } 
       if(pf.cardNumber() == 1 && cntr11neg < 24){
       dataToCL1Card1[81+57+cntr11neg] = mydata ;
       cntr11neg++ ;
	goto fillendp ;
       } 
       if(pf.cardNumber() == 2 && cntr21neg < 24){
       dataToCL1Card2[81+57+cntr21neg] = mydata ;
       cntr21neg++ ;
	goto fillendp ; 
       } 
       
fillendp:  ;

  }}
  

  cntr03pos = 0 ;
  cntr03neg = 0 ;
  cntr01pos = 0 ;
  cntr01neg = 0 ;

  cntr13pos = 0 ;
  cntr13neg = 0 ;
  cntr11pos = 0 ;
  cntr11neg = 0 ;

  cntr23pos = 0 ;
  cntr23neg = 0 ;
  cntr21pos = 0 ;
  cntr21neg = 0 ;


  edm::Handle<l1tp2::DigitizedClusterCorrelatorCollectionTMI18> egtocorr18;
  if(evt.getByToken(egDigitizedToCorrelatorTMI18Src_, egtocorr18)){
//       std::cout << " EG Size:" << egtocorr18->size() <<  std::endl;
    for(const auto & egDigi : *egtocorr18){
//       std::cout << "    pt: " << egDigi.pt() << 
//        "    eta: " << egDigi.eta() << 
//        "    phi: " << egDigi.phi() << 
//        "    hoe: " << egDigi.hoe() << 
//        "    iso: " << egDigi.iso() << 
//        "    shape: " << egDigi.shape() << 
//        "    wp: " << egDigi.wp() <<
//        "    timing: " << egDigi.timing() << 
//        "    brems: " << egDigi.brems() << 
//        "    cardNr: " << egDigi.cardNumber() << 
//        "    slrNr: " << egDigi.slrNumber() << 
//        "    etaPos: " << egDigi.etaPositive() << 
//        "    data " << egDigi.data() << std::endl;

       mydata = egDigi.data() ;
//       if(egDigi.pt() > 20) std::cout << hex << "  eg pt: " << egDigi.pt() << " card " << egDigi.cardNumber() << " slr " << egDigi.slrNumber() << egDigi.etaPositive() << std::endl ; 

       if(egDigi.slrNumber() == 3 && egDigi.etaPositive() == 1) goto slr3pos ;
       if(egDigi.slrNumber() == 3 && egDigi.etaPositive() == 0) goto slr3neg ;
       if(egDigi.slrNumber() == 1 && egDigi.etaPositive() == 1) goto slr1pos ;
       if(egDigi.slrNumber() == 1 && egDigi.etaPositive() == 0) goto slr1neg ;

slr3pos:  ;

       if(egDigi.cardNumber() == 0 && cntr03pos < 16){
       dataToCL1Card0[1+cntr03pos] = mydata ;
       cntr03pos++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 1 && cntr13pos < 16){
       dataToCL1Card1[1+cntr13pos] = mydata ;
       cntr13pos++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 2 && cntr23pos < 16){
       dataToCL1Card2[1+cntr23pos] = mydata ;
       cntr23pos++ ;
	goto fillend ;
       } 

slr3neg:  ;

       if(egDigi.cardNumber() == 0 && cntr03neg < 16){
       dataToCL1Card0[41+cntr03neg] = mydata ;
       cntr03neg++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 1 && cntr13neg < 16){
       dataToCL1Card1[41+cntr13neg] = mydata ;
       cntr13neg++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 2 && cntr23neg < 16){
       dataToCL1Card2[41+cntr23neg] = mydata ;
       cntr23neg++ ;
	goto fillend ;
       } 

slr1pos:  ;


       if(egDigi.cardNumber() == 0 && cntr01pos < 16){
       dataToCL1Card0[81+1+cntr01pos] = mydata ;
       cntr01pos++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 1 && cntr11pos < 16){
       dataToCL1Card1[81+1+cntr11pos] = mydata ;
       cntr11pos++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 2 && cntr21pos < 16){
       dataToCL1Card2[81+1+cntr21pos] = mydata ;
       cntr21pos++ ;
	goto fillend ;
       } 

slr1neg:  ;

       if(egDigi.cardNumber() == 0 && cntr01neg < 16){
       dataToCL1Card0[81+41+cntr01neg] = mydata ;
       cntr01neg++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 1 && cntr11neg < 16){
       dataToCL1Card1[81+41+cntr11neg] = mydata ;
       cntr11neg++ ;
	goto fillend ;
       } 
       if(egDigi.cardNumber() == 2 && cntr21neg < 16){
       dataToCL1Card2[81+41+cntr21neg] = mydata ;
       cntr21neg++ ;
	goto fillend ;
       } 
fillend:  ;
  }}

        l1tp2::DigitizedCaloToCorrelatorTMI18 l1CaloTMI18 = l1tp2::DigitizedCaloToCorrelatorTMI18(dataToCL1Card0, dataToCL1Card1, dataToCL1Card2) ;
	caloCandsTMI18->push_back(l1CaloTMI18) ;
	evt.put(std::move(caloCandsTMI18), "DigitizedCaloToCorrelatorTMI18");

 
 }

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void Phase2L1CaloToCorrelatorTMI18::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("egtocorr18", edm::InputTag("l1tPhase2L1CaloEGammaEmulator", "GCTDigitizedClusterToCorrelatorTMI18"));
  desc.add<edm::InputTag>("pftocorr18", edm::InputTag("l1tPhase2CaloPFClusterEmulator","GCTDigitizedPFClusterToCorrelatorTMI18"));
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(Phase2L1CaloToCorrelatorTMI18);
