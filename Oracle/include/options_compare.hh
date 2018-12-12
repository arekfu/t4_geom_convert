#ifndef OPTIONS_COMPARE_H
#define OPTIONS_COMPARE_H

#include <vector>
#include <string>

using namespace std;

void
help();


enum SamplingMethod { SobolSampling, RandomSampling };


/** \brief class to manage the options of the comparison utility
*/
class OptionsCompare {
  public:
    vector<string>      filenames;
    bool                help;
    int                 verbosity;

    OptionsCompare();
    void get_opts(int, char **);

  private:
    void check_argv(int,int);

};

#endif
