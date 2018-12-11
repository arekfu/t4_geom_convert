//============================================================================
// Name        : oracle.cpp
// Author      : J. Faustin
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <fstream>
#include <sstream>

#include "MCNPGeometry.hh"
using namespace std;

void readT4input(){
	cout << "Implement reading T4 input ..." << endl;
}

void readMCNPinput(){
	cout << "Implement reading MCNP input ..." << endl;
}

int main(int argc, char **argv){
  // tracability
  std::cout << "*** MCNP/Tripoli-4 geometry comparison ***" << endl;
//  t4_output_stream = &cout;
//  t4_language = (T4_language) 2;
//
//  // ---- Read options ----
//  OptionsCompare options;
//  options.get_opts(argc, argv);
//  if (options.help){
//    help();
//    exit(EXIT_SUCCESS);
//  }
//
//  std::cout << "Will test on " << options.n_points << " points" << std::endl;
//  compare_geoms(options);


  readT4input();
	readMCNPinput();

	MCNPGeometry mcnp(argv[1], argv[2]);
	mcnp.goThroughHeaderPTRAC(8);
	pair<int, int> pointEvent = mcnp.readPointEvent();
	cout << "point " << pointEvent.first << " should be " << 1 << endl;
	cout << "event " << pointEvent.second << " should be " << 1000 << endl;

  cout << "Done" << endl;
  return 0;
}
