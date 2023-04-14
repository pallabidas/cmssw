#ifndef _PHASE_2_L1_CALO_JET_EMULATOR_H_
#define _PHASE_2_L1_CALO_JET_EMULATOR_H_

#include <cstdlib>

static constexpr int nTowerEta = 34;
static constexpr int nTowerPhi = 72;
static constexpr int nSTEta = 6;
static constexpr int nSTPhi = 24;

class towerMax{
  public:
  float energy;
  int phi;
  int eta;
  float energyMax;
  int phiMax;
  int etaMax;

  towerMax(){
    energy = 0;
    phi = 0;
    eta = 0;
    energyMax = 0;
    phiMax = 0;
    etaMax = 0;
  }

  towerMax& operator=(const towerMax& rhs){
    energy = rhs.energy;
    phi = rhs.phi;
    eta = rhs.eta;
    energyMax = rhs.energyMax;
    phiMax = rhs.phiMax;
    etaMax = rhs.etaMax;
    return *this;
  }
};

class jetInfo{
  public:
  float seedEnergy;
  float energy;
  int phi;
  int eta;
  float energyMax;
  int phiMax;
  int etaMax;

  jetInfo(){
    seedEnergy = 0;
    energy = 0;
    phi = 0;
    eta = 0;
    energyMax = 0;
    phiMax = 0;
    etaMax = 0;
  }

  jetInfo& operator=(const jetInfo& rhs){
    seedEnergy = rhs.seedEnergy;
    energy = rhs.energy;
    phi = rhs.phi;
    eta = rhs.eta;
    energyMax = rhs.energyMax;
    phiMax = rhs.phiMax;
    etaMax = rhs.etaMax;
    return *this;
  }
};

typedef struct {
  float et ;
  int eta ;
  int phi ;
  float towerEt ;
  int towerEta ;
  int towerPhi ;
} GCTsupertower_t ;

typedef struct {
  GCTsupertower_t cr[nSTPhi];
} etaStrip_t ;

typedef struct {
  GCTsupertower_t etaStrip[nSTEta];
} hgcalRegion_t ;

typedef struct {
  GCTsupertower_t pk[nSTEta];
} etaStripPeak_t ;

typedef struct {
  float et ;
  float hoe ;
} GCTtower_t ;

typedef struct {
  GCTtower_t GCTtower[nTowerEta/2][nTowerPhi] ;
} GCTintTowers_t ;

int getPeakBinOf3(float et0, float et1, float et2) {
  int x;
  float temp;
  if (et0 > et1) { x = 0; temp = et0; }
  else { x = 1; temp = et1; }
  if (et2 > temp) { x = 2; }
  return x;
}

