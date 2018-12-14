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
  int nbIgnored;
  int nbOutside;
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
  * Increments the number of points considered too closed to the next surface.
  *
  *
  */
  void IncrementIgnore();

  /**
  * Increments the number of points found outside the geometry (rank=-1).
  *
  *
  */
  void IncrementOutside();

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
  * Auxiliary method to report on successful, failed and ignored tests.
  *
  * @param[in] status The status of the displayed data.
  * @param[in] data   The data to be displayed, i.e. number of tests
  * @param[in] total  The total number of tests
  */
  void reportOn(const string& status, int data, int total);

  /**
  * Get the vector of failure positions.
  *
  * @return failurePositions
  */
  vector<vector<float> >& getFailurePositions(){
    return failurePositions;
  }

  // int getNbSuccess(){
  //   return nbSuccess;
  // }
  //
  // int getNbFailure(){
  //   return nbFailure;
  // }

  /**
  * Writes out the position of the points which fail the weak equivalence test
  * AND are too close to the next surface.
  *
  * @param[in] fname The output file name.
  */
  void writeOutForVisu(const string& fname);
};

#endif /* STATISTICS_H_ */
