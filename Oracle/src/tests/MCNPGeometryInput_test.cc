/*
 * MCNPGeometryInput_test.cpp
 *
 *  Created on: 10 dec. 2018
 *      Author: jofausti
 */

#include "MCNPGeometry.hh"
#include "gtest/gtest.h"
#include <fstream>

using namespace std;

class MCNPtestInput : public ::testing::Test {

public:
  MCNPGeometry *MCNPg1;
  void SetUp( ){
    // code here will execute just before the test ensues
    MCNPg1 = new MCNPGeometry("slabp", "input_slab");
  }

  void TearDown( ){
    delete MCNPg1;
  }
};

TEST_F(MCNPtestInput, isComment)
{
  string lineTest = "c      Test line true";
  ASSERT_EQ(MCNPg1->isLineAComment(lineTest),1);

  lineTest = "C      Test line true CAP";
  ASSERT_EQ(MCNPg1->isLineAComment(lineTest),1);

  lineTest = "Test line false";
  ASSERT_EQ(MCNPg1->isLineAComment(lineTest),0);
}


TEST_F(MCNPtestInput, AssociateCell2Density)
{
  MCNPg1->parseINP();
  ASSERT_EQ(MCNPg1->getCell2Density()[1001], "-2.7");
  ASSERT_EQ(MCNPg1->getCell2Density()[2001], "-2.7");
  ASSERT_EQ(MCNPg1->getCell2Density()[3001], "-2.7");
}

TEST_F(MCNPtestInput, AssociateMaterialDensity)
{
  MCNPg1->parseINP();
  MCNPg1->goThroughHeaderPTRAC(8);
  MCNPg1->readNextPtracData(20000);
  ASSERT_EQ(MCNPg1->getMaterialDensity(),"1-2.7");

  MCNPg1->readNextPtracData(20000);
  ASSERT_EQ(MCNPg1->getMaterialDensity(),"2-2.7");
}

TEST_F(MCNPtestInput, ReadNPS)
{
  MCNPg1->readNPS();
  ASSERT_EQ(MCNPg1->getNPS(), 1000);
}
