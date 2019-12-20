#ifndef OPTIONS_COMPARE_H
#define OPTIONS_COMPARE_H

#include <string>
#include <vector>
#include <memory>
#include "PTRACFormat.hh"

void help();

/** \brief class to manage the options of the comparison utility
*/
class OptionsCompare
{
public:
  std::vector<std::string> filenames;
  bool help;
  int verbosity;
  std::unique_ptr<long> npoints;
  double delta;
  bool guessMaterialAssocs;
  PTRACFormat ptracFormat;

  OptionsCompare();
  void get_opts(int, char **);

private:
  void check_argv(int, int);
};

#endif
