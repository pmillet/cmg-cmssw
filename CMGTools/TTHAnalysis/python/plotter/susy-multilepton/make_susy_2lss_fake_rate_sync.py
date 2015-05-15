plotmode='norm'
pyfile=["mcPlots.py -f --plotmode "+plotmode+" --print 'pdf'",'mcEfficiencies.py']

#PATH="-P /afs/cern.ch/work/b/botta/TREES_72X_050515_MiniIso"
PATH="-P /data1/p/peruzzi/TREES_72X_050515_MiniIso"
OUTDIR='plots_test/plots_test'

cuts={}
def add_cuts(mylist):
    my = list(set(mylist))
    return ' '.join("-A alwaystrue "+cut+" '"+cuts[cut]+"'" for cut in my)
def remove_cuts(mylist):
    my = list(set(mylist))
    return ' '.join("-X "+cut for cut in my)
def replace_cuts(mylist):
    my = list(set(mylist))
    return ' '.join("-R "+cut+" "+newcut+" '"+cuts[newcut]+"'" for cut,newcut in mylist)
def prepare_cuts(add,remove,replace):
    my = list(set(add))
    my = [i for i in my if i not in remove]
    for k,l in replace:
        my = [l if k==x else x for x in my]
        my=list(set(my))
    return my
    


cuts["anylep"]="abs(LepGood_pdgId) > 0"
cuts["minireliso04"]="LepGood_miniRelIso<0.4"
cuts["dxy005"]="LepGood_dxy<0.05"
cuts["dz01"]="LepGood_dz<0.1"
cuts["sipLT4"]="LepGood_sip3d<4"
cuts["sipGT4"]="LepGood_sip3d>4"
cuts["pt5"]="LepGood_pt > 5"
cuts["pt7"]="LepGood_pt > 7"
cuts["pt10"]="LepGood_pt > 10"
cuts["etaLT2p4"]="abs(LepGood_eta) < 2.4"
cuts["etaLT2p5"]="abs(LepGood_eta) < 2.5"
cuts["ismu"]="abs(LepGood_pdgId)==13"
cuts["isel"]="abs(LepGood_pdgId)==11"
cuts["muLooseID"]="LepGood_looseMuonId > 0"
cuts["muMediumID"]="LepGood_mediumMuonId > 0"
cuts["elMVAloose"]="LepGood_mvaIdPhys14 > -0.11+(-0.35+0.11)*(abs(LepGood_eta)>0.8)+(-0.55+0.35)*(abs(LepGood_eta)>1.479)"
cuts["elMVAtight"]="LepGood_mvaIdPhys14 > 0.73+(0.57-0.73)*(abs(LepGood_eta)>0.8)+(+0.05-0.57)*(abs(LepGood_eta)>1.479)"
cuts["losthitsLEQ1"]="LepGood_lostHits<=1"
cuts["losthitsEQ0"]="LepGood_lostHits==0"
cuts["elConvVeto"]="LepGood_convVeto"
cuts["tightcharge"]="LepGood_tightCharge > (abs(LepGood_pdgId) == 11)"
cuts["multiiso"]="multiIso_multiWP(LepGood_pdgId,LepGood_pt,LepGood_eta,LepGood_miniRelIso,LepGood_jetPtRatio,LepGood_jetPtRel,2) > 0"
cuts["mutrackpterr"]="blablabla"


LooseLepSel=["minireliso04","dxy005","dz01"]
LooseMuSel=LooseLepSel+["pt5","etaLT2p4","muLooseID"]
LooseElSel=LooseLepSel+["pt7","etaLT2p5","elMVAloose","elConvVeto","losthitsLEQ1"]

TightLepSel=["sipLT4","dz01","multiiso"]
TightMuSel=LooseMuSel+TightLepSel+["pt10","etaLT2p4","muMediumID","tightcharge"]
TightElSel=LooseElSel+TightLepSel+["pt10","etaLT2p5","elMVAtight","elConvVeto","tightcharge","losthitsEQ0"]


MuDsetsQCD='-p QCDMu_red'
ElDsetsQCD='-p QCDEl_red'
MuDsetsInSitu='-p TTJets_red'
ElDsetsInSitu='-p TTJets_red'

runs=[]
#[NAME,SELECTION_CUTS,REMOVED_CUTS,REPLACED_CUTS,DATASETS,NUM_FOR_FR_STUDY(doeff==1 + define in sels.txt),XVAR_FOR_FR_STUDY(doeff==1 + define in xvars.txt)]
#runs.append(["LooseMu",LooseMuSel,[],[],MuDsets])
#runs.append(["LooseEl",LooseElSel,[],[],ElDsets])
#runs.append(["TightMu",TightMuSel,[],[],MuDsets])
#runs.append(["TightEl",TightElSel,[],[],ElDsets])
runs.append(["FO1Mu",TightMuSel,[],[("multiiso","minireliso04")],MuDsetsQCD])
runs.append(["FO1El",TightElSel,[],[("multiiso","minireliso04")],ElDsetsQCD])
runs.append(["FO2El",TightElSel,[],[("multiiso","minireliso04"),("elMVAtight","elMVAloose")],ElDsetsQCD])
runs.append(["FO1MuInSitu",TightMuSel,["dxy005","dz01"],[("sipLT4","sipGT4"),("multiiso","minireliso04")],MuDsetsInSitu])
runs.append(["FO1ElInSitu",TightElSel,["dxy005","dz01"],[("sipLT4","sipGT4"),("multiiso","minireliso04")],ElDsetsInSitu])
runs.append(["FO2ElInSitu",TightElSel,["dxy005","dz01"],[("sipLT4","sipGT4"),("multiiso","minireliso04"),("elMVAtight","elMVAloose")],ElDsetsInSitu])


for run in runs:
    doeff = (len(run)>5)
    RUN="python "+pyfile[doeff]+" --s2v --tree treeProducerSusyMultilepton susy-multilepton/susy_2lss_fake_rate_mca.txt susy-multilepton/susy_2lss_fake_rate_perlep.txt"
    if doeff:
        run[0]=run[5]+'_ON_'+run[0]
        B0=' '.join([RUN,PATH,"susy-multilepton/susy_2lss_fake_rate_sels.txt","susy-multilepton/susy_2lss_fake_rate_xvars.txt"])
        B0 += " --legend=TL  --yrange -1 2 --showRatio --ratioRange 0 3 --xcut 10 999 --ytitle 'Fake rate' --groupBy cut"
        B0 += ' --sP '+run[5]
        B0 += " -o "+OUTDIR+'_'+run[0]+"/plots.root"
        B0 += ' --sP '+run[6]
    else:
        B0=' '.join([RUN,PATH,"susy-multilepton/susy_2lss_fake_rate_plots.txt"])
        B0 += " --pdir "+OUTDIR+'_'+run[0]
        if 'ismu' in run[1]:
            B0 += " --xP ele_MVAid,losthits,multiIso_AND_EleId,EleId,sieie_EB,sieie_EE"
        elif 'isel' in run[1]:
            B0 += " --xP mu_mediumid,multiIso_AND_MuonId,MuonId"
    B0 += ' '+add_cuts(prepare_cuts(run[1],run[2],run[3]))
    B0 += ' '+str(run[4])
    print B0

