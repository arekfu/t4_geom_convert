/**
* @file Statistics.hh
*
*
* @brief Statistics class header
*
* @author J. Faustin
* @version 1.0
*/

#ifndef STASTISTICS_H_
#define STASTISTICS_H_

#include <iostream>
#include <vector>

using namespace std;

/** \class Statistics.
*  \brief Class for dealing with comparison statistics.
*
*  This class records the comparison sucesses and fails, the points of failure
*  and write report and output data file.
*/
class Statistics {
  int nbSuccess;
  int nbFailure;
  vector<vector<float> > failurePositions;

public:

  /**
  * Class constructor.
  *
  *
  */
  Statistics();

  /**
  * Class destructor.
  *
  *
  */
  virtual ~Statistics();

  /**
  * Increments the number of success.
  *
  *
  */
  void IncrementSuccess();

  /**
  * Increments the number of failure.
  *
  *
  */
  void IncrementFailure();


  /**
  * Add a new position to list of positions where the weak equivalence failed.
  *
  *
  */
  void recordFailurePosition(vector<float> position);

  /**
  * Reports in the terminal the comparison statistics
  *
  *
  */
  void report();

  /**
  * Get the vector of failure positions.
  *
  * @return failurePositions
  */
  vector<vector<float> >& getFailurePositions(){
    return failurePositions;
  }

  int getNbSuccess(){
    return nbSuccess;
  }

  int getNbFailure(){
    return nbFailure;
  }
};

#endif /* STATISTICS_H_ */
