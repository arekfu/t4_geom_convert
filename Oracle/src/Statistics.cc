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
  failed.position = {position[0], position[1], position[2]};
  failed.volumeID = rank;
  failures.push_back(failed);
}

vector<failedPoint> Statistics::getFailures(){
  return failures;
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

void Statistics::writeOutForVisu(string& fname){
  T4_event_storing<failedPoint> t4_store;
  string rawname = getRawFileName(fname);
  rawname += ".points";
  char* cstr = getCstrFileName(rawname);
  t4_store.initialize(cstr,
                      T4_OUTPUT,
                      ASCII,
                      T4_TYPE_DOUBLE, "x",
                      T4_TYPE_DOUBLE, "y",
                      T4_TYPE_DOUBLE, "z",
                      T4_NO_TYPE);
  t4_store.write_header_dx();
  for (int iFail=0; iFail<nbFailure; iFail++){
    t4_store.store(&failures[iFail]);
  }

  t4_store.finalize();
}


string Statistics::getRawFileName(string& fname){
  size_t lastindex = fname.find_last_of(".");
  string rawname = fname.substr(0, lastindex);
  return rawname;
}

char* Statistics::getCstrFileName(string& rawname){
  char *cstr = new char[rawname.length() + 1];
  strcpy(cstr, rawname.c_str());
  return cstr;
}
