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
#include <array>
using namespace std;

struct failedPoint {
  array<double, 3> position;
  long volumeID;
};

/** \class Statistics.
*  \brief Class for dealing with comparison statistics.
*
*  This class records the comparison sucesses and failures, the points of failure
*  and write report and output data file.
*/
class Statistics {
  int nbSuccess;
  int nbFailure;
  int nbIgnored;
  int nbOutside;
  long nbT4Volumes;
  vector<long> coveredRanks;
  vector<failedPoint> failures;


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
  void incrementSuccess();

  /**
  * Increments the number of failure.
  *
  *
  */
  void incrementFailure();

  /**
  * Increments the number of points considered too closed to the next surface.
  *
  *
  */
  void incrementIgnore();

  /**
  * Increments the number of points found outside the geometry (rank=-1).
  *
  *
  */
  void incrementOutside();

  /**
  * Gets the total number of investigated points.
  *
  * @returns the sum of sum of successes, failures,
  * ignore and outside points.
  */
  int getTotalPts();

  /**
  * If the rank is being explored for the first time, add it to the list of covered ranks.
  *
  * @param[in] rank The volume ID to be added to the list.
  */
  void recordCoveredRank(long rank);

  /**
  * Sets the number of volumes defined in T4 input file.
  *
  *
  */
  void setNbT4Volumes(long nbVolumes);

  /**
  * Add a new failed test info to the list of failed weak equivalence tests.
  *
  * @param[in] position The position of the point where the test failedPoint.
  * @param[in] rank The volumeID where this point is located according to T4.
  */
  void recordFailure(vector<double> position, long rank);

  /**
  * Get the list of failed tests.
  *
  * @return failures
  */
  vector<failedPoint> getFailures();


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
