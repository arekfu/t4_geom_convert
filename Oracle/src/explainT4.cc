#include <chrono>
#include <iostream>
#include <fstream>
#include "t4coreglob.hh"
#include "T4Geometry.hh"
#include "options_explainT4.hh"
//
// geom includes
//
extern "C" {
#include "geom.h"
#include "geutil.h"
#include "geread.h"
#include "geextlib.h"
#include "geintlib.h"
}


int strictness_level = 3; //Global variable required by T4 libraries


void containedInVolumes(Ge_float const x, Ge_float const y, Ge_float const z)
{
  Ge_maille *maille = nullptr;
  std::vector<int> numvols;
  for(int rankvol=0; rankvol<ge_volu_tab_info.ge_nbvolu; ++rankvol) {
    Ge_volu *volu = ge_get_volu_by_rank(rankvol);
    if(volu->fictif) {
      continue;
    }
    ST_volu_pos pos = ge_volu_pos(volu, x, y, z, maille);
    if((pos == ST_VOLU_INT || pos == ST_VOLU_FRONT) && volu->volu_type != GE_VOLU_RESEAU) {
      numvols.push_back(volu->numvol);
    }
  }
  std::cout << "Point contained in the following volumes:";
  for(auto const &numvol: numvols) {
    std::cout << ' ' << numvol;
  }
  std::cout << std::endl;
}


bool explainVolume(Ge_float const x, Ge_float const y, Ge_float const z, int const numvol, std::string const &prefix)
{
  bool success = true;
  int rankvol = numvol_to_rankvol(numvol);

  if(rankvol >= 0) {
    Ge_volu *volu = ge_volu_tab_info.ge_volu[rankvol];
    std::cout << prefix << "* volume info: num      = " << volu->numvol
      << '\n' << prefix << "|              rank     = " << volu->rankvol
      << '\n' << prefix << "|              type     = " << volu->volu_type
      << '\n' << prefix << "|              fictive  = " << volu->fictif
      << '\n';

    // treat surface-based volumes
    if(volu->volu_type == GE_VOLU_EQUA) {
      auto const data = volu->volu_descr.volu_equa.equa_data;
      int const nb_plus = data.nb_plus;
      int const nb_moins = data.nb_moins;
      std::cout << prefix << "|              nb_surf+ = " << nb_plus
        << '\n' << prefix << "|              nb_surf- = " << nb_moins
        << '\n';
      std::string moreprefix = prefix + "| ";
      for(int iplus=0; iplus<nb_plus; ++iplus) {
        auto const surf = data.surface_plus_tab[iplus];
        auto surf_sign = ge_surf_pos(surf, x, y, z);
        bool const thisSurfSuccess = surf_sign == GE_SURF_PLUS;
        success = success && thisSurfSuccess;
        std::cout << moreprefix << "+ surf: num  = " << surf->numsurf
          << '\n' << moreprefix << "+       rank = " << surf->ranksurf
          << '\n' << moreprefix << "+       sign = " << ((surf_sign == GE_SURF_PLUS) ? '+' : '-')
          << '\n' << moreprefix << "+       satisfied? " << (thisSurfSuccess ? "OK" : "FAILED")
          << '\n';
      }
      for(int iminus=0; iminus<nb_moins; ++iminus) {
        auto const surf = data.surface_moins_tab[iminus];
        auto surf_sign = ge_surf_pos(surf, x, y, z);
        bool const thisSurfSuccess = surf_sign == GE_SURF_MOINS;
        success = success && thisSurfSuccess;
        std::cout << moreprefix << "- surf: num  = " << surf->numsurf
          << '\n' << moreprefix << "-       rank = " << surf->ranksurf
          << '\n' << moreprefix << "-       sign = " << ((surf_sign == GE_SURF_PLUS) ? '+' : '-')
          << '\n' << moreprefix << "-       satisfied? " << (thisSurfSuccess ? "OK" : "FAILED")
          << '\n';
      }
    }

    // treat operators
    for(int idef=0; idef<volu->nb_def; ++idef) {
      auto const &op = volu->def_operator[idef];
      switch(op.oper_type) {
        case GE_OPERATOR_UNION:
          {
            auto const &reunion_arg = op.operator_arg.reunion_arg;
            std::cout << prefix << "* operator UNION, " << reunion_arg.nb_arg << " args\n";
            bool unionSuccess = false;
            for(int iarg=0; iarg<reunion_arg.nb_arg; ++iarg) {
              Ge_volu *volu_union = reunion_arg.reunion[iarg];
              int const subnumvol = volu_union->numvol;
              std::cout << prefix << "(U)recursing into subvolume " << subnumvol << '\n';
              bool const subVolumeSuccess = explainVolume(x, y, z, subnumvol, prefix + "| ");
              unionSuccess = unionSuccess || subVolumeSuccess;
            }
            std::cout << prefix << "* operator UNION success = " << (unionSuccess ? "OK" : "FAILED") << '\n';
            success = success || unionSuccess;
          }
          break;
        case GE_OPERATOR_INTER:
          {
            auto const &inter_arg = op.operator_arg.inter_arg;
            std::cout << prefix << "* operator INTE, " << inter_arg.nb_arg << " args\n";
            bool interSuccess = true;
            for(int iarg=0; iarg<inter_arg.nb_arg; ++iarg) {
              Ge_volu *volu_inter = inter_arg.inter[iarg];
              int const subnumvol = volu_inter->numvol;
              std::cout << prefix << "(I)recursing into subvolume " << subnumvol << '\n';
              bool const subVolumeSuccess = explainVolume(x, y, z, subnumvol, prefix + "| ");
              interSuccess = interSuccess && subVolumeSuccess;
            }
            std::cout << prefix << "* operator INTE success = " << (interSuccess ? "OK" : "FAILED") << '\n';
            success = success && interSuccess;
          }
          break;
        default:
          break;
      }
    }

    std::cout << prefix << "* volume " << numvol << ": " << (success ? "OK" : "FAILED") << '\n';
  } else {
    std::cout << prefix << "* volume not found\n";
  }

  return success;
}

void explain(OptionsExplainT4 const &options)
{
  T4Geometry t4Geom(options.filenames[0]);
  std::ifstream iFile(options.filenames[1]);

  Ge_float x, y, z;
  long volID;
  while(iFile) {
    iFile >> x >> y >> z >> volID;
    if(!iFile) {
      break;
    }
    std::cout << "Inspecting point (" << x << ", " << y << ", " << z
      << "), volume " << volID << "?\n";
    containedInVolumes(x, y, z);
    explainVolume(x, y, z, volID, "");
    std::cout << std::endl;
  }
}

int main(int argc, char **argv)
{
  auto start = std::chrono::system_clock::now();
  std::cout << "*** Tripoli-4 geometry query ***" << endl;
  t4_output_stream = &cout;
  t4_language = T4_ENGLISH;

  // ---- Read options ----
  OptionsExplainT4 options;
  options.get_opts(argc, argv);
  if (options.help) {
    help();
    exit(EXIT_SUCCESS);
  }

  explain(options);

  auto end = std::chrono::system_clock::now();
  std::chrono::duration<double> elapsed_seconds = end - start;
  std::cout << "Elapsed time: " << elapsed_seconds.count() << "s\n";
  return 0;
}
