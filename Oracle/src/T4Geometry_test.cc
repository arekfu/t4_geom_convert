/*
 * T4Geometry_test.cpp
 *
 *  Created on: 11 dec. 2018
 *      Author: jofausti
 */

#include "T4Geometry.hh"
#include "gtest/gtest.h"

using namespace std;

class T4test : public ::testing::Test {

public:
	T4Geometry *t4Geom;
	void SetUp( ){
		// code here will execute just before the test ensues
		t4Geom = new T4Geometry("slab.t4");        
	}

	void TearDown( ){}
};

TEST_F(T4test, createObject)
{
  ASSERT_EQ(t4Geom->getFilename(), "../data/slab.t4");
}
