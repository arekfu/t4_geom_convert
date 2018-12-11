#include "help.hh"
#include "options_compare.hh"
#include <cstdlib>
#include <cstdio>
#include <unistd.h>

using namespace std;

/** \brief Display the command line help
 */
void
help()
{
  std::cout << endl
    << "compare_geoms\n"
    << "\n  Compare geometries in several input files and check that they are the"
    << "\n  same by sampling points in a given bounding box."
    << "\n  A point is assumed to match be checking the name of the composition at"
    << "\n  that point in each geometry."
    << "\n\nUSAGE"
    << "\n\tcompare_geoms [options] jdd.t4 jdd.t4 [...]" << endl <<
    endl;

  std::cout << "INPUT FILES" << endl;
  edit_help_option("<file>", "A TRIPOLI-4 input file that may contain any geometry supported by TRIPOLI-4.");

  std::cout << endl << "OPTIONS" << endl;
  edit_help_option("-n, --n-points <n_points>", "number of points to be samples (default: 1000).");
  edit_help_option("-l, --lang <language>", "Specify the language used in the input files. <language> equals 0 (english), 1 (french) or 2 (old, default).");
  edit_help_option("--bbox x0 y0 z0 x1 y1 z1","Define the bounding box (in cm) for the point coordinates (default: -50 -50 -50 50 50 50).");
  edit_help_option("--sampling <method>","Specify how to sample points. Must be one of: sobol (default), random.");
  edit_help_option("-V, --verbose", "Increase output verbosity.");
  edit_help_option("-h, --help", "Displays this help message.");

  std::cout << endl;
}


/** \brief Constructor of the class
*/
OptionsCompare::OptionsCompare() :
  lang(2), // 0->english, 1->french, 2->old
  help(false),
  n_points(1000),
  sampling_method(SobolSampling),
  verbosity(0)
{
  bbox[0] = -50.;
  bbox[1] = -50.;
  bbox[2] = -50.;
  bbox[3] = 50.;
  bbox[4] = 50.;
  bbox[5] = 50.;
}

/** \brief Get the options set in the command line
 * \param argc The number of arguments in the command line
 * \param argv The splitted command line
 */
void OptionsCompare::get_opts(int argc, char **argv)
{
  int nv; // number of expected arguments for a given option

  if(argc<=2){
    // not allowed
    help = true;
    return;
  } else {

    for(int i=1; i<argc; i++) {
      string opt(argv[i]);

      if(opt.compare("--help")==0 || opt.compare("-h") == 0) {
        help = true;
        return;
      } else if(opt.compare("--lang") == 0 || opt.compare("-l") == 0) {
        // get the language
        nv = 1;
        check_argv(argc, i+nv);
        if(strcmp(argv[i+1], "english") == 0)
          lang = 0;
        else if(strcmp(argv[i+1], "french") == 0)
          lang = 1;
        else if(strcmp(argv[i+1], "old") == 0)
          lang = 2;
        else
          lang = int_of_string(argv[i+1]);
        check_lang(lang);
        i+=nv;
      } else if(opt.compare("--bbox") == 0) {
        // get the frame of the window
        nv = 6;
        check_argv(argc,i+nv);
        bbox[0] = double_of_string(argv[i+1]);
        bbox[1] = double_of_string(argv[i+2]);
        bbox[2] = double_of_string(argv[i+3]);
        bbox[3] = double_of_string(argv[i+4]);
        bbox[4] = double_of_string(argv[i+5]);
        bbox[5] = double_of_string(argv[i+6]);
        i+=nv;
      } else if(opt.compare("--n-points")==0 || opt.compare("-n") == 0) {
        nv = 1;
        check_argv(argc, i+nv);
        n_points = int_of_string(argv[i+1]); //(int)atof(argv[i+1]);
        if(n_points<=0) {
          std::cout << "Warning: n_points<=0. Setting n_points=100." << std::endl;
          n_points=100;
        }
        i+=nv;
      } else if(opt.compare("--verbose")==0 || opt.compare("-V") == 0) {
        ++verbosity;
      } else if(opt.compare("--sampling")==0) {
        nv = 1;
        check_argv(argc, i+nv);
        if(strcmp(argv[i+1], "sobol") == 0)
          sampling_method = SobolSampling;
        else if(strcmp(argv[i+1], "random") == 0)
          sampling_method = RandomSampling;
        else {
          cout << "invalid option value for --sampling: "
            << argv[i+1]
            << "\n must be one of: sobol, random" << endl;
          exit(EXIT_FAILURE);
        }
        i+=nv;
      } else {
        filenames.push_back(opt);
      }
    }
  }

  // check that all the input files exist
  for(vector<string>::const_iterator fname=filenames.begin(), efname=filenames.end();
      fname!=efname; ++fname) {
    if(access(fname->c_str(), R_OK)==-1) {
      cout << "'" << *fname << "': unknown option or unreachable file." << endl;
      cout << "Try '" << argv[0] << " --help for more information.\n" << endl;
      exit(EXIT_FAILURE);
    }
  }

}

/** \brief Check if the position of the last value for an option is compatible
 * with the line command line.
 * \param argc The number of arguments in the line command.
 * \param ip   The expected position of the last value of the option in the
 * commmand line.
 */
void
OptionsCompare::check_argv(int argc, int ip)
{
  if ( ip >= argc )
  {
    cout << "\nError in command line.\n" << endl;
    exit(EXIT_FAILURE);
  }
}

/** \brief Check the language
 * \param lang  The language
 */
void
OptionsCompare::check_lang(int lang)
{
  if (! ( lang == 0 || lang == 1 || lang == 2)) {
    cout << "\nWrong language option. Use : 0 (english), 1 (french) or 2 (old).\n" << endl;
    exit(EXIT_FAILURE);
  }
}