void makeST(const float GCTintTowers[nTowerEta/2][nTowerPhi], GCTsupertower_t supertower_return[nSTEta][nSTPhi]){
  float et_sumEta[nSTEta][nSTPhi][3];
  float stripEta[nSTEta][nSTPhi][3];
  float stripPhi[nSTEta][nSTPhi][3];
  //float debug[nSTEta][nSTPhi][3][3];

  float ex_et[nTowerEta/2+1][nTowerPhi];
  for(int j = 0; j< nTowerPhi; j++){
    ex_et[nTowerEta/2][j] = 0;
    for(int i = 0; i < nTowerEta/2; i++){
      ex_et[i][j] = GCTintTowers[i][j];
    }
  }

  int index_i = 0;
  int index_j = 0;
  for(int i = 0; i < nTowerEta/2+1; i += 3){ // 17+1 to divide into 6 super towers
    index_j = 0;
    for(int j = 0; j < nTowerPhi; j+=3){ // 72 phi to 24 super towers
      //debug[index_i][index_j][0][0] = ex_et[i][j];
      //debug[index_i][index_j][0][1] = ex_et[i][j+1];
      //debug[index_i][index_j][0][2] = ex_et[i][j+2];
      //debug[index_i][index_j][1][0] = ex_et[i+1][j];
      //debug[index_i][index_j][1][1] = ex_et[i+1][j+1];
      //debug[index_i][index_j][1][2] = ex_et[i+1][j+2];
      //debug[index_i][index_j][2][0] = ex_et[i+2][j];
      //debug[index_i][index_j][2][1] = ex_et[i+2][j+1];
      //debug[index_i][index_j][2][2] = ex_et[i+2][j+2];

      stripEta[index_i][index_j][0] = ex_et[i][j] + ex_et[i][j+1] + ex_et[i][j+2];
      stripEta[index_i][index_j][1] = ex_et[i+1][j] + ex_et[i+1][j+1] + ex_et[i+1][j+2];
      stripEta[index_i][index_j][2] = ex_et[i+2][j] + ex_et[i+2][j+1] + ex_et[i+2][j+2];
      stripPhi[index_i][index_j][0] = ex_et[i][j] + ex_et[i+1][j] + ex_et[i+2][j];
      stripPhi[index_i][index_j][1] = ex_et[i][j+1] + ex_et[i+1][j+1] + ex_et[i+2][j+1];
      stripPhi[index_i][index_j][2] = ex_et[i][j+2] + ex_et[i+1][j+2] + ex_et[i+2][j+2];
      for(int k=0; k<3; k++){
        et_sumEta[index_i][index_j][k] = ex_et[i+k][j] + ex_et[i+k][j+1] + ex_et[i+k][j+2];
      }
      index_j++;
    }
    index_i++;
  }
  for(int i = 0; i < nSTEta; i++){
    for(int j = 0; j < nSTPhi; j++){
      GCTsupertower_t temp;
      float supertowerEt = et_sumEta[i][j][0] + et_sumEta[i][j][1] + et_sumEta[i][j][2];
      temp.et = supertowerEt;
      temp.eta = i;
      temp.phi = j;
      int peakEta = getPeakBinOf3(stripEta[i][j][0], stripEta[i][j][1], stripEta[i][j][2]);
      temp.towerEta = peakEta;
      int peakPhi = getPeakBinOf3(stripPhi[i][j][0], stripPhi[i][j][1], stripPhi[i][j][2]);
      temp.towerPhi = peakPhi;
      //float peakEt = ex_et[i*3+peakEta][j*3+1+peakPhi];
      float peakEt = ex_et[i*3+peakEta][j*3+peakPhi];
      temp.towerEt = peakEt;
      supertower_return[i][j] = temp;

      // DEBUG tower entries and peak position
      //std::cout<<"supertower: "<<std::endl;
      //std::cout<<debug[i][j][0][0]<<"\t"<<debug[i][j][0][1]<<"\t"<<debug[i][j][0][2]<<"\t"<<debug[i][j][1][0]<<"\t"<<debug[i][j][1][1]<<"\t"<<debug[i][j][1][2]<<"\t"<<debug[i][j][2][0]<<"\t"<<debug[i][j][2][1]<<"\t"<<debug[i][j][2][2]<<std::endl;
      //std::cout<<"max: "<<peakEta<<"\t"<<peakPhi<<"\t"<<peakEt<<std::endl;
      //std::cout<<"total: "<<i<<"\t"<<j<<"\t"<<supertowerEt<<std::endl;
    }
  }
  //return supertower_return;
}

GCTsupertower_t bestOf2(const GCTsupertower_t& calotp0, const GCTsupertower_t& calotp1) {
  GCTsupertower_t x;
  x = (calotp0.et > calotp1.et) ? calotp0 : calotp1;
  return x;
}

