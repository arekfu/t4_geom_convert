/*
* T4Geometry_test.cc
*
*  Created on: 11 dec. 2018
*      Author: jofausti
*/

#include "T4Geometry.hh"
#include "MCNPGeometry.hh"
#include "gtest/gtest.h"

using namespace std;

class T4test : public ::testing::Test {

protected:
	static void SetUpTestCase( ){
		t4_output_stream = &cout;
		t4_language = (T4_language) 0;
		t4Geom = new T4Geometry("../data/slab.t4");
	}

	static void TearDownTestCase(){
		delete t4Geom;
		t4Geom = NULL;
	}
	static T4Geometry* t4Geom;
};

T4Geometry* T4test::t4Geom = NULL;

TEST_F(T4test, CreationAndCompo)
{
	ASSERT_EQ(t4Geom->getFilename(), "../data/slab.t4");

	long rank;
	string compo;
	vector<double> point = {12.024, -72.882,  1.0883};
	rank = t4Geom->getVolumes()->which_volume(point);
	compo = t4Geom->getCompos()->get_name_from_volume(rank);
	ASSERT_EQ(compo, "ALU1");
}

TEST_F(T4test, WeakEquivalenceNOK)
{
	ASSERT_FALSE(t4Geom->weakEquivalence(9999, "ALU2"));
}

TEST_F(T4test, WeakEquivalenceOK)
{
	MCNPGeometry mcnpGeom("../data/slabp", "../data/input_slab");
	long rank;
	string compo;
	vector<double> point(3);

	t4Geom->addEquivalence(1, "ALU1");
	point = {12.024, -72.882,  1.0883};

	rank = t4Geom->getVolumes()->which_volume(point);
	compo = t4Geom->getCompos()->get_name_from_volume(rank);
	mcnpGeom.setCellMaterial({3001, 1});
	ASSERT_TRUE(t4Geom->weakEquivalence(mcnpGeom.getMaterialID(), compo));

	t4Geom->addEquivalence(2, "ALU3");
	point = {0.43281, -1.3670, -0.096474};

	rank = t4Geom->getVolumes()->which_volume(point);
	compo = t4Geom->getCompos()->get_name_from_volume(rank);
	mcnpGeom.setCellMaterial({2001, 2});
	ASSERT_FALSE(t4Geom->weakEquivalence(mcnpGeom.getMaterialID(), compo));
}
