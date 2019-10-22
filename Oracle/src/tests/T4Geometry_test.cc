/**
 * @file T4Geometry_test.cc
 *
 *
 * @brief unit testing for the T4Geometry class
 *
 * @author J. Faustin
 * @version 1.0
 */

#include "MCNPGeometry.hh"
#include "T4Geometry.hh"
#include "anyvolumes.hh"
#include "volumes.hh"
#include "gtest/gtest.h"

class T4test : public ::testing::Test
{

protected:
  static void SetUpTestCase()
  {
    t4_output_stream = &cout;
    t4_language = (T4_language)0;
    t4Geom = new T4Geometry("slab.t4");
  }

  static void TearDownTestCase()
  {
    delete t4Geom;
    t4Geom = nullptr;
  }
  static T4Geometry *t4Geom;
};

T4Geometry *T4test::t4Geom = nullptr;

TEST_F(T4test, CreationAndCompo)
{
  ASSERT_EQ(t4Geom->getFilename(), "slab.t4");

  vector<double> point = {12.024, -72.882, 1.0883};
  long rank = t4Geom->getVolumes()->which_volume(point);
  std::string compo = t4Geom->getCompos()->get_name_from_volume(rank);
  ASSERT_EQ(compo, "ALU1");
}

TEST_F(T4test, AddEquivalence)
{
  ASSERT_FALSE(t4Geom->materialInMap("5-6.2"));
  t4Geom->addEquivalence("5-6.2", "ZINC");
  ASSERT_TRUE(t4Geom->materialInMap("5-6.2"));
}

TEST_F(T4test, WeakEquivalenceNOK)
{
  ASSERT_FALSE(t4Geom->weakEquivalence("9999-3.9", "ALU2"));
}

TEST_F(T4test, WeakEquivalenceOK)
{
  MCNPGeometry mcnpGeom("input_slab");
  vector<double> point(3);

  t4Geom->addEquivalence("345_-2.7", "ALU1");
  point = {12.024, -72.882, 1.0883};

  long rank = t4Geom->getVolumes()->which_volume(point);
  std::string compo = t4Geom->getCompos()->get_name_from_volume(rank);
  mcnpGeom.addCell2Density(3001, {345, "-2.7"});
  ASSERT_TRUE(t4Geom->weakEquivalence(mcnpGeom.getCellDensity(3001), compo));

  t4Geom->addEquivalence("345-2.7", "ALU3"); //should be ALU2 and test will give false.
  point = {0.43281, -1.3670, -0.096474};

  rank = t4Geom->getVolumes()->which_volume(point);
  compo = t4Geom->getCompos()->get_name_from_volume(rank);
  mcnpGeom.addCell2Density(2001, {345, "-2.7"});
  ASSERT_FALSE(t4Geom->weakEquivalence(mcnpGeom.getCellDensity(2001), compo));
}

TEST_F(T4test, DistanceToSurface)
{
  vector<double> point1 = {3.0, -1.0, -0.5};           // on Surface between blue and green
  vector<double> point1a = {3.0, -1.0, -0.5 + 2.0e-8}; // within margin of error
  vector<double> point1b = {3.0, -1.0, -0.5 - 2.0e-8}; // within margin of error
  vector<double> point2 = {3.0, -1.0, -1.44};          // in blue, far for Surface
  long rank;

  Volumes *volumes = t4Geom->getVolumes();

  rank = volumes->which_volume(point1);
  ASSERT_TRUE(t4Geom->distanceFromSurface(point1, rank) <= 1e-7);

  rank = volumes->which_volume(point1a);
  ASSERT_TRUE(t4Geom->distanceFromSurface(point1a, rank) <= 1e-7);

  rank = volumes->which_volume(point1b);
  ASSERT_TRUE(t4Geom->distanceFromSurface(point1b, rank) <= 1e-7);

  rank = volumes->which_volume(point2);
  ASSERT_FALSE(t4Geom->distanceFromSurface(point2, rank) <= 1e-7);
}