GCTsupertower_t getPeakBin24N(const etaStrip_t& etaStrip){

  GCTsupertower_t best01 = bestOf2(etaStrip.cr[0],etaStrip.cr[1]) ;
  GCTsupertower_t best23 = bestOf2(etaStrip.cr[2],etaStrip.cr[3]) ;
  GCTsupertower_t best45 = bestOf2(etaStrip.cr[4],etaStrip.cr[5]) ;
  GCTsupertower_t best67 = bestOf2(etaStrip.cr[6],etaStrip.cr[7]) ;
  GCTsupertower_t best89 = bestOf2(etaStrip.cr[8],etaStrip.cr[9]) ;
  GCTsupertower_t best1011 = bestOf2(etaStrip.cr[10],etaStrip.cr[11]) ;
  GCTsupertower_t best1213 = bestOf2(etaStrip.cr[12],etaStrip.cr[13]) ;
  GCTsupertower_t best1415 = bestOf2(etaStrip.cr[14],etaStrip.cr[15]) ;
  GCTsupertower_t best1617 = bestOf2(etaStrip.cr[16],etaStrip.cr[17]) ;
  GCTsupertower_t best1819 = bestOf2(etaStrip.cr[18],etaStrip.cr[19]) ;
  GCTsupertower_t best2021 = bestOf2(etaStrip.cr[20],etaStrip.cr[21]) ;
  GCTsupertower_t best2223 = bestOf2(etaStrip.cr[22],etaStrip.cr[23]) ;
  
  GCTsupertower_t best0123 = bestOf2(best01,best23) ;
  GCTsupertower_t best4567 = bestOf2(best45,best67) ;
  GCTsupertower_t best891011 = bestOf2(best89,best1011) ;
  GCTsupertower_t best12131415 = bestOf2(best1213,best1415) ;
  GCTsupertower_t best16171819 = bestOf2(best1617,best1819) ;
  GCTsupertower_t best20212223 = bestOf2(best2021,best2223) ;
  
  GCTsupertower_t best01234567 = bestOf2(best0123,best4567) ;
  GCTsupertower_t best89101112131415 = bestOf2(best891011,best12131415) ;
  GCTsupertower_t best16to23 = bestOf2(best16171819,best20212223) ;
  
  GCTsupertower_t best0to15 = bestOf2(best01234567,best89101112131415) ;
  GCTsupertower_t bestOf24 = bestOf2(best0to15,best16to23) ;
  
  return bestOf24 ;
}

towerMax getPeakBin6N(const etaStripPeak_t& etaStrip){
  towerMax x;
  
  GCTsupertower_t best01 = bestOf2(etaStrip.pk[0],etaStrip.pk[1]) ;
  GCTsupertower_t best23 = bestOf2(etaStrip.pk[2],etaStrip.pk[3]) ;
  GCTsupertower_t best45 = bestOf2(etaStrip.pk[4],etaStrip.pk[5]) ;
  
  GCTsupertower_t best0123 = bestOf2(best01,best23) ;
  
  GCTsupertower_t bestOf6 = bestOf2(best0123,best45) ;
  
  x.energy = bestOf6.et ;
  x.phi = bestOf6.phi;
  x.eta = bestOf6.eta;
  x.energyMax = bestOf6.towerEt;
  x.etaMax = bestOf6.towerEta ;
  x.phiMax = bestOf6.towerPhi ;
  return x ;
}

jetInfo getJetPosition(GCTsupertower_t temp[nSTEta][nSTPhi]){
  etaStripPeak_t etaStripPeak;
  jetInfo jet ;

  for (int i = 0; i < nSTEta; i++) {
    etaStrip_t test;
    for (int j = 0; j < nSTPhi; j++) {
      test.cr[j] = temp[i][j];    
    }
    etaStripPeak.pk[i] = getPeakBin24N(test);
  }

  towerMax peakIn6;
  peakIn6 = getPeakBin6N(etaStripPeak);

  jet.seedEnergy = peakIn6.energy ;
  jet.energy = 0 ;
  jet.eta = peakIn6.eta ;
  jet.phi = peakIn6.phi ;
  jet.energyMax = peakIn6.energyMax;
  jet.etaMax = peakIn6.etaMax;
  jet.phiMax = peakIn6.phiMax;
  //std::cout<<jet.seedEnergy<<"\t"<<jet.energy<<"\t"<<jet.eta<<"\t"<<jet.phi<<"\t"<<jet.energyMax<<"\t"<<jet.etaMax<<"\t"<<jet.phiMax<<std::endl;

  return jet ;
}

