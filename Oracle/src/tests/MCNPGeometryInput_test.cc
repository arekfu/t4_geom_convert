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

class MCNPtestInput : public ::testing::Test
{

public:
  MCNPGeometry *MCNPg1;
  MCNPPTRAC *MCNPptrac;
  void SetUp()
  {
    // code here will execute just before the test ensues
    MCNPg1 = new MCNPGeometry("input_slab");
    MCNPptrac = new MCNPPTRAC("slabp", PTRACFormat::ASCII);
  }

  void TearDown()
  {
    delete MCNPg1;
    delete MCNPptrac;
  }
};

TEST_F(MCNPtestInput, isComment)
{
  string lineTest = "c      Test line true";
  ASSERT_EQ(MCNPg1->isLineAComment(lineTest), 1);

  lineTest = "C      Test line true CAP";
  ASSERT_EQ(MCNPg1->isLineAComment(lineTest), 1);

  lineTest = "Test line false";
  ASSERT_EQ(MCNPg1->isLineAComment(lineTest), 0);
}

TEST_F(MCNPtestInput, AssociateCell2Density)
{
  MCNPg1->parseINP();
  ASSERT_EQ(MCNPg1->getCellDensity(1000), "0_void");
  ASSERT_EQ(MCNPg1->getCellDensity(1001), "347_-2.7");
  ASSERT_EQ(MCNPg1->getCellDensity(2001), "346_-2.7");
  ASSERT_EQ(MCNPg1->getCellDensity(3001), "345_-2.7");
}
