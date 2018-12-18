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
  vector<vector<double> > failPos = Stats->getFailurePositions();
  ASSERT_FALSE(std::find(failPos.begin(), failPos.end(), position) != failPos.end());

  Stats->recordFailure(position, 3);
  failPos = Stats->getFailurePositions();
  ASSERT_TRUE(std::find(failPos.begin(), failPos.end(), position) != failPos.end());
}
