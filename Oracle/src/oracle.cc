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
#include <iomanip>
#include <cstdlib>
#include <vector>
#include <utility>
#include "options_compare.hh"
#include "geometrytype.hh"
#include "volumes.hh"
#include "anyvolumes.hh"
#include "compos.hh"
#include "composfromgeom.hh"
#include "t4coreglob.hh"
#include "t4convert.hh"
#include "t4sobol.hh"
#include "t4random.hh"
#include "MCNPGeometry.hh"
#include "T4Geometry.hh"
using namespace std;
int strictness_level = 3;
int npoints = 1000; // TODO : remove this


void compare_geoms(const OptionsCompare &options){
	T4Geometry t4Geom(options.filenames[0]);
	MCNPGeometry mcnpGeom(options.filenames[2], options.filenames[1]);

	//Volumes* const &volumes = t4Geom.getVolumes();
	//Compos* const &compos = t4Geom.getCompos();

	std::vector<double> point(3);
	int n_inside = 0;

	std::cout << "Starting comparison..." << std::endl;
	mcnpGeom.parseINP();
	mcnpGeom.goThroughHeaderPTRAC(8);

	int ii=0;
	while (mcnpGeom.readNextPtracData(npoints)) {
		ii++;
		long rank;
		std::string compo;

		rank = t4Geom.getVolumes()->which_volume(point);
		compo = t4Geom.getCompos()->get_name_from_volume(rank);

		if (!t4Geom.materialInMap(mcnpGeom.getMaterialDensity())){
				t4Geom.addEquivalence(mcnpGeom.getMaterialDensity(), compo);
				cout << ii << "  adding to equivalence map  " << endl;
		}
		else{
			if (t4Geom.weakEquivalence(mcnpGeom.getMaterialDensity(), compo)){
				cout << ii << "      match"  <<endl;
			}
			else{
				cout << ii << "   NO match !!"  <<endl;
			}
		}
	}
		// flag to check if the point is inside all geometries
		//bool inside_all = true;

		// rank = volumes->which_volume(point);
		// if(rank>=0) {
		// 	compo = compos->get_name_from_volume(rank);
		// } else {
		// 	inside_all = false;
		// 	compo.clear();
		// }

		// // check that both points are inside or outside the geometry
		// if((rank>=0 && mcnp_cell<0) || (rank<0 && mcnp_cell>=0)) {
		// 	std::cout << "Test #" << i << ": IN/OUT MISMATCH:"
		// 	<< "\n    point = "
		// 	<< point[0] << ", " << point[1] << ", " << point[2]
		// 	<< "\n    rank = " << rank << "; mcnp_cell = " << mcnp_cell
		// 	<< "\n    name = \"" << volumes->get_name_from_volume(rank)
		// 	<< "\"; mcnp_name = \"" << "Implement this" << '"'
		// 	<< std::endl;
		// } else if(options.verbosity>0) {
		// 	std::cout << "Test #" << i << ": IN/OUT OK: point = "
		// 	<< point[0] << ", " << point[1] << ", " << point[2]
		// 	<< "; rank = " << rank << "; mcnp_cell = " << "implement this"
		// 	<< "\n    name = \"" << volumes->get_name_from_volume(rank)
		// 	<< "\"; mcnp_name = \"" << "Implement this" << '"'
		// 	<< std::endl;
		// }

	// 	if(rank>=0) {
	// 		if(compo!=mcnp_compo) {
	// 			std::cout << "Test #" << i << ": COMPO MISMATCH:"
	// 			<< "\n    point = "
	// 			<< point[0] << ", " << point[1] << ", " << point[2]
	// 			<< "\n    rank = " << rank << "; mcnp_cell = " << mcnp_cell
	// 			<< "\n    name = \"" << volumes->get_name_from_volume(rank)
	// 			<< "\"; mcnp_name = \"" << "implement this"
	// 			<< "\"\n    compo = \"" << compo
	// 			<< "\"; mcnp_compo = \"" << "implement this" << '"'
	// 			<< std::endl;
	// 		} else if(options.verbosity>0) {
	// 			std::cout << "Test #" << i << ": COMPO OK:"
	// 			<< "\n    point = "
	// 			<< point[0] << ", " << point[1] << ", " << point[2]
	// 			<< "\n    rank = " << rank << "; mcnp_cell = " << mcnp_cell
	// 			<< "\n    name = \"" << volumes->get_name_from_volume(rank)
	// 			<< "\"; mcnp_name = \"" << "implement this"
	// 			<< "\"\n    compo = \"" << compo
	// 			<< "\"; mcnp_compo = \"" << "implement this" << '"'
	// 			<< std::endl;
	// 		}
	// 	}
	//
	// 	// count points inside all geometries
	// 	if(inside_all)
	// 	++n_inside;
	// }
	// std::cout << "End of comparison." << std::endl;
	// const float inside_percentage = 100.*float(n_inside)/float(npoints);
	// std::cout << "Points inside all geometries: " << n_inside << "/" << npoints
	// << " (" << inside_percentage << "%)" << std::endl;
	// if(inside_percentage<50.) {
	// 	std::cout << "\nYou may want to manually adjust the bounding box (--bbox) if this percentage is too low."
	// 	<< std::endl;
	// }

	// ---- End ----
	// for(vector<Volumes*>::const_iterator ivol=volumes.begin(), evol=volumes.end(); ivol!=evol; ++ivol) {
	// 	(*ivol)->free();
	// }
}

int main(int argc, char ** argv){
	// tracability
	std::cout << "*** Tripoli-4 geometry comparison ***" << endl;
	// std::cout << "Tripoli-4 Version is $Name:  $\n" << endl;
	// std::cout << "File Version is $Id: visutripoli4.cc,v 1.20 2016/07/26 09:09:13 dm232107 Exp $\n" << endl;
	t4_output_stream = &cout;
	t4_language = (T4_language) 0;

	// ---- Read options ----
	OptionsCompare options;
	options.get_opts(argc, argv);
	if (options.help){
		help();
		exit(EXIT_SUCCESS);
	}

	compare_geoms(options);

	return 0;
}
