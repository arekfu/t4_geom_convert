#include "options_explainT4.hh"
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
            << "explainT4\n"
            << "\n  Explain why a point belongs or not to a T4 cell."
            << "\n\nUSAGE"
            << "\n\texplainT4 [options] jdd.t4 points_file" << endl
            << endl;

  std::cout << "INPUT FILES" << endl;
  edit_help_option("jdd.t4", "A TRIPOLI-4 input file with the geometry to query.");
  edit_help_option("points_file", "A file of lines of the form <x> <y> <z> <volID>.");

  std::cout << endl
            << "OPTIONS" << endl;
  edit_help_option("-V, --verbose", "Increase output verbosity.");
  edit_help_option("-h, --help", "Displays this help message.");

  std::cout << endl;
}

/** \brief Constructor of the class
*/
OptionsExplainT4::OptionsExplainT4() : help(false),
                                   verbosity(0)
{
}

/** \brief Get the options set in the command line
 * @param[in] argc The number of arguments in the command line
 * @param[in] argv The splitted command line
 */
void OptionsExplainT4::get_opts(int argc, char **argv)
{

  if (argc <= 2) {
    help = true;
    return;
  }

  for (int i = 1; i < argc; i++) {
    string opt(argv[i]);

    if (opt.compare("--help") == 0 || opt.compare("-h") == 0) {
      help = true;
      return;
    } else if (opt.compare("--verbose") == 0 || opt.compare("-V") == 0) {
      ++verbosity;
    } else {
      filenames.push_back(opt);
    }
  }

  // check that all the input files exist
  for(auto const &fname: filenames) {
    if (access(fname.c_str(), R_OK) == -1) {
      cout << "'" << fname << "': unknown option or unreachable file." << endl;
      cout << "Try '" << argv[0] << " --help for more information.\n"
           << endl;
      exit(EXIT_FAILURE);
    }
  }
}
