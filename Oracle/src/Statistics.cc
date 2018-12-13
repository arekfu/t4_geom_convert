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
}

Statistics::~Statistics(){ }

void Statistics::IncrementSuccess(){
  nbSuccess+=1;
}

void Statistics::IncrementFailure(){
  nbFailure+=1;
}

void Statistics::recordFailurePosition(vector<float> position){
  failurePositions.push_back(position);
}

void Statistics::report(){
  cout << "\n---------------------------" << endl ;
  cout << "Reporting on MCNP/T4 geometry comparison" << endl ;
  cout << "-----------------------------" << endl ;

  int totalPt = nbSuccess + nbFailure;
  cout << "Number of SAMPLED points:     " << totalPt << endl;
  cout << "Number of SUCCESSFUL tests:  " << nbSuccess
                                      << " -> "
                                      << 100.*float(nbSuccess)/float(totalPt)
                                      << "%" << endl;

  cout << "Number of FAILED tests:      " << nbFailure
                                      << " -> "
                                      << 100.*float(nbFailure)/float(totalPt)
                                      << "%" << endl;
}
