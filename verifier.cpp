#include "common.h"

pair<bool, int> verify(const Instance &instance, const Solution &solution) {
  int size = instance.size;

  // check number of used processes
  if (size != solution.proc.size()) {
    cerr << format("The number of processes used({}) is different than in the "
                   "instance({})",
                   solution.proc.size(), size);
    return {false, 0};
  }

  // check processess range
  bool c3 = std::find_if(solution.proc.begin(), solution.proc.end(),
                         [size](int n) { return n <= 0 || n > size; }) !=
            solution.proc.end();
  if (!c3) {
    cerr << format(
        "The solution contains a process outside the allowed range({}:{})", 1,
        size);
    return {false, 0};
  }

  // check unique processess
  std::vector<bool> used(size, false);
  for (int i = 0; i < solution.proc.size(); i++) {
    used[i] = true;
  }
  const auto &it = std::find(used.begin(), used.end(), false);
  if (it != used.end()) {
    cerr << format("The solution doesn't include process {}", it._M_offset + 1);
    return {false, 0};
  }

  // check the score
  int s1 = getScore(instance, solution);
  int s2 = solution.score;
  if (getScore(instance, solution) != solution.score) {
    cerr << format(
        "The raported score({}) is different from the calculated({})", s1, s2);
    return {false, 0};
  }
  return {true, s1};
}

void parseArgs(int argc, char *argv[], po::variables_map &vm) {
  po::options_description desc("Allowed options");
  desc.add_options()("help,h", "print this message and leave")(
      "instance_filename", po::value<string>(),
      "name of the instance input file")("solution_filename",
                                         po::value<string>(),
                                         "name of the solution input file");
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
  Solution solution(solutionFile, true);

  const auto &ret = verify(instance, solution);
  if (ret.first) {
    cout << ret.second;
  }

  return 0;
}
