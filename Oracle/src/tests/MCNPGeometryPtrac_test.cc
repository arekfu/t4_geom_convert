/*
 * MCNPGeometryPtrac_test.cpp
 *
 *  Created on: 7 dec. 2018
 *      Author: jofausti
 */

#include "MCNPGeometry.hh"
#include "gtest/gtest.h"
#include <fstream>

using namespace std;

class MCNPtestPtrac : public ::testing::Test
{

public:
  MCNPGeometry *MCNPg1;
  MCNPPTRAC *MCNPptrac;
  void SetUp()
  {
    // code here will execute just before the test ensues
    MCNPg1 = new MCNPGeometry("input_slab");
    MCNPptrac = new MCNPPTRACASCII("slabp");
  }

  void TearDown()
  {
    delete MCNPg1;
    delete MCNPptrac;
  }
};

TEST_F(MCNPtestPtrac, createObject)
{
  ASSERT_EQ(MCNPg1->getInputPath(), "input_slab");
}

TEST_F(MCNPtestPtrac, ReadFirstData)
{
  MCNPptrac->readNextPtracData(1000);
  auto const &record = MCNPptrac->getPTRACRecord();
  ASSERT_EQ(record.pointID, 1);
  ASSERT_EQ(record.eventID, 1000);
  ASSERT_EQ(record.cellID, 3001);
  ASSERT_EQ(record.materialID, 1);
  ASSERT_DOUBLE_EQ(record.point[0], 12.024);
  ASSERT_DOUBLE_EQ(record.point[1], -72.882);
  ASSERT_DOUBLE_EQ(record.point[2], 1.0883);
}

TEST_F(MCNPtestPtrac, ReadAll)
{
  int ii = 1;
  while (ii <= 1000) {
    MCNPptrac->readNextPtracData(2000);
    ii++;
  }

  auto const &record = MCNPptrac->getPTRACRecord();
  ASSERT_EQ(record.pointID, 1000);
  ASSERT_EQ(record.eventID, 1000);

  ASSERT_EQ(record.cellID, 1001);
  ASSERT_EQ(record.materialID, 3);

  ASSERT_DOUBLE_EQ(record.point[0], -2.2580);
  ASSERT_DOUBLE_EQ(record.point[1], 18.880);
  ASSERT_DOUBLE_EQ(record.point[2], -1.2856);

  ASSERT_EQ(MCNPptrac->getNbPointsRead(), 1000);
}
