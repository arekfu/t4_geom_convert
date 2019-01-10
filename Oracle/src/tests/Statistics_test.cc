/*
 * Statistics_test.cpp
 *
 *  Created on: 13 d�c. 2018
 *      Author: jofausti
 */

#include "Statistics.hh"
#include "gtest/gtest.h"

using namespace std;

class StatisticsTest : public ::testing::Test
{

public:
  Statistics *Stats;
  void SetUp()
  {
    // code here will execute just before the test ensues
    Stats = new Statistics();
  }

  void TearDown()
  {
    delete Stats;
  }
};

TEST_F(StatisticsTest, addFailed)
{
  vector<double> position = {1.0, 2.5, 4.0};
  array<double, 3> pos = {1.0, 2.5, 4.0};
  failedPoint fail{pos,
                   1,
                   4,
                   2,
                   pos[0],
                   3};
  vector<failedPoint> failures = Stats->getFailures();
  ASSERT_EQ(failures.size(), 0);

  Stats->recordFailure(position, 3.0, 1, 4, 2);
  failures = Stats->getFailures();
  ASSERT_EQ(failures.size(), 1);
  ASSERT_EQ(failures[0].position[0], fail.position[0]);
  ASSERT_EQ(failures[0].position[1], fail.position[1]);
  ASSERT_EQ(failures[0].position[2], fail.position[2]);
  ASSERT_EQ(failures[0].mcnpParticleID, fail.mcnpParticleID);
  ASSERT_EQ(failures[0].mcnpCellID, fail.mcnpCellID);
  ASSERT_EQ(failures[0].mcnpMaterialID, fail.mcnpMaterialID);
  ASSERT_EQ(failures[0].color, fail.color);
  ASSERT_EQ(failures[0].rank, fail.rank);
}