jetInfo getJetValues(GCTsupertower_t tempX[nSTEta][nSTPhi], int seed_eta, int seed_phi ){
  float temp[nSTEta+2][nSTPhi+2] ;
  float eta_slice[3] ;
  jetInfo jet_tmp;
  //float debug[3][3];

  for(int i = 0; i < nSTEta+2; i++){
    for(int k = 0; k < nSTPhi+2; k++){
      temp[i][k] = 0 ;
    }
  }

  for(int i = 0; i < nSTEta; i++){
    for(int k = 0; k < nSTPhi; k++){
      temp[i+1][k+1] = tempX[i][k].et ;
    }
  }

  int seed_eta1,  seed_phi1 ;

  seed_eta1 = seed_eta ; //to start from corner
  seed_phi1 = seed_phi ; //to start from corner
  float tmp1, tmp2, tmp3 ;

  for(int j = 0; j < nSTEta; j++){
    for(int k = 0; k < nSTPhi; k++){
      if(j == seed_eta1 && k == seed_phi1) {
        //debug[0][0] = temp[j][k];
        //debug[0][1] = temp[j][k+1];
        //debug[0][2] = temp[j][k+2];
        //debug[1][0] = temp[j+1][k];
        //debug[1][1] = temp[j+1][k+1];
        //debug[1][2] = temp[j+1][k+2];
        //debug[2][0] = temp[j+2][k];
        //debug[2][1] = temp[j+2][k+1];
        //debug[2][2] = temp[j+2][k+2];

        for(int m = 0; m < 3 ; m++){
          tmp1 = temp[j+m][k] ;
          tmp2 = temp[j+m][k+1] ;
          tmp3 = temp[j+m][k+2] ;

          eta_slice[m] = tmp1 + tmp2 + tmp3 ;
        }
      }
    }
  }

  jet_tmp.energy=eta_slice[0] + eta_slice[1] + eta_slice[2] ;

  // DEBUG jet energy and seed
  //std::cout<<"inside getJetValues:"<<std::endl;
  //std::cout<<debug[0][0]<<"\t"<<debug[0][1]<<"\t"<<debug[0][2]<<"\t"<<debug[1][0]<<"\t"<<debug[1][1]<<"\t"<<debug[1][2]<<"\t"<<debug[2][0]<<"\t"<<debug[2][1]<<"\t"<<debug[2][2]<<std::endl;
  //std::cout<<"seed: "<<tempX[seed_eta][seed_phi].et<<std::endl;
  //std::cout<<"total: "<<seed_eta<<"\t"<<seed_phi<<"\t"<<jet_tmp.energy<<std::endl;

  // set the used supertower ets to 0
  for(int i = 0; i < nSTEta; i++){
    if(i+1 >= seed_eta && i <= seed_eta+1){
      for(int k = 0; k < nSTPhi; k++){
        if(k+1 >= seed_phi && k <= seed_phi+1) tempX[i][k].et = 0;
      }
    }
  }

  return jet_tmp ;
}

jetInfo getRegion(GCTsupertower_t temp[nSTEta][nSTPhi]){
  jetInfo jet_tmp, jet;
  jet_tmp = getJetPosition(temp) ;
  int seed_phi = jet_tmp.phi ;
  int seed_eta = jet_tmp.eta ;
  jet = getJetValues(temp, seed_eta, seed_phi) ;
  jet_tmp.energy = jet.energy;
  return jet_tmp;
}

bool compareByEt (l1tp2::Phase2L1CaloJet i, l1tp2::Phase2L1CaloJet j) { return(i.jetEt() > j.jetEt()); };

#endif
