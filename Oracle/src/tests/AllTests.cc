#include "gtest/gtest.h"
#include "geometrytype.hh"

using namespace std;
int strictness_level = 3;

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
