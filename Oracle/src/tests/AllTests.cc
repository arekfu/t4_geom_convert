#include "geometrytype.hh"
#include "gtest/gtest.h"

using namespace std;
int strictness_level = 3;

int main(int argc, char **argv)
{
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
