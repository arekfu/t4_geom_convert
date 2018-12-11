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
    int                 lang;
    bool                help;
    double              bbox[6]; // xmin, ymin, zmin, xmax, ymax, zmax
    int                 n_points;
    SamplingMethod      sampling_method;
    int                 verbosity;

    OptionsCompare();
    void get_opts(int, char **);

  private:
    void check_lang(int);
    void check_argv(int,int);

};

#endif
