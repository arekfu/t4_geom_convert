/**
 * @file oracle.cc
 * This is the main file for the test Oracle of the converter.
 *
 * @brief contains the main functions of the Oracle program
 *
 * @author J. Faustin
 * @version 1.0
 */

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
int npoints = 10; // TODO : remove this


void compare_geoms(const OptionsCompare &options){
	T4Geometry t4Geom(options.filenames[0]);
	MCNPGeometry mcnpGeom(options.filenames[2], options.filenames[1]);

	std::vector<double> point(3);
	int n_inside = 0;

	mcnpGeom.parseINP();

	std::cout << "Starting comparison on "
						<< min(npoints, mcnpGeom.getNPS()) << " points..."
	          << std::endl;
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
				//cout << ii << "      match"  <<endl;
			}
			else{
				cout << ii << "   NO match !!"  <<endl;
			}
		}
	}
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
