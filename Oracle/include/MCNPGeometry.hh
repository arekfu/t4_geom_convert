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

#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <map>

using namespace std;

/** \class MCNPGeometry.
 *  \brief Class for dealing with MCNP geometry.
 *
 *  This class reads the MCNP INP and PTRAC files and gives pseudo-random points,
 *  cells and materials information.
 */
class MCNPGeometry {
  int pointID;
  int eventID;
  int cellID;
  int materialID;
  vector<double> pointXYZ;

  map<int, string> cell2Density;

  vector<int> volumeList;
  int nbDataCellMaterialLine;
  long nbPointsRead;
  long nps;
  string ptracPath;
  string inputPath;

  ifstream ptracFile;
  ifstream inputFile;
  string currentLine;
public:

  MCNPGeometry();

  /**
  * Class constructor.
  *
  * @param[in] ptracPath MCNP ptrac file path.
  * @param[in] inputPath MCNP inp file path.
  */
  MCNPGeometry(string ptracPath, string inputPath);

  /**
  * Class destructor.
  *
  *
  */
  virtual ~MCNPGeometry();

  /**
  * Reads the point ID number and the event ID number.
  *
  * @return A pair containing the point ID and event ID.
  */
  pair<int, int> readPointEvent();

  /**
  * Reads the cell ID number and the material ID number.
  *
  * @return a pair containing the volume ID and material ID.
  */
  pair<int, int> readCellMaterial();

  /**
  * Reads the point coordinates (x,y,z).
  *
  * @return the point coordinates as a vector of 3 doubles.
  */
  vector<double> readPoint();

  /**
  * If the maximum number of read points has not been reached: reads the next
  * particle, event, volume, material, position in PTRAC file.
  *
  * @returns 1 if successful, 0 otherwise.
  */
  int readNextPtracData(long maxReadPoint);

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
  * @param[in] *iss The pointer to the stringstream constructed from header line.
  * @return the number of integer data stored on the 2nd of each particle event
  * data block.
  */
  int getDataFromLine5Ptrac(istringstream *iss);

  /**
  * Checks that the 2nd line of each particle event data block does contain the
  * cell ID and the material ID. These information are respectively identified as
  * 17 and 18 by the PTRAC writer. The program exits if it is not the case.
  *
  * @param[in] iss The pointer to the stringstream constructed from header line.
  * @param[in] nbData The number of data expected on 2nd line of each particle
  * event data block (given by getDataFromLine5Ptrac function).
  */
  void checkDataFromLine6Ptrac(istringstream *iss, int nbData);

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
  void addCell2Density(int key, const string& value);

  /**
   * Gives the association material ID - material density.
   *
   * @return the association as a string: materialID-density.
   */
   string getMaterialDensity();

   void getNextLine();

  /**
   * Determines whether we have read the whole block data in the
   * Caution : blank line separator is identified as string of length 1...
   *
   * @returns 1 if the whole block data has been read, 0 otherwise
   */
  int finishedReading();

  /**
   * Determines whether the current is a comment
   *
   *
   * @returns 1 if current line is a comment, 0 otherwise
   */
  int isLineAComment(string lineContent);

  ifstream& getInputFile();
  const string& getInputPath();
  void setInputPath(const string& inputPath);
  long getNPS();
  long getNbPointsRead();
  ifstream& getPtracFile();
  const string& getPtracPath();
  void setPtracPath(const string& ptracPath);
  const vector<int>& getVolumeList();
  void setVolumeList(const vector<int>& volumeList);
  string getCurrentLine();
  int setCurrentLine(ifstream& inFile);
  int getPointID();
  int getEventID();
  void setPointEvent(const pair<int, int>& pointEvent);
  vector<double> getPointXyz();
  void setPointXyz(const vector<double>& pointXyz);
  int getCellID();
  int getMaterialID();
  void setCellMaterial(const pair<int, int>& cellMat);
  map<int, string>& getCell2Density();

};


#endif /* MCNPGEOMETRY_H_ */
