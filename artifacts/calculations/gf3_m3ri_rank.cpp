#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kPanel = 8;

struct Matrix {
  std::size_t rows;
  std::size_t columns;
  std::size_t words;
  std::vector<std::uint64_t> storage;

  std::uint64_t* one(std::size_t row) {
    return storage.data() + row * 2 * words;
  }

  std::uint64_t* two(std::size_t row) {
    return one(row) + words;
  }

  const std::uint64_t* one(std::size_t row) const {
    return storage.data() + row * 2 * words;
  }

  const std::uint64_t* two(std::size_t row) const {
    return one(row) + words;
  }
};

int digit(const std::uint64_t* one, const std::uint64_t* two,
          std::size_t column) {
  const std::uint64_t bit = std::uint64_t{1} << (column & 63);
  const std::size_t word = column >> 6;
  if (one[word] & bit) return 1;
  if (two[word] & bit) return 2;
  return 0;
}

void add_rows(std::uint64_t* left_one, std::uint64_t* left_two,
              const std::uint64_t* right_one,
              const std::uint64_t* right_two, std::size_t first_word,
              std::size_t words) {
  for (std::size_t word = first_word; word < words; ++word) {
    const std::uint64_t left_zero = ~(left_one[word] | left_two[word]);
    const std::uint64_t right_zero = ~(right_one[word] | right_two[word]);
    const std::uint64_t result_one =
        (left_zero & right_one[word]) |
        (left_one[word] & right_zero) |
        (left_two[word] & right_two[word]);
    const std::uint64_t result_two =
        (left_zero & right_two[word]) |
        (left_two[word] & right_zero) |
        (left_one[word] & right_one[word]);
    left_one[word] = result_one;
    left_two[word] = result_two;
  }
}

void add_negative_row(std::uint64_t* left_one, std::uint64_t* left_two,
                      const std::uint64_t* right_one,
                      const std::uint64_t* right_two,
                      std::size_t first_word, std::size_t words) {
  add_rows(left_one, left_two, right_two, right_one, first_word, words);
}

void swap_rows(Matrix& matrix, std::size_t left, std::size_t right) {
  if (left == right) return;
  for (std::size_t word = 0; word < 2 * matrix.words; ++word) {
    std::swap(matrix.one(left)[word], matrix.one(right)[word]);
  }
}

void normalize_row(Matrix& matrix, std::size_t row, std::size_t column) {
  if (digit(matrix.one(row), matrix.two(row), column) == 2) {
    for (std::size_t word = column >> 6; word < matrix.words; ++word) {
      std::swap(matrix.one(row)[word], matrix.two(row)[word]);
    }
  }
}

std::vector<int> base_three_digits(int value, int count) {
  std::vector<int> answer(count);
  for (int index = 0; index < count; ++index) {
    answer[index] = value % 3;
    value /= 3;
  }
  return answer;
}

std::size_t power_three(int exponent) {
  std::size_t answer = 1;
  for (int index = 0; index < exponent; ++index) answer *= 3;
  return answer;
}

