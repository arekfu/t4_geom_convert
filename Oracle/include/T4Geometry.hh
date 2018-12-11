/*
 * T4Geometry.hh
 *
 *  Created on: 11 dec. 2018
 *      Author: jofausti
 */

#ifndef T4GEOMETRY_H_
#define T4GEOMETRY_H_

#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include "volumes.hh"
#include "anyvolumes.hh"
#include "compos.hh"
#include "composfromgeom.hh"
#include "t4coreglob.hh"
#include "t4convert.hh"
#include "t4sobol.hh"
#include "t4random.hh"

using namespace std;

class T4Geometry {
  Volumes* volumes;
	Compos* compos;
	string t4Filename;

public:
  T4Geometry();
  T4Geometry(string t4Filename);
  ~T4Geometry();

  void readT4input(const string t4Filename);
  string getFilename(){
    return t4Filename;
  }

  Volumes* const & getVolumes(){
    return volumes;
  }

  Compos* const & getCompos(){
    return compos;
  }
};

#endif /* T4GEOMETRY_H_ */
