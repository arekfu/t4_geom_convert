/*
 * Statistics_test.cpp
 *
 *  Created on: 13 d�c. 2018
 *      Author: jofausti
 */

#include "Statistics.hh"
#include "gtest/gtest.h"

using namespace std;

class StatisticsTest : public ::testing::Test {

public:
  Statistics *Stats;
  void SetUp( ){
    // code here will execute just before the test ensues
    Stats = new Statistics();
  }

  void TearDown( ){}
};

TEST_F(StatisticsTest, addFailed)
{
  vector<double> position = {0.0, 0.0, 0.0};
  array<double, 3> pos = {0.0, 0.0, 0.0};
  failedPoint fail;
  fail.position = pos;
  //fail.volumeID = 3;
  vector<failedPoint> failures = Stats->getFailures();
  ASSERT_EQ(failures.size(), 0);

  Stats->recordFailure(position, 3);
  failures = Stats->getFailures();
  ASSERT_EQ(failures.size(), 1);
  ASSERT_EQ(failures[0].position[0], fail.position[0]);
  ASSERT_EQ(failures[0].position[1], fail.position[1]);
  ASSERT_EQ(failures[0].position[2], fail.position[2]);
  //ASSERT_EQ(failures[0].volumeID, fail.volumeID);
}
