#pragma once

#include <algorithm>
#include <boost/program_options.hpp>
#include <format>
#include <fstream>
#include <iostream>
#include <istream>
#include <random>
#include <vector>

using namespace std;
namespace po = boost::program_options;

inline int randomInt(int low, int high) {
  return rand() % (high - low + 1) + low;
}

struct File {
  string filename;
  fstream fileStream;

  File();
  File(const string &name) : filename(name) { open(filename); }
  virtual ~File(){};

  void open(const string &name) {
    filename = name;
    open();
  }
  void open() {
    fileStream = fstream(filename, ios::in | ios::out);
    if (fileStream.is_open())
      return;

    fileStream.open(filename, ios::out);
    if (!fileStream.is_open()) {
      throw runtime_error("Cannot create file: " + filename);
    }
    fileStream.close();

    fileStream.open(filename, ios::in | ios::out);
    if (!fileStream.is_open()) {
      throw runtime_error("Cannot open file: " + filename);
    }
  }

  void clear(const string &name) {
    filename = name;
    clear();
  }
  void clear() {
    fileStream.close();
    fileStream.open(filename, ios::out | ios::trunc);
    if (!fileStream.is_open()) {
      throw runtime_error("Failed to clear the file: " + filename);
    }
    open();
  }
  void virtual read(istream &input) = 0;
  void virtual write(ostream &output) = 0;
};

struct Solution : public File {
  int score;
  vector<int> proc;

  Solution();
  Solution(const string filename, bool load = false) : File(filename) {
    if (load)
      read(fileStream);
  };

  void read(istream &input) override {
    input >> score;
    int a;
    while (input >> a) {
      proc.emplace_back(a - 1);
    }
  }
  void write(ostream &output) override {
    output << score << '\n';
    for (int i : proc) {
      output << i + 1 << ' ';
    }
  }
};

struct Instance : public File {
  int size;
  vector<pair<int, int>> begin_end;
  vector<vector<int>> cost;

  Instance();
  Instance(const string &filename, bool load = false) : File(filename) {
    if (load)
      read(fileStream);
  }
  Instance(const string &filename, int n, bool load = false)
      : Instance(filename, load) {
    size = n;
  }

  void read(istream &input) override {
    input >> size;
    begin_end.reserve(size);
    pair<int, int> p;
    for (int i = 0; i < size; i++) {
      // pair<int, int> p;
      input >> p.first >> p.second;
      begin_end.emplace_back(p);
    }
    for (int i = 0; i < size; i++) {
      vector<int> v1;
      for (int j = 0; j < size; j++) {
        int a;
        input >> a;
        v1.emplace_back(a);
      }
      cost.emplace_back(v1);
    }
  }

  void write(ostream &output) override {
    output << size << '\n';
    for (const auto &[start, end] : begin_end) {
      output << start << end << '\n';
    }

    for (const auto &v1 : cost) {
      for (const auto &c : v1) {
        output << c << ' ';
      }
      output << '\n';
    }
  }

  void generate(int n = -1) {
    srand(time(0));

    if (n != -1) {
      size = n;
    }

    int d_mean = size + size / 10 + size / 8;
    int d_stddev = 4 * size + d_mean;

    int p_mean = size / 10;
    int p_stddev = size / 10 + p_mean;

    int s_mean = size / 100 + 5;
    int s_stddev = s_mean;

    default_random_engine generator(time(0));
    normal_distribution<double> d_dist(d_mean, d_stddev);
    normal_distribution<double> p_dist(p_mean, p_stddev);
    normal_distribution<double> s_dist(s_mean, s_stddev);

    begin_end.reserve(size);
    for (int i = 0; i < size; ++i) {
      begin_end[i] = {abs(p_dist(generator)), abs(d_dist(generator))};
    }

    // Generate the cleaning times matrix Sij
    cost.reserve(size);
    for (int i = 0; i < size; ++i) {
      cost[i].reserve(size);
      for (int j = 0; j < size; ++j) {
        if (i == j) {
          cost[i][j] = 0;
        } else {
          cost[i][j] = max(0, (int)s_dist(generator));
        }
      }
    }
  }
};

inline int getScore(const Instance &instance, const Solution &solution) {
  int score = 0;
  int currentTime = 0;

  for (int idx = 0; idx < solution.proc.size(); ++idx) {
    int task = solution.proc[idx];
    int p_j = instance.begin_end[task].first;
    int d_j = instance.begin_end[task].second;

    if (idx > 0) {
      int previousTask = solution.proc[idx - 1];
      currentTime += instance.cost[previousTask][task];
    }

    currentTime += p_j;
    int C_j = currentTime;
    int Y_j = min(p_j, max(0, C_j - d_j));
    score += Y_j;
  }

  return score;
}
