#include "options_compare.hh"
#include "help.hh"
#include <cstdio>
#include <cstdlib>
#include <unistd.h>

using namespace std;

/** \brief Display the command line help
 */
void help()
{
  std::cout << endl
            << "oracle\n"
            << "\n  Compare MCNP and T4 geometries check that they are weakly equivalent."
            << "\n  A point is assumed to match by checking the name of the composition at"
            << "\n  that point in each geometry."
            << "\n\nUSAGE"
            << "\n\toracle [options] jdd.t4 jdd.inp ptrac" << endl
            << endl;

  std::cout << "INPUT FILES" << endl;
  edit_help_option("jdd.t4", "A TRIPOLI-4 input file converted from MCNP INP file.");
  edit_help_option("jdd.inp", "The MCNP INP file that was used for the conversion.");
  edit_help_option("ptrac", "The MCNP PTRAC file corresponding to the INP file.");

  std::cout << endl
            << "OPTIONS" << endl;
  edit_help_option("-V, --verbose", "Increase output verbosity.");
  edit_help_option("-h, --help", "Displays this help message.");
  edit_help_option("-n, --npts", "Maximum number of tested points.");
  edit_help_option("-d, --delta", "Distance to the nearest surface below which a failed test is ignored.");
  edit_help_option("-g, --guess-material-assocs", "guess the materials correspondence based on the first few points");

  std::cout << endl;
}

/** \brief Constructor of the class
*/
OptionsCompare::OptionsCompare() : help(false),
                                   verbosity(0),
                                   npoints(2000000),
                                   delta(1.0E-7),
                                   guessMaterialAssocs(false)
{
}

/** \brief Get the options set in the command line
 * @param[in] argc The number of arguments in the command line
 * @param[in] argv The splitted command line
 */
void OptionsCompare::get_opts(int argc, char **argv)
{

  if (argc <= 3) {
    help = true;
    return;
  } else {

    for (int i = 1; i < argc; i++) {
      string opt(argv[i]);

      if (opt.compare("--help") == 0 || opt.compare("-h") == 0) {
        help = true;
        return;
      } else if (opt.compare("--verbose") == 0 || opt.compare("-V") == 0) {
        ++verbosity;
      } else if (opt.compare("--guess-material-assocs") == 0 || opt.compare("-g") == 0) {
        guessMaterialAssocs = true;
      } else if (opt.compare("--npts") == 0 || opt.compare("-n") == 0) {
        int nv = 1;
        check_argv(argc, i + nv);
        npoints = int_of_string(argv[i + 1]);
        if (npoints <= 0) {
          std::cout << "Warning: npoints<=0. Setting npoints=100." << std::endl;
          npoints = 100;
        }
        i += nv;
      } else if (opt.compare("--delta") == 0 || opt.compare("-d") == 0) {
        int nv = 1;
        check_argv(argc, i + nv);
        istringstream os(argv[i + 1]);
        os >> delta;
        if (delta <= 0) {
          std::cout << "Warning: delta<=0. Setting delta=1.0e-7" << std::endl;
          delta = 1.0e-7;
        }
        i += nv;
      } else {
        filenames.push_back(opt);
      }
    }
  }

  // check that all the input files exist
  for (vector<string>::const_iterator fname = filenames.begin(), efname = filenames.end();
       fname != efname; ++fname) {
    if (access(fname->c_str(), R_OK) == -1) {
      cout << "'" << *fname << "': unknown option or unreachable file." << endl;
      cout << "Try '" << argv[0] << " --help for more information.\n"
           << endl;
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
void OptionsCompare::check_argv(int argc, int ip)
{
  if (ip >= argc) {
    cout << "\nError in command line.\n"
         << endl;
    exit(EXIT_FAILURE);
  }
}
