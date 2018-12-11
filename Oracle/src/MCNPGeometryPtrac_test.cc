/*
 * MCNPGeometryPtrac_test.cpp
 *
 *  Created on: 7 d�c. 2018
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
		MCNPg1 = new MCNPGeometry("../mcnp/slabp", "../mcnp/input_slab");
		MCNPg1->goThroughHeaderPTRAC(8);
	}

	void TearDown( ){}
};


TEST_F(MCNPtestPtrac, ReadFirstData)
{
	pair<int, int> pointEvent = MCNPg1->readPointEvent();
	ASSERT_EQ(pointEvent.first,1);
	ASSERT_EQ(pointEvent.second,1000);

	pair<int, int> volumeMaterial = MCNPg1->readVolumeMaterial();
	ASSERT_EQ(volumeMaterial.first,3001);
	ASSERT_EQ(volumeMaterial.second,1);

	vector<float> pointCoords = MCNPg1->readPoint();
	ASSERT_FLOAT_EQ(pointCoords[0], 12.024);
	ASSERT_FLOAT_EQ(pointCoords[1], -72.882);
	ASSERT_FLOAT_EQ(pointCoords[2], 1.0883);
}

TEST_F(MCNPtestPtrac, ReadAll)
{
	int ii=1;
	while(ii<=1000){
		MCNPg1->readNextPtracData();
		ii++;
	}

	ASSERT_EQ(MCNPg1->getPointEvent().first, 1000);
	ASSERT_EQ(MCNPg1->getPointEvent().second, 1000);

	ASSERT_EQ(MCNPg1->getVolumeMaterial().first, 1001);
	ASSERT_EQ(MCNPg1->getVolumeMaterial().second, 3);

	ASSERT_FLOAT_EQ(MCNPg1->getPointXyz()[0], -2.2580);
	ASSERT_FLOAT_EQ(MCNPg1->getPointXyz()[1], 18.880);
	ASSERT_FLOAT_EQ(MCNPg1->getPointXyz()[2], -1.2856);

	ASSERT_EQ(MCNPg1->getNpoints(), 1000);
}
