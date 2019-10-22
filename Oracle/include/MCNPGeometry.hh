/**
 * @file MCNPGeometry.hh
 *
 *
 * @brief MCNPGeometry class header
 *
 * @author J. Faustin
 * @version 1.0
 */

#ifndef MCNPGEOMETRY_H_
#define MCNPGEOMETRY_H_

#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <vector>
#include "PTRACFormat.hh"


struct PTRACRecord {
  int pointID, eventID;
  int cellID, materialID;
  std::vector<double> point;
};

class MCNPPTRAC
{
  protected:
    long nbPointsRead;
    PTRACRecord record;

  public:
    MCNPPTRAC();
    virtual ~MCNPPTRAC() {};

    /**
     * If the maximum number of read points has not been reached: reads the next
     * particle, event, volume, material, position in PTRAC file.
     *
     * @returns true if successful, false otherwise.
     */
    virtual bool readNextPtracData(long maxReadPoint) = 0;

    /**
     * Increments the number of points read so far.
     */
    void incrementNbPointsRead();
    long getNbPointsRead();

    PTRACRecord const &getPTRACRecord() const;
};


class MCNPPTRACASCII : public MCNPPTRAC
{
  protected:
    std::string currentLine;
    int nbDataCellMaterialLine;
    std::ifstream ptracFile;

  public:

    /**
     * @param[in] ptracPath MCNP ptrac file path.
     */
    MCNPPTRACASCII(std::string const &ptracPath);

    /**
     * If the maximum number of read points has not been reached: reads the next
     * particle, event, volume, material, position in PTRAC file.
     *
     * @returns true if successful, false otherwise.
     */
    bool readNextPtracData(long maxReadPoint);

  protected:
    /**
     * Reads the header lines. Sets the current line at the last header line of PTRAC file.
     *
     * @param[in] nHeaderLines The number of header lines in the PTRAC file.
     */
    void goThroughHeaderPTRAC(int nHeaderLines);

    /**
     * Gets the number of data expected on 2nd line of each particle event data block.
     * If the PTRAC has the correct format, this information is found in the 5th
     * header line.
     *
     * @param[in] line5 The string containing the data of the 5th header line.
     * @return the number of integer data stored on the 2nd of each particle event
     * data block.
     */
    int getDataFromLine5Ptrac(const std::string &line5);

    /**
     * Checks that the 2nd line of each particle event data block does contain the
     * cell ID and the material ID. These information are respectively identified as
     * 17 and 18 by the PTRAC writer. The program exits if it is not the case.
     *
     * @param[in] line6 The string containing the data of the 6th header line.
     * @param[in] nbData The number of data expected on 2nd line of each particle
     * event data block (given by getDataFromLine5Ptrac function).
     */
    void checkDataFromLine6Ptrac(const std::string &line6, int nbData);

    /**
     * Reads the point ID number and the event ID number.
     *
     * @return A pair containing the point ID and event ID.
     */
    std::pair<int, int> readPointEvent();

    /**
     * Reads the cell ID number and the material ID number.
     *
     * @return a pair containing the volume ID and material ID.
     */
    std::pair<int, int> readCellMaterial();

    /**
     * Reads the point coordinates (x,y,z).
     *
     * @return the point coordinates as a vector of 3 doubles.
     */
    std::vector<double> readPoint();

    /**
     * Stores the next line in the PTRAC file in the currentLine variable.
     *
     *
     */
    void getNextLinePtrac();

    /**
     * Determines whether we have read the whole block data in the input file.
     * Caution : blank line separator is identified as string of length 1...
     *
     * @returns true if the whole block data has been read, false otherwise
     */
    bool finishedReading();
};


/** \class MCNPGeometry.
 *  \brief Class for dealing with MCNP geometry.
 *
 *  This class reads the MCNP INP and PTRAC files and gives pseudo-random points,
 *  cells and materials information.
 */
class MCNPGeometry
{
  std::map<unsigned long, std::string> cell2Density;

  std::vector<int> volumeList;
  long nps;
  std::string inputPath;

  std::ifstream inputFile;
  std::string currentLine;

public:
  /**
  * Class constructor.
  *
  * @param[in] inputPath MCNP inp file path.
  */
  MCNPGeometry(const std::string &inputPath);

  /**
  * Reads and associates the current material to its density in the cell2Density map.
  *
  */
  void associateCell2Density();

  /**
   * Parses the INP file, looking for the material densities.
   *
   *
   */
  void parseINP();

  /**
   * Attempts to add a new association cell ID -> material density.
   *
   *
   */
  void addCell2Density(unsigned long key, const std::pair<unsigned long, std::string> &value);

  /**
   * Gives the association cell ID - material density.
   *
   * @param[in] cellID the cell ID
   * @return the association as a string: materialID-density.
   */
  std::string const &getCellDensity(unsigned long cellID) const;

  /**
   * Determines whether we have read the whole block data in the input file.
   * Caution : blank line separator is identified as string of length 1...
   *
   * @returns true if the whole block data has been read, false otherwise
   */
  bool finishedReading();

  /**
   * Determines whether the current is a comment
   *
   *
   * @returns true if current line is a comment, false otherwise
   */
  bool isLineAComment(std::string const &lineContent) const;

  /**
   * Determines whether the current is a material definition
   *
   *
   * @returns true if current line is a comment, false otherwise
   */
  bool isLineAMaterial(std::string const &lineContent) const;

  const std::string &getInputPath();
  long getNPS();
  const std::vector<int> &getVolumeList();
  void setVolumeList(const std::vector<int> &volumeList);
  std::map<unsigned long, std::string> &getCell2Density();
};
#endif /* MCNPGEOMETRY_H_ */
