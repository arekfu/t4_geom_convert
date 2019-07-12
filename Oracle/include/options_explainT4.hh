#ifndef OPTIONS_EXPLAINT4_H
#define OPTIONS_EXPLAINT4_H

#include <string>
#include <vector>

void help();

/** \brief class to manage the options of the comparison utility
*/
class OptionsExplainT4
{
public:
  std::vector<std::string> filenames;
  bool help;
  int verbosity;

  OptionsExplainT4();
  void get_opts(int, char **);
};

#endif
