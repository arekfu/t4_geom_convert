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

#include "anyvolumes.hh"
#include "compos.hh"
#include "composfromgeom.hh"
#include "t4convert.hh"
#include "volumes.hh"
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

/** \class T4Geometry
 *  \brief Class for dealing with Tripoli-4 geometry
 *
 *  This class reads the T4 input file, retrieves the composition at a given
 *  point and calls the weak equivalence test.
 */
class T4Geometry
{
  static const std::vector<std::vector<double>> directions;
  Volumes *volumes;
  Compos *compos;
  std::string t4Filename;
  std::map<std::string, std::string> equivalenceMap;

public:
  T4Geometry();

  /**
   *  Class constructor.
   *
   * @param[in] t4Filename The Tripoli-4 geometry file to be compared.
   * is ignored.
   */
  T4Geometry(const std::string &t4Filename);

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

  std::string getFilename();
  Volumes *const &getVolumes();
  Compos *const &getCompos();

  /**
   * Check if the input material as already been mapped to T4 composition.
   * @param[in] matDens An MCNP materialID-density key to be checked.
   * @returns True if already been mapped, False otherwise.
   */
  bool materialInMap(const std::string &matDens);

  /**
   * Adds the association MCNP materialID-density -> T4 composition.
   *
   *
   */
  void addEquivalence(const std::string &matDens, const std::string &compo);

  /**
   * Checks if the weak equivalence tests is passed, i.e. if MCNP and T4 see
   * the same material at the considered point.
   * @param[in] matDens An MCNP materialID-density.
   * @param[in] compo A T4 composition.
   * @return True if the weak equivalence test passes, False otherwise.
   */
  bool weakEquivalence(const std::string &matDens, const std::string &compo);

  /**
   * Returns an estimate of the distance from the considered point to the
   * nearest surface.
   * @param[in] point the coordinates of the considered point.
   * @param[in] long the volume number where the considered point is.
   * @return an estimate of the distance
   */
  double distanceFromSurface(const std::vector<double> &point, long rank);
};

#endif /* T4GEOMETRY_H_ */
