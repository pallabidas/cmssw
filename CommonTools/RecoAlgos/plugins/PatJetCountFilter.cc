/* \class PatJetCountFilter
 *
 * Filters events if at least N jets
 *
 * \author: Andrew Brinkerhoff, Baylor
 *
 */
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CommonTools/UtilAlgos/interface/ObjectCountFilter.h"

 typedef ObjectCountFilter<
         std::vector<pat::Jet>
         >::type PatJetCountFilter;

DEFINE_FWK_MODULE( PatJetCountFilter );
