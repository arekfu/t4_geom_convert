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

#include <array>
#include <iostream>
#include <set>
#include <vector>

/**
* A structure to represent the points where the weak equivalence test failed.
*
*/
struct failedPoint {
  std::array<double, 3> position;
  int mcnpParticleID;
  int mcnpCellID;
  int mcnpMaterialID;
  double color;
  int rank;
};

/** \class Statistics.
*  \brief Class for dealing with comparison statistics.
*
*  This class records the successful and failed comparisons, the points of failure
*  and write report and output data file.
*/
class Statistics
{
  int nbSuccess;
  int nbFailure;
  int nbIgnored;
  int nbOutside;
  long nbT4Volumes;
  std::set<long> coveredRanks;
  std::vector<failedPoint> failures;

public:
  /**
  * Class constructor.
  *
  *
  */
  Statistics();

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
  * @returns the sum of successful, failed,
  * ignored and outside points.
  */
  int getTotalPts();

  /**
  * Insert the rank being explored to set of covered ranked (if it is part of the set,
  * set.insert() does nothing).
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
  * @param[in] rank The volume number where this point is located according to T4.
  * @param[in] pointID The point number as listed by MCNP in the PTRAC file
  * @param[in] cellID The volume number where the point is located according to MCNP.
  * @param[in] materialID The material number where the point is located according to MCNP.
  */
  void recordFailure(std::vector<double> position, long rank, int pointID, int cellID, int materialID);

  /**
  * Get the list of failed tests.
  *
  * @return failures
  */
  std::vector<failedPoint> getFailures();

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
  void reportOn(const std::string &status, int data, int total);

  /**
  * Writes out the position of the points which fail the weak equivalence test
  * AND are too close to the next surface.
  *
  * @param[in] fname The input file name on which will be based the output file name.
  */
  void writeOutForVisu(std::string &fname);

  /**
  * Returns the raw file name, i.e. without file extension.
  *
  * @return The raw file name.
  */
  std::string getRawFileName(std::string &fname);

  void writePointsFile(std::string &rawname);
};

#endif /* STATISTICS_H_ */
