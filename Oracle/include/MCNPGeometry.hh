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
	vector<float> pointXYZ;

	map<int, string> cell2Density;

	vector<int> volumeList;
	int npoints;
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
	* @return the point coordinates as a vector of 3 floats.
	*/
	vector<float> readPoint();

	/**
	* If the maximum number of read points has not been reached: reads the next
	* particle, event, volume, material, position in PTRAC file.
	*
	* @returns 1 if successful, 0 otherwise.
	*/
	int readNextPtracData(int maxReadPoint=1000000000);

	/**
	* Reads and stores the materials density.
	*
	*/
	void readMaterialDensity();

	/**
	 * Parses the INP file, looking for the material densities.
	 *
	 *
	 */
	void parseINP();

	/**
	 * Sets the current line at the last header line of PTRAC file.
	 *
	 * @param[in] nHeaderLines The number of header lines in the PTRAC file.
	 */
	void goThroughHeaderPTRAC(int nHeaderLines);

	/**
	 * Increments the number of points read so far.
	 *
	 *
	 */
	void incrementNpoints(){
		setNpoints(npoints+1);
	}

	/**
	 * Attempts to add a new association cell ID -> material density.
	 *
	 *
	 */
	void addCell2Density(int key, string value);

	/**
	 * Gives the association material ID - material density.
	 *
	 * @return the association as a string: materialID-density.
	 */
	string getMaterialDensity(){
		string density = cell2Density[cellID];
		return (to_string(materialID)+density);
	}

	/**
	 * Determines whether we have read all the cells definition in the INP file
	 * based on blank line block separator.
	 *
	 *
	 * @returns 1 if all cells have been read, 0 otherwise
	 */
	int finishedReadingCells();

	/**
	 * Determines whether the current is a comment
	 *
	 *
	 * @returns 1 if current line is a comment, 0 otherwise
	 */
	int isLineAComment(string lineContent);


	ifstream& getInputFile() {
		return inputFile;
	}

	const string& getInputPath(){
		return inputPath;
	}

	void setInputPath(const string& inputPath) {
		this->inputPath = inputPath;
	}

	int getNpoints() {
		return npoints;
	}

	void setNpoints(int npoints){
		this->npoints = npoints;
	}

	ifstream& getPtracFile() {
		return ptracFile;
	}

	const string& getPtracPath() {
		return ptracPath;
	}

	void setPtracPath(const string& ptracPath) {
		this->ptracPath = ptracPath;
	}

	const vector<int>& getVolumeList() {
		return volumeList;
	}

	void setVolumeList(const vector<int>& volumeList) {
		this->volumeList = volumeList;
	}

	string getCurrentLine(){
		return currentLine;
	}

	int setCurrentLine(ifstream& inFile){
		if(getline(inFile, currentLine)){
			return 1;
		}
		else{
			return 0;
		}
	}

	int getPointID() {
		return pointID;
	}

	int getEventID() {
		return eventID;
	}

	void setPointEvent(const pair<int, int>& pointEvent) {
		this->pointID = pointEvent.first;
		this->eventID = pointEvent.second;
	}

	const vector<float>& getPointXyz() const {
		return pointXYZ;
	}

	void setPointXyz(const vector<float>& pointXyz) {
		pointXYZ = pointXyz;
	}

	int getCellID() {
		return cellID;
	}

	int getMaterialID() {
		return materialID;
	}

	void setCellMaterial(const pair<int, int>& cellMat) {
		this->cellID = cellMat.first;
		this->materialID = cellMat.second;
	}

	map<int, string>& getCell2Density(){
		return cell2Density;
	}

};


#endif /* MCNPGEOMETRY_H_ */
