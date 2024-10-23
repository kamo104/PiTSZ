#include "common.h"

void parseArgs(int argc, char *argv[], po::variables_map &vm) {
  po::options_description desc("Allowed options");
  desc.add_options()("help,h", "print this message and leave")(
      "instance_filename", po::value<string>(),
      "name of the instance input file")("solution_filename",
                                         po::value<string>(),
                                         "name of the solution output file");
  po::positional_options_description pos_desc;
  pos_desc.add("instance_filename", 1);
  pos_desc.add("solution_filename", 1);

  po::store(po::command_line_parser(argc, argv)
                .options(desc)
                .positional(pos_desc)
                .run(),
            vm);
  po::notify(vm);

  if (vm.count("help") || argc < 2) {
    cerr << desc << "\n";
    exit(1);
  }
}

int main(int argc, char *argv[]) {
  po::variables_map vm;
  parseArgs(argc, argv, vm);
  string instanceFile = vm["instance_filename"].as<string>();
  string solutionFile = vm["solution_filename"].as<string>();

  Instance instance(instanceFile, true);
  Solution solution(solutionFile);

  solution.proc.reserve(instance.size);
  for (int i = 0; i < instance.size; i++) {
    // for (int i = instance.size - 1; i >= 0; i--) {
    solution.proc.emplace_back(i);
  }
  solution.score = getScore(instance, solution);
  solution.clear();
  solution.write(solution.fileStream);

  return 0;
}
