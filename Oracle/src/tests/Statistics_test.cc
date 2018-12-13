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

TEST_F(StatisticsTest, addPosition)
{
  vector<float> position = {0.0, 0.0, 0.0};
  vector<vector<float> > failures = Stats->getFailurePositions();
  ASSERT_FALSE(std::find(failures.begin(), failures.end(), position) != failures.end());
  Stats->recordFailurePosition(position);
  failures = Stats->getFailurePositions();
  ASSERT_TRUE(std::find(failures.begin(), failures.end(), position) != failures.end());
}
