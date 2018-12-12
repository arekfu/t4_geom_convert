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
    << "oracle\n"
    << "\n  Compare MCNP and T4 geometries check that they are weakly equivalent."
    << "\n  A point is assumed to match by checking the name of the composition at"
    << "\n  that point in each geometry."
    << "\n\nUSAGE"
    << "\n\toracle [options] jdd.t4 jdd.inp" << endl <<
    endl;

  std::cout << "INPUT FILES" << endl;
  edit_help_option("jdd.t4", "A TRIPOLI-4 input file converted from MCNP INP file.");
  edit_help_option("jdd.inp", "The MCNP INP file that was used for the conversion.");
  edit_help_option("ptrac", "The MCNP PTRAC file corresponding to the INP file.");

  std::cout << endl << "OPTIONS" << endl;
  edit_help_option("-V, --verbose", "Increase output verbosity.");
  edit_help_option("-h, --help", "Displays this help message.");

  std::cout << endl;
}


/** \brief Constructor of the class
*/
OptionsCompare::OptionsCompare() :
  //lang(0), // 0->english, 1->french, 2->old
  help(false),
  //n_points(1000),
  //sampling_method(SobolSampling),
  verbosity(0)
  {

  }

/** \brief Get the options set in the command line
 * \param argc The number of arguments in the command line
 * \param argv The splitted command line
 */
void OptionsCompare::get_opts(int argc, char **argv){

  if(argc!=3){
    // not allowed
    help = true;
    return;
  } else {

    for(int i=1; i<argc; i++) {
      string opt(argv[i]);

      if(opt.compare("--help")==0 || opt.compare("-h") == 0) {
        help = true;
        return;
      } else if(opt.compare("--verbose")==0 || opt.compare("-V") == 0) {
        ++verbosity;
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
