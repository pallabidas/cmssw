#ifndef DataFormats_L1TCalorimeterPhase2_DigitizedPFClusterCorrelatorTMI18_h
#define DataFormats_L1TCalorimeterPhase2_DigitizedPFClusterCorrelatorTMI18_h

#include <ap_int.h>
#include <vector>

namespace l1tp2 {

  class DigitizedPFClusterCorrelatorTMI18 {
  private:
    // Data
    unsigned long long int clusterData;
    unsigned int idxGCTCard;  // 0, 1, or 2
    unsigned int idxSLR;  //  1 or 3
    unsigned int idxEtaPos ; // 1 or 0  

    // Constants
    static constexpr unsigned int n_towers_eta = 34;  // in GCT card unique region
    static constexpr unsigned int n_towers_phi = 24;  // in GCT card unique region
    static constexpr unsigned int n_crystals_in_tower = 5;
    static constexpr float LSB_PT = 0.5;                 // 0.5 GeV
    static constexpr float ETA_RANGE_ONE_SIDE = 1.4841;  // barrel goes from (-1.4841, +1.4841)
    static constexpr float LSB_ETA = ((2 * ETA_RANGE_ONE_SIDE) / (n_towers_eta * n_crystals_in_tower));  // (2.8 / 170)
    static constexpr float LSB_PHI = ((2 * M_PI) / (3 * n_towers_phi * n_crystals_in_tower));            // (2 pi * 360)

    static constexpr unsigned int n_bits_pt = 12;            // 12 bits allocated for pt
    static constexpr unsigned int n_bits_unused_start = 63;  // unused bits start at bit 63

    // "top" of the correlator card #0 in GCT coordinates is iPhi tower index 24
    static constexpr int correlatorCard0_tower_iphi_offset = 24;
    // same but for correlator cards #1 and 2 (cards wrap around phi = 180 degrees):
    static constexpr int correlatorCard1_tower_iphi_offset = 48;
    static constexpr int correlatorCard2_tower_iphi_offset = 0;

    // Private member functions to perform digitization
    ap_uint<12> digitizePt(float pt_f) {
      float maxPt_f = (std::pow(2, n_bits_pt) - 1) * LSB_PT;
      // If pT exceeds the maximum (extremely unlikely), saturate the value
      if (pt_f >= maxPt_f) {
        return (ap_uint<12>)0xFFF;
      }

      return (ap_uint<12>)(pt_f / LSB_PT);
    }

    ap_uint<7> digitizeEta(unsigned int iEtaCr) { return (ap_uint<7>)iEtaCr; }

    ap_uint<7> digitizePhi(unsigned int iPhiCr) { return (ap_uint<7>)iPhiCr; }

    // To-do: fb: no information yet
    ap_uint<6> digitizeFb(unsigned int fb) { return (ap_uint<6>)fb; }


    // TO-DO: Spare
    ap_uint<20> digitizeSpare(unsigned int spare) { return (ap_uint<20>)spare; }

  public:
    DigitizedPFClusterCorrelatorTMI18() { clusterData = 0x0; }

    DigitizedPFClusterCorrelatorTMI18(ap_uint<64> data) { clusterData = data; }

    // Constructor from digitized inputs
    DigitizedPFClusterCorrelatorTMI18(ap_uint<12> pt,
                               ap_uint<7> eta,
                               ap_int<7> phi,
                               ap_uint<12> ecal,
                               ap_uint<6> fb,
                               ap_uint<20> spare,
                               int iGCTCard,
                               bool fullydigitizedInputs) {
      (void)fullydigitizedInputs;
      clusterData = ((ap_uint<64>)pt) | (((ap_uint<64>)eta) << 12) | (((ap_uint<64>)phi) << 19) |
                    (((ap_uint<64>)ecal) << 26) | (((ap_uint<64>)fb) << 38) | 
                    (((ap_uint<64>)spare << 44));
           
      idxGCTCard = int((spare>>3) & 0x3) ;
      idxSLR = int(spare & 0x3 ) ;
      idxEtaPos = int((spare >> 2) & 0x1) ;
    }

    ap_uint<64> data() const { return clusterData; }

    // Other getters
    float ptLSB() const { return LSB_PT; }
    ap_uint<12> pt() const { return (clusterData & 0xFFF); }

    // crystal eta in the correlator region (LSB: 2.8/170)
    ap_uint<7> eta() const { return ((clusterData >> 12) & 0x7F); }  // (eight 1's) 0b11111111 = 0xFF

    // crystal phi in the correlator region (LSB: 2pi/360)
    ap_int<7> phi() const { return ((clusterData >> 19) & 0x7F); }  // (seven 1's) 0b1111111 = 0x7F

    // timing: not saved in the current emulator
    ap_uint<12> ecal() const { return ((clusterData >> 26) & 0xFFF); }
    ap_uint<6> fb() const { return ((clusterData >> 38) & 0x3F); }

    // brems: not saved in the current emulator
    ap_uint<10> spare() const { return ((clusterData >> 44) & 0xFFFFF); }

    // which GCT card (0, 1, or 2)
    unsigned int cardNumber() const { return idxGCTCard; }

    // which SLR (3 or 1)
    unsigned int slrNumber() const { return idxSLR; }

    // eta pos neg
    unsigned int etaPositive() const { return idxEtaPos; }

    const int unusedBitsStart() const { return n_bits_unused_start; }

    // Other checks
    bool passNullBitsCheck(void) const { return ((data() >> unusedBitsStart()) == 0x0); }

    // Get real eta (does not depend on card number). crystal iEta = 0 starts at real eta -1.4841.
    float realEta() const { return (float)((-1 * ETA_RANGE_ONE_SIDE) + (eta() * LSB_ETA)); }

    // Get real phi (uses card number).
    float realPhi() const {
      // each card starts at a different real phi
      int offset_tower = 0;
      if (cardNumber() == 0) {
        offset_tower = correlatorCard0_tower_iphi_offset;
      } else if (cardNumber() == 1) {
        offset_tower = correlatorCard1_tower_iphi_offset;
      } else if (cardNumber() == 2) {
        offset_tower = correlatorCard2_tower_iphi_offset;
      }
      int thisPhi = (phi() + (offset_tower * n_crystals_in_tower));
      // crystal iPhi = 0 starts at real phi = -180 degrees
      return (float)((-1 * M_PI) + (thisPhi * LSB_PHI));
    }
  };

  // Collection typedef
  typedef std::vector<l1tp2::DigitizedPFClusterCorrelatorTMI18> DigitizedPFClusterCorrelatorCollectionTMI18;

}  // namespace l1tp2

#endif
