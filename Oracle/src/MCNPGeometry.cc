/*
 * MCNPGeometry.cpp
 *
 *  Created on: 7 d�c. 2018
 *      Author: jofausti
 */

#include "MCNPGeometry.hh"
#include <cctype>

/**
	Class constructor

	@param ptracPath MCNP ptrac file path
	@param inputPath MCNP inp file path
*/
MCNPGeometry::MCNPGeometry(string ptracPath, string inputPath) {
	npoints = 0;
	volumeList = {};

	this->ptracPath=ptracPath;
	this->inputPath=inputPath;
	ptracFile.open(ptracPath);
	if(ptracFile.fail()){
		cerr << "PTRAC file not found." << endl;
		exit(EXIT_FAILURE);
	}
	inputFile.open(inputPath);
	if(inputFile.fail()){
		cerr << "INP file not found." << endl;
		exit(EXIT_FAILURE);
	}
}

MCNPGeometry::~MCNPGeometry() {
	// TODO Auto-generated destructor stub
}

/**
    Returns the point ID number and the event ID number

    @return a pair containing the point ID and event ID
 */
pair<int, int> MCNPGeometry::readPointEvent() {
	getline(ptracFile, currentLine);
	istringstream iss(getCurrentLine());
	int pointID, eventID;
	iss >> pointID >> eventID;
	return {pointID, eventID};
}

/**
    Returns the volume ID number and the material ID number

    @return a pair containing the volume ID and material ID
 */
pair<int, int> MCNPGeometry::readCellMaterial() {
	getline(ptracFile, currentLine);
	istringstream iss(currentLine);
	int dummy1, dummy2, dummy3, dummy4, volumeID, materialID;
	iss >> dummy1 >> dummy2 >> dummy3 >> dummy4 >> volumeID >> materialID;
	return {volumeID, materialID};
}

/**
    Returns the point coordinates (x,y,z)

    @return the point coordinates as a vector of 3 floats
 */
vector<float> MCNPGeometry::readPoint() {
	getline(ptracFile, currentLine);
	istringstream iss(currentLine);
	float pointX, pointY, pointZ;
	iss >> pointX >> pointY >> pointZ;
	return {pointX, pointY, pointZ};
}

/**
    If the maximum number of read points has not been reached: reads the next particle, event, volume, material, position in PTRAC file

	@returns
 */
void MCNPGeometry::readNextPtracData(int maxReadPoint) {
	if(ptracFile && !ptracFile.eof() && getNpoints() < maxReadPoint){
		incrementNpoints();
		setPointEvent(readPointEvent());
		setCellMaterial(readCellMaterial());
		setPointXyz(readPoint());
	}
}

/**
	Reads and stores the materials density

 */
void MCNPGeometry::readMaterialDensity(){
	istringstream iss(currentLine);
	int cellNum, matNum;
	string density;
	if (iss >> cellNum){
		iss >> matNum;
		if(matNum == 0){
			addCell2Density(cellNum, "void");
		}
		else{
			iss >> density;
			addCell2Density(cellNum, density);
		}
	//	to_return = 1;
	}
//	else{
	//	to_return = 0;
//	}
//	return to_return;
}

void MCNPGeometry::addCell2Density(int key, string value){
	if (cell2Density.find(key) == cell2Density.end()){
		cell2Density[key] = value;
	}
}



/**
    Parses the INP file, looking for the material densities

	@returns
 */
void MCNPGeometry::parseINP() {
	if (inputFile){
		while(getline(inputFile, currentLine)){
			if (!isLineAComment(currentLine) && isdigit(currentLine[0])){
				readMaterialDensity();
			}
		}
	}
}

/**
	Determines whether we have read all the cells definition in the INP file based on blank line block separator

	@returns 1 if all cells have been read, 0 otherwise
 */
int MCNPGeometry::finishedReadingCells(){
	if(getline(inputFile, currentLine)){
		return currentLine.length() == 0;
	}
	else{
		return 0;
	}
}

/**
	Determines whether the current is a comment

	@returns 1 if current line is a comment, 0 otherwise
 */
int MCNPGeometry::isLineAComment(string lineContent){
	return lineContent[0] == 'c' || lineContent[0] == 'C';
	//size_t found = lineContent.find_first_not_of(" \t");
	//if(found != string::npos) && (line[found])
}

/**
 	 Sets the current line at the last header line of PTRAC file

	@returns
 */
void MCNPGeometry::goThroughHeaderPTRAC(int nHeaderLines){
	for (int ii=0; ii<nHeaderLines; ii++){
		getline(ptracFile, currentLine);
	}
}
