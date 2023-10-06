/* \class PatJetSelector
 *
 * Selects jets with a configurable string-based cut.
 * Saves clones of the selected jets
 *
 * \author: Andrew Brinkerhoff, Baylor
 *
 * usage:
 *
 * module bestPatJets = PatJetSelector {
 *   src = cms.InputTag('slimmedJetsAK8') ## For AK8 "fat" jets
 *   string cut = "pt > 20 & abs( eta ) < 2"
 * }
 *
 * for more details about the cut syntax, see the documentation
 * page below:
 *
 *   https://twiki.cern.ch/twiki/bin/view/CMS/SWGuidePhysicsCutParser
 *
 *
 */

#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/SingleObjectSelector.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

 typedef SingleObjectSelector<
           std::vector<pat::Jet>, 
           StringCutObjectSelector<pat::Jet> 
         > PatJetSelector;

DEFINE_FWK_MODULE( PatJetSelector );