std::size_t rank_and_kernel(Matrix& matrix, std::vector<int>& kernel) {
  std::size_t rank = 0;
  std::size_t next_column = 0;
  std::vector<std::size_t> pivot_columns;
  pivot_columns.reserve(matrix.columns);

  while (next_column < matrix.columns && rank < matrix.rows) {
    const std::size_t panel_start_rank = rank;
    std::vector<std::size_t> panel_columns;

    while (next_column < matrix.columns &&
           panel_columns.size() < kPanel && rank < matrix.rows) {
      std::size_t source = rank;
      bool found = false;
      while (source < matrix.rows) {
        for (std::size_t local = 0; local < panel_columns.size(); ++local) {
          const int entry = digit(matrix.one(source), matrix.two(source),
                                  panel_columns[local]);
          if (entry == 1) {
            add_negative_row(matrix.one(source), matrix.two(source),
                             matrix.one(panel_start_rank + local),
                             matrix.two(panel_start_rank + local),
                             panel_columns[local] >> 6, matrix.words);
          } else if (entry == 2) {
            add_rows(matrix.one(source), matrix.two(source),
                     matrix.one(panel_start_rank + local),
                     matrix.two(panel_start_rank + local),
                     panel_columns[local] >> 6, matrix.words);
          }
        }
        if (digit(matrix.one(source), matrix.two(source), next_column)) {
          found = true;
          break;
        }
        ++source;
      }
      if (!found) {
        ++next_column;
        continue;
      }

      swap_rows(matrix, rank, source);
      normalize_row(matrix, rank, next_column);
      for (std::size_t local = 0; local < panel_columns.size(); ++local) {
        const std::size_t previous_row = panel_start_rank + local;
        const int entry = digit(matrix.one(previous_row),
                                matrix.two(previous_row), next_column);
        if (entry == 1) {
          add_negative_row(matrix.one(previous_row), matrix.two(previous_row),
                           matrix.one(rank), matrix.two(rank),
                           next_column >> 6, matrix.words);
        } else if (entry == 2) {
          add_rows(matrix.one(previous_row), matrix.two(previous_row),
                   matrix.one(rank), matrix.two(rank), next_column >> 6,
                   matrix.words);
        }
      }
      panel_columns.push_back(next_column);
      pivot_columns.push_back(next_column);
      ++rank;
      ++next_column;
    }

    const int panel_size = static_cast<int>(panel_columns.size());
    if (panel_size == 0) continue;
    const std::size_t combinations = power_three(panel_size);
    const std::size_t first_word = panel_columns.front() >> 6;
    const std::size_t active_words = matrix.words - first_word;
    std::vector<std::uint64_t> table(combinations * 2 * active_words, 0);
    auto table_one = [&](std::size_t index) {
      return table.data() + index * 2 * active_words;
    };
    auto table_two = [&](std::size_t index) {
      return table_one(index) + active_words;
    };

    for (std::size_t index = 1; index < combinations; ++index) {
      std::size_t quotient = index;
      int local = 0;
      while (quotient % 3 == 0) {
        quotient /= 3;
        ++local;
      }
      const int coefficient = quotient % 3;
      const std::size_t place = power_three(local);
      const std::size_t previous = index - coefficient * place;
      std::copy(table_one(previous), table_one(previous) + active_words,
                table_one(index));
      std::copy(table_two(previous), table_two(previous) + active_words,
                table_two(index));
      const std::size_t pivot_row = panel_start_rank + local;
      if (coefficient == 1) {
        add_negative_row(table_one(index), table_two(index),
                         matrix.one(pivot_row) + first_word,
                         matrix.two(pivot_row) + first_word, 0,
                         active_words);
      } else {
        add_rows(table_one(index), table_two(index),
                 matrix.one(pivot_row) + first_word,
                 matrix.two(pivot_row) + first_word, 0, active_words);
      }
    }

    for (std::size_t row = rank; row < matrix.rows; ++row) {
      std::size_t index = 0;
      std::size_t place = 1;
      for (std::size_t local = 0; local < panel_columns.size(); ++local) {
        index += place * digit(matrix.one(row), matrix.two(row),
                               panel_columns[local]);
        place *= 3;
      }
      if (index) {
        add_rows(matrix.one(row) + first_word,
                 matrix.two(row) + first_word, table_one(index),
                 table_two(index), 0, active_words);
      }
    }

    if (rank % 512 < static_cast<std::size_t>(panel_size)) {
      std::cerr << "rank=" << rank << " column=" << next_column << '\n';
    }
  }

  kernel.assign(matrix.columns, 0);
  if (rank < matrix.columns) {
    std::vector<bool> is_pivot(matrix.columns, false);
    for (std::size_t column : pivot_columns) is_pivot[column] = true;
    std::size_t free_column = 0;
    while (free_column < matrix.columns && is_pivot[free_column]) {
      ++free_column;
    }
    if (free_column < matrix.columns) kernel[free_column] = 1;

    for (std::size_t reverse = rank; reverse-- > 0;) {
      const std::size_t pivot = pivot_columns[reverse];
      int sum = 0;
      for (std::size_t column = pivot + 1; column < matrix.columns; ++column) {
        if (kernel[column]) {
          sum += digit(matrix.one(reverse), matrix.two(reverse), column) *
                 kernel[column];
        }
      }
      kernel[pivot] = (3 - (sum % 3)) % 3;
    }
  }
  return rank;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "usage: gf3_m3ri_rank ROWS COLUMNS INPUT KERNEL_OUTPUT\n";
    return 2;
  }
  Matrix matrix;
  matrix.rows = std::stoull(argv[1]);
  matrix.columns = std::stoull(argv[2]);
  matrix.words = (matrix.columns + 63) / 64;
  matrix.storage.resize(matrix.rows * 2 * matrix.words);

  std::ifstream input(argv[3], std::ios::binary);
  if (!input) throw std::runtime_error("cannot open input matrix");
  input.read(reinterpret_cast<char*>(matrix.storage.data()),
             static_cast<std::streamsize>(matrix.storage.size() *
                                          sizeof(std::uint64_t)));
  if (!input) throw std::runtime_error("short input matrix");

  std::vector<int> kernel;
  const std::size_t rank = rank_and_kernel(matrix, kernel);
  std::cout << "rows=" << matrix.rows << " columns=" << matrix.columns
            << " rank=" << rank
            << " nullity=" << matrix.columns - rank << '\n';

  std::ofstream output(argv[4]);
  if (!output) throw std::runtime_error("cannot open kernel output");
  for (std::size_t index = 0; index < kernel.size(); ++index) {
    if (kernel[index]) output << index << ' ' << kernel[index] << '\n';
  }
  return 0;
}
