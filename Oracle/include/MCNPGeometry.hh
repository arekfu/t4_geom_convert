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

/** \class MCNPGeometry.
 *  \brief Class for dealing with MCNP geometry.
 *
 *  This class reads the MCNP INP and PTRAC files and gives pseudo-random points,
 *  cells and materials information.
 */
class MCNPGeometry
{
  int pointID;
  int eventID;
  int cellID;
  int materialID;
  std::vector<double> pointXYZ;

  std::map<int, std::string> cell2Density;

  std::vector<int> volumeList;
  int nbDataCellMaterialLine;
  long nbPointsRead;
  long nps;
  std::string ptracPath;
  std::string inputPath;

  std::ifstream ptracFile;
  std::ifstream inputFile;
  std::string currentLine;

public:
  /**
  * Class constructor.
  *
  * @param[in] ptracPath MCNP ptrac file path.
  * @param[in] inputPath MCNP inp file path.
  */
  MCNPGeometry(const std::string &ptracPath, const std::string &inputPath);

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
  * If the maximum number of read points has not been reached: reads the next
  * particle, event, volume, material, position in PTRAC file.
  *
  * @returns true if successful, false otherwise.
  */
  bool readNextPtracData(long maxReadPoint);

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
   * Searches the INP file for the total number of particle NPS.
   *
   */
  void readNPS();

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
   * Increments the number of points read so far.
   *
   *
   */
  void incrementNbPointsRead();

  /**
   * Attempts to add a new association cell ID -> material density.
   *
   *
   */
  void addCell2Density(int key, const std::string &value);

  /**
   * Gives the association material ID - material density.
   *
   * @return the association as a string: materialID-density.
   */
  std::string getMaterialDensity();

  void getNextLine();

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
   * @returns 1 if current line is a comment, 0 otherwise
   */
  int isLineAComment(std::string lineContent);

  const std::string &getInputPath();
  long getNPS();
  long getNbPointsRead();
  std::ifstream &getPtracFile();
  const std::string &getPtracPath();
  void setPtracPath(const std::string &ptracPath);
  const std::vector<int> &getVolumeList();
  void setVolumeList(const std::vector<int> &volumeList);
  int setCurrentLine(std::ifstream &inFile);
  int getPointID();
  int getEventID();
  void setPointEvent(const std::pair<int, int> &pointEvent);
  std::vector<double> getPointXyz();
  void setPointXyz(const std::vector<double> &pointXyz);
  int getCellID();
  int getMaterialID();
  void setCellMaterial(const std::pair<int, int> &cellMat);
  std::map<int, std::string> &getCell2Density();
};

#endif /* MCNPGEOMETRY_H_ */
