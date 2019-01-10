#ifndef OPTIONS_COMPARE_H
#define OPTIONS_COMPARE_H

#include <string>
#include <vector>

void help();

/** \brief class to manage the options of the comparison utility
*/
class OptionsCompare
{
public:
  std::vector<std::string> filenames;
  bool help;
  int verbosity;
  long npoints;
  double delta;

  OptionsCompare();
  void get_opts(int, char **);

private:
  void check_argv(int, int);
};

#endif
