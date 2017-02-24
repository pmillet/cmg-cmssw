#include "L1Trigger/L1THGCal/interface/be_algorithms/HGCalClusteringImpl.h"

//class constructor
HGCalClusteringImpl::HGCalClusteringImpl(const edm::ParameterSet& conf){    
    seedThr_ = conf.getParameter<double>("seeding_threshold");
    tcThr_ = conf.getParameter<double>("clustering_threshold");
    dr_ = conf.getParameter<double>("dR_cluster");
}

void HGCalClusteringImpl::clusterise( const l1t::HGCalTriggerCellBxCollection & trgcells_, 
                                      l1t::HGCalClusterBxCollection & clusters_
    ){

    double_t protoClEta = 0.;
    double_t protoClPhi = 0.;           
    double_t C2d_pt  = 0.;
    double_t C2d_eta = 0.;
    double_t C2d_phi = 0.;
    uint32_t C2d_hwPtEm = 0;
    uint32_t C2d_hwPtHad = 0;
                
    int layer=0;
    bool seeds[trgcells_.size()];

    int itc=0;
    for(l1t::HGCalTriggerCellBxCollection::const_iterator tc = trgcells_.begin(); tc != trgcells_.end(); ++tc,++itc)
        seeds[itc] = (tc->hwPt() > seedThr_) ? true : false;

    itc=0;
    for(l1t::HGCalTriggerCellBxCollection::const_iterator tc = trgcells_.begin(); tc != trgcells_.end(); ++tc,++itc){

        if( seeds[itc] ){}
        
        int iclu=0;
        vector<int> tcPertinentClusters; 
        for(l1t::HGCalClusterBxCollection::const_iterator clu = clusters_.begin(); clu != clusters_.end(); ++clu,++iclu){
            if( clu->isPertinent(*tc, dr_) )
                tcPertinentClusters.push_back(iclu);
        }

        if( tcPertinentClusters.size() == 0 ){
            l1t::HGCalCluster obj( *tc );
            clusters_.push_back( 0, obj );
        }
        else{
            uint minDist = 1;
            uint targetClu = 0; 
            for( std::vector<int>::const_iterator iclu = tcPertinentClusters.begin(); iclu != tcPertinentClusters.end(); ++iclu ){
            } 
        }
       
    }
        
}


