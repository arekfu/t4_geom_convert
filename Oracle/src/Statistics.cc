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
  nbSuccess++;
}

void Statistics::IncrementFailure(){
  nbFailure++;
}

void Statistics::recordFailurePosition(vector<float> position){
  failurePositions.push_back(position);
}
