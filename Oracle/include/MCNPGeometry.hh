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

#include "PTRACFormat.hh"
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

struct PTRACRecord {
  long pointID, eventID;
  long cellID, materialID;
  std::vector<double> point;
};

struct PTRACRecordIndices {
  int event, cell, mat, px, py, pz;
  long nbDataSrcLong, nbDataSrcDouble;
};

class MCNPPTRAC
{
protected:
  long nbPointsRead;
  PTRACRecord record;

public:
  MCNPPTRAC();
  virtual ~MCNPPTRAC(){};

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
};

class MCNPPTRACBinary : public MCNPPTRAC
{
protected:
  std::ifstream ptracFile;
  PTRACRecordIndices indices;

public:
  /**
     * @param[in] ptracPath MCNP ptrac file path.
     */
  MCNPPTRACBinary(std::string const &ptracPath);

  /**
     * If the maximum number of read points has not been reached: reads the next
     * particle, event, volume, material, position in PTRAC file.
     *
     * @returns true if successful, false otherwise.
     */
  bool readNextPtracData(long maxReadPoint);

protected:
  /**
   * Reads the header
   */
  void parseHeader();

  void skipHeader();

  void skipPtracInputData();

  /// return the indices of the field IDs
  void parseVariableIDs();

  void parsePTRACRecord();
};

/** \class MCNPGeometry.
 *  \brief Class for dealing with MCNP geometry.
 *
 *  This class reads the MCNP INP and PTRAC files and gives pseudo-random points,
 *  cells and materials information.
 */
class MCNPGeometry
{
  std::map<unsigned long, std::pair<unsigned long, std::string>> cell2Density;

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
   * Handle the LIKE n BUT syntax
   */
  void handleLikeNBut(unsigned long cellNum, std::string::size_type pos);

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
  std::string getCellDensity(unsigned long cellID) const;

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
   * Determines whether the current has a continuation character at the end
   *
   *
   * @returns true if current line ends in a continuation character
   */
  bool lineEndsInContinuation(std::string const &lineContent) const;

  /**
   * Determines whether the current is a continuation
   *
   *
   * @returns true if current line starts at column < 6
   */
  bool isLineAContinuation(std::string const &lineContent) const;

  /**
   * Determines whether the line is empty (only spaces)
   *
   * @returns true if the line is empty
   */
  bool isLineEmpty(std::string const &lineContent) const;

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
  std::map<unsigned long, std::pair<unsigned long, std::string>> &getCell2Density();
};

/*******************************************************
*  utility functions for parsing FORTRAN binary files  *
********************************************************/

template <typename T>
T readBinary(std::istream &stream)
{
  T value;
  stream.read(reinterpret_cast<char *>(&value), sizeof(T) / sizeof(char));
  if (!stream) {
    throw std::logic_error("bad stream state after read");
  }
  return value;
}

inline std::string readBinary(std::istream &file, size_t length)
{
  std::string buffer(length, '\0');
  file.read(&buffer[0], length);
  if (!file) {
    throw std::logic_error("bad stream state after read");
  }
  return buffer;
}

inline std::string readRecord(std::istream &file)
{
  const int rec_len_start = readBinary<int>(file);
  std::string buffer = readBinary(file, rec_len_start);
  const int rec_len_end = readBinary<int>(file);
  if (rec_len_start != rec_len_end) {
    throw std::logic_error("mismatched record length");
  }
  return buffer;
}

inline std::tuple<> reinterpretBuffer(std::istream &, std::tuple<> const &)
{
  return std::make_tuple();
}

template <typename T, typename... Ts>
std::tuple<T, Ts...> reinterpretBuffer(std::istream &stream, std::tuple<T, Ts...> const &)
{
  T value = readBinary<T>(stream);
  return std::tuple_cat(std::make_tuple(value), reinterpretBuffer(stream, std::tuple<Ts...>()));
}

template <typename... Ts>
std::tuple<Ts...> reinterpretBuffer(std::istream &stream)
{
  return reinterpretBuffer<Ts...>(stream, std::tuple<Ts...>());
}

template <typename... Ts>
std::tuple<Ts...> reinterpretBuffer(std::string const &buffer)
{
  std::stringstream stream(buffer);
  return reinterpretBuffer<Ts...>(stream);
}

#endif /* MCNPGEOMETRY_H_ */
