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

class MCNPtestPtrac : public ::testing::Test {

public:
  MCNPGeometry *MCNPg1;
  void SetUp( ){
    // code here will execute just before the test ensues
    MCNPg1 = new MCNPGeometry("slabp", "input_slab");
    MCNPg1->goThroughHeaderPTRAC(8);
  }

  void TearDown( ){}
};

TEST_F(MCNPtestPtrac, createObject)
{
  ASSERT_EQ(MCNPg1->getPtracPath(), "slabp");
  ASSERT_EQ(MCNPg1->getInputPath(), "input_slab");
}

TEST_F(MCNPtestPtrac, ReadFirstData)
{
  MCNPg1->getNextLine();
  pair<int, int> pointEvent = MCNPg1->readPointEvent();
  ASSERT_EQ(pointEvent.first,1);
  ASSERT_EQ(pointEvent.second,1000);

  MCNPg1->getNextLine();
  pair<int, int> cellMaterial = MCNPg1->readCellMaterial();
  ASSERT_EQ(cellMaterial.first,3001);
  ASSERT_EQ(cellMaterial.second,1);

  MCNPg1->getNextLine();
  vector<double> pointCoords = MCNPg1->readPoint();
  ASSERT_DOUBLE_EQ(pointCoords[0], 12.024);
  ASSERT_DOUBLE_EQ(pointCoords[1], -72.882);
  ASSERT_DOUBLE_EQ(pointCoords[2], 1.0883);
}

TEST_F(MCNPtestPtrac, ReadAll)
{
  int ii=1;
  while(ii<=1000){
    MCNPg1->readNextPtracData(2000);
    ii++;
  }

  ASSERT_EQ(MCNPg1->getPointID(), 1000);
  ASSERT_EQ(MCNPg1->getEventID(), 1000);

  ASSERT_EQ(MCNPg1->getCellID(), 1001);
  ASSERT_EQ(MCNPg1->getMaterialID(), 3);

  ASSERT_DOUBLE_EQ(MCNPg1->getPointXyz()[0], -2.2580);
  ASSERT_DOUBLE_EQ(MCNPg1->getPointXyz()[1], 18.880);
  ASSERT_DOUBLE_EQ(MCNPg1->getPointXyz()[2], -1.2856);

  ASSERT_EQ(MCNPg1->getNbPointsRead(), 1000);
}
