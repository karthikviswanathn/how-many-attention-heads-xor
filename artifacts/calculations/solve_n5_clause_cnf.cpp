#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kVariables = 32;

struct Clause {
  std::vector<unsigned char> literals;
  int first = 0;
  int second = 0;
};

class Solver {
 public:
  explicit Solver(std::uint64_t node_limit) : node_limit_(node_limit) {
    assignments_.fill(-1);
    occurrences_.fill(0);
  }

  void AddClause(std::uint32_t positive, std::uint32_t negative) {
    if ((positive & negative) != 0) std::abort();
    Clause clause;
    for (int vertex = 0; vertex < kVariables; ++vertex) {
      const std::uint32_t bit = std::uint32_t{1} << vertex;
      if ((positive & bit) != 0) {
        clause.literals.push_back(static_cast<unsigned char>(2 * vertex + 1));
        ++occurrences_[vertex];
      } else if ((negative & bit) != 0) {
        clause.literals.push_back(static_cast<unsigned char>(2 * vertex));
        ++occurrences_[vertex];
      }
    }
    if (clause.literals.empty()) has_empty_clause_ = true;
    clauses_.push_back(std::move(clause));
  }

  bool Solve(std::uint32_t* candidate) {
    if (has_empty_clause_) return false;
    for (int index = 0; index < static_cast<int>(clauses_.size()); ++index) {
      Clause& clause = clauses_[index];
      clause.second = clause.literals.size() == 1 ? 0 : 1;
      watchers_[clause.literals[clause.first]].push_back(index);
      if (clause.second != clause.first) {
        watchers_[clause.literals[clause.second]].push_back(index);
      }
      if (clause.literals.size() == 1) {
        const int literal = clause.literals[0];
        if (!Enqueue(literal / 2, literal % 2)) return false;
      }
    }
    if (!Enqueue(0, 0)) return false;
    return Search(0, candidate);
  }

  std::uint64_t nodes() const { return nodes_; }
  int max_depth() const { return max_depth_; }
  bool limit_exceeded() const { return limit_exceeded_; }

 private:
  bool Enqueue(int vertex, int value) {
    if (assignments_[vertex] >= 0) return assignments_[vertex] == value;
    assignments_[vertex] = static_cast<signed char>(value);
    trail_.push_back(vertex);
    return true;
  }

  int LiteralState(int literal) const {
    const int value = assignments_[literal / 2];
    if (value < 0) return -1;
    return value == literal % 2 ? 1 : 0;
  }

  bool Propagate() {
    while (propagation_index_ < trail_.size()) {
      const int vertex = trail_[propagation_index_++];
      const int false_literal = 2 * vertex + (1 - assignments_[vertex]);
      std::vector<int>& watch_list = watchers_[false_literal];
      std::size_t position = 0;
      while (position < watch_list.size()) {
        const int clause_index = watch_list[position];
        Clause& clause = clauses_[clause_index];
        int slot;
        int current_position;
        int other_position;
        if (clause.literals[clause.first] == false_literal) {
          slot = 0;
          current_position = clause.first;
          other_position = clause.second;
        } else if (clause.literals[clause.second] == false_literal) {
          slot = 1;
          current_position = clause.second;
          other_position = clause.first;
        } else {
          std::abort();
        }

        int replacement = -1;
        for (int candidate = 0;
             candidate < static_cast<int>(clause.literals.size()); ++candidate) {
          if (candidate == current_position || candidate == other_position) continue;
          if (LiteralState(clause.literals[candidate]) != 0) {
            replacement = candidate;
            break;
          }
        }
        if (replacement >= 0) {
          if (slot == 0) {
            clause.first = replacement;
          } else {
            clause.second = replacement;
          }
          watch_list[position] = watch_list.back();
          watch_list.pop_back();
          watchers_[clause.literals[replacement]].push_back(clause_index);
          continue;
        }

        const int other_literal = clause.literals[other_position];
        const int other_state = LiteralState(other_literal);
        if (other_state == 0) return false;
        if (other_state < 0 && !Enqueue(other_literal / 2, other_literal % 2)) {
          return false;
        }
        ++position;
      }
    }
    return true;
  }

  void Backtrack(std::size_t size) {
    for (std::size_t index = size; index < trail_.size(); ++index) {
      assignments_[trail_[index]] = -1;
    }
    trail_.resize(size);
    propagation_index_ = std::min(propagation_index_, size);
  }

  bool Search(int depth, std::uint32_t* candidate) {
    ++nodes_;
    max_depth_ = std::max(max_depth_, depth);
    if (nodes_ > node_limit_) {
      limit_exceeded_ = true;
      return false;
    }
    if (!Propagate()) return false;
    int vertex = -1;
    for (int current = 0; current < kVariables; ++current) {
      if (assignments_[current] < 0 &&
          (vertex < 0 || occurrences_[current] > occurrences_[vertex])) {
        vertex = current;
      }
    }
    if (vertex < 0) {
      std::uint32_t mask = 0;
      for (int current = 0; current < kVariables; ++current) {
        if (assignments_[current] == 1) mask |= std::uint32_t{1} << current;
      }
      *candidate = mask;
      return true;
    }

    const int preferred = vertex == 0 ? 0 : 1;
    const std::size_t snapshot = trail_.size();
    for (const int value : {preferred, 1 - preferred}) {
      if (Enqueue(vertex, value) && Search(depth + 1, candidate)) return true;
      if (limit_exceeded_) return false;
      Backtrack(snapshot);
    }
    return false;
  }

  std::vector<Clause> clauses_;
  std::array<std::vector<int>, 2 * kVariables> watchers_;
  std::array<signed char, kVariables> assignments_;
  std::array<int, kVariables> occurrences_;
  std::vector<int> trail_;
  std::size_t propagation_index_ = 0;
  std::uint64_t node_limit_;
  std::uint64_t nodes_ = 0;
  int max_depth_ = 0;
  bool has_empty_clause_ = false;
  bool limit_exceeded_ = false;
};

}  // namespace

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  std::size_t clause_count;
  std::uint64_t node_limit;
  if (!(std::cin >> clause_count >> node_limit)) return 2;
  Solver solver(node_limit);
  for (std::size_t index = 0; index < clause_count; ++index) {
    std::uint64_t positive;
    std::uint64_t negative;
    if (!(std::cin >> positive >> negative)) return 2;
    solver.AddClause(static_cast<std::uint32_t>(positive),
                     static_cast<std::uint32_t>(negative));
  }

  std::uint32_t candidate = 0;
  const bool satisfiable = solver.Solve(&candidate);
  if (solver.limit_exceeded()) {
    std::cout << "LIMIT " << solver.nodes() << ' ' << solver.max_depth() << '\n';
    return 3;
  }
  if (satisfiable) {
    std::cout << "candidate " << std::hex << std::setw(8) << std::setfill('0')
              << candidate << std::dec << ' ' << solver.nodes() << ' '
              << solver.max_depth() << '\n';
  } else {
    std::cout << "UNSAT " << solver.nodes() << ' ' << solver.max_depth() << '\n';
  }
  return 0;
}
