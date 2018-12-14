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

Statistics::Statistics(){
  nbSuccess = 0;
  nbFailure = 0;
  nbIgnored = 0;
}

Statistics::~Statistics(){ }

void Statistics::IncrementSuccess(){
  nbSuccess+=1;
}

void Statistics::IncrementFailure(){
  nbFailure+=1;
}

void Statistics::IncrementIgnore(){
  nbIgnored+=1;
}

void Statistics::recordFailurePosition(vector<float> position){
  failurePositions.push_back(position);
}

void Statistics::report(){
  cout << "\n---------------------------" << endl ;
  cout << "Reporting on MCNP/T4 geometry comparison" << endl ;
  cout << "-----------------------------" << endl ;

  int totalPt = nbSuccess + nbFailure + nbIgnored;
  cout << "Number of SAMPLED points:     " << totalPt << endl;
  reportOn("SUCCESSFUL", nbSuccess, totalPt);
  reportOn("FAILED    ", nbFailure, totalPt);
  reportOn("IGNORED   ", nbIgnored, totalPt);
}

void Statistics::reportOn(const string& status, int data, int total){
  cout << "Number of " << status << ":  " << data
                                          << " -> "
                                          << 100.*float(data)/float(total)
                                          << "%" << endl;
}

void Statistics::writeOutForVisu(const string& fname){
  //TODO : implement this
  cout << "Please implement visualization output..." << endl;
}
