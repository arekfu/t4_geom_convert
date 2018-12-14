/**
 * @file T4Geometry.hh
 *
 *
 * @brief T4Geometry class header file
 *
 * @author J. Faustin
 * @version 1.0
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

/** \class T4Geometry
 *  \brief Class for dealing with Tripoli-4 geometry
 *
 *  This class reads the T4 input file, retrieves the composition at a given
 *  point and calls the weak equivalence test.
 */
class T4Geometry {
  Volumes* volumes;
  Compos* compos;
  string t4Filename;
  map<string, string> equivalenceMap;
  double delta;
public:
  T4Geometry();

  /**
   *  Class constructor.
   *
   * @param[in] t4Filename The Tripoli-4 geometry file to be compared.
   * @param[in] delta The distance to the closest boundary below which a mismatch
   * is ignored.
   */
  T4Geometry(const string& t4Filename, double delta);

  /**
   *  Class destructor.
   *
   *
   */
  ~T4Geometry();


  /**
   * Reads the T4 input file and stores the volumes and compositions information.
   *
   *
   */
  void readT4input();

  string getFilename();
  Volumes* const & getVolumes();
  Compos* const & getCompos();
  double getDelta();
  
  /**
   * Check if the input material as already been mapped to T4 composition.
   * @param[in] matDens An MCNP materialID-density key to be checked.
   * @returns True if already been mapped, False otherwise.
   */
  bool materialInMap(string matDens);

  /**
   * Adds the association MCNP materialID-density -> T4 composition.
   *
   *
   */
   void addEquivalence(string matDens, const string& compo);

  /**
   * Checks if the weak equivalence tests is passed, i.e. if MCNP and T4 see
   * the same material at the considered point.
   * @param[in] matDens An MCNP materialID-density.
   * @param[in] compo A T4 composition.
   * @return True if the weak equivalence test passes, False otherwise.
   */
  bool weakEquivalence(string matDens, const string& compo);

  /**
   * Checks if the considered point distance to the nearest surface is below
   * a pre-defined threshold delta.
   * @param[in] point the coordinates of the considered point.
   * @param[in] long the volume number where the considered point is.
   * @return True if the point distance to the next surface is too small, False otherwise.
   */
  bool isPointNearSurface(const vector<double>& point, long rank);

};

#endif /* T4GEOMETRY_H_ */
