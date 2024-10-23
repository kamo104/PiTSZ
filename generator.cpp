#include "common.h"

void parseArgs(int argc, char *argv[], po::variables_map &vm) {
  po::options_description desc("Allowed options");
  desc.add_options()("help,h", "print this message and leave")(
      "instance_size", po::value<int>(), "size of the instance")(
      "output_filename", po::value<string>(), "name of the output file");

  boost::program_options::positional_options_description pos_desc;
  pos_desc.add("instance_size", 1);
  pos_desc.add("output_filename", 1);

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

  string outFile = vm["output_filename"].as<string>();
  int size = vm["instance_size"].as<int>();

  Instance instance(outFile, size);
  instance.generate();
  instance.write(instance.fileStream);
}
