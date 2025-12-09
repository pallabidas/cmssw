#ifndef DataFormats_L1TCalorimeterPhase2_DigitizedCaloToCorrelatorTMI18_h
#define DataFormats_L1TCalorimeterPhase2_DigitizedCaloToCorrelatorTMI18_h

#include <ap_int.h>
#include <vector>

namespace l1tp2 {

  class DigitizedCaloToCorrelatorTMI18 {
  private:
    // Data
    ap_uint<64> Card0Link[162] ;
    ap_uint<64> Card1Link[162] ;
    ap_uint<64> Card2Link[162] ;

  public:

    DigitizedCaloToCorrelatorTMI18() { for(int i=0;i<162;i++) {Card0Link[i]=0; Card1Link[i]=0; Card2Link[i]=0;}}
    DigitizedCaloToCorrelatorTMI18(ap_uint<64> data0[162], ap_uint<64> data1[162], ap_uint<64> data2[162]) { for(int i=0;i<162;i++) {Card0Link[i]=data0[i]; Card1Link[i]=data1[i]; Card2Link[i]=data2[i];}}

    const ap_uint<64>*  link0() const { return Card0Link; }
    const ap_uint<64>*  link1() const { return Card1Link; }
    const ap_uint<64>*  link2() const { return Card2Link; }

  };

  // Collection typedef
  typedef std::vector<l1tp2::DigitizedCaloToCorrelatorTMI18> DigitizedCaloToCorrelatorCollectionTMI18;

}  // namespace l1tp2

#endif
