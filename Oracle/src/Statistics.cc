/**
* @file Statistics.cc
*
*
* @brief Statistics class
*
* @author J. Faustin
* @version 1.0
*/

#include "Statistics.hh"
#include "t4storeevent.hh"
#include "errorCC.hh"
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <algorithm>
Statistics::Statistics(){
  nbSuccess = 0;
  nbFailure = 0;
  nbIgnored = 0;
  nbOutside = 0;
  nbT4Volumes = 0;
}

Statistics::~Statistics(){ }

void Statistics::incrementSuccess(){
  nbSuccess+=1;
}

void Statistics::incrementFailure(){
  nbFailure+=1;
}

void Statistics::incrementIgnore(){
  nbIgnored+=1;
}

void Statistics::incrementOutside(){
  nbOutside+=1;
}

int Statistics::getTotalPts(){
  return nbSuccess + nbFailure + nbIgnored + nbOutside;
}

void Statistics::recordCoveredRank(long rank){
  if (std::find(coveredRanks.begin(), coveredRanks.end(),rank)==coveredRanks.end()){
    coveredRanks.push_back(rank);
  }
}

void Statistics::setNbT4Volumes(long nbVolumes){
  nbT4Volumes = nbVolumes;
}

void Statistics::recordFailure(vector<double> position, long rank){
  failedPoint failed;
  failed.position = position;
  failed.volumeID = rank;
  failures.push_back(failed);
}

vector<vector<double> > Statistics::getFailurePositions(){
  vector<vector<double> > fail_pos;
  for(vector<failedPoint >::iterator ifp=failures.begin(), efp=failures.end();
      ifp!=efp; ++ifp){
        failedPoint dummy = *ifp;
        fail_pos.push_back(dummy.position);
      }
  return fail_pos;
}

void Statistics::report(){
  cout << "\n---------------------------" << endl ;
  cout << "Reporting on MCNP/T4 geometry comparison" << endl ;
  cout << "-----------------------------" << endl ;

  int totalPt = getTotalPts();
  cout << "Number of SAMPLED points : " << totalPt << endl;
  reportOn("SUCCESSFUL", nbSuccess, totalPt);
  reportOn("FAILED    ", nbFailure, totalPt);
  reportOn("IGNORED   ", nbIgnored, totalPt);
  reportOn("OUTSIDE   ", nbOutside, totalPt);
  cout << "Number of COVERED volumes: " << coveredRanks.size() << endl;
  cout << "Number of INPUT   volumes: " << nbT4Volumes << endl;
}

void Statistics::reportOn(const string& status, int data, int total){
  cout << "Number of " << status << "     : " << data
                                          << " -> "
                                          << 100.*float(data)/float(total)
                                          << "%" << endl;
}

void Statistics::writeOutForVisu(const string& fname){
  cout << "Please implement visualization output..." << endl;
  T4_event_storing<failedPoint> t4_store;
  //initialize(char *filearg, enum direction_type dir, enum file_mode mode, ...);
  // ifstream file;
  // file.open(fname);
  // T4_store_locus_interface interface(&file);
  // interface.batch_initialize(fname.c_str(), 0);
  // for (int iFail=0; iFail<nbFailure; iFail++){
  //   vector<double> nextPosition = failurePositions[iFail];
  //   T4_store_locus T4store(nextPosition[0], nextPosition[1], nextPosition[2],
  //     0.0, 0.0, 0.0,
  //     0.0, 0.0,
  //     0.0, 0.0,
  //     0.0,
  //     0.0, 0.0,
  //     0.0, 0.0,
  //     0.0);
  //     interface.store(&T4store);
  // }
  // interface.batch_collect();


}
