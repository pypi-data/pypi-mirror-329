#pragma once
//==============================================================================
// C headers
#include <assert.h>
#include <cmath>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
//==============================================================================
// C++ headers
#include <algorithm>
#include <array>
#include <chrono>
#include <memory>
#include <numeric>
#include <optional>
#include <set>
#include <unordered_map>
#include <vector>
//==============================================================================
namespace std
{
template <> struct hash<std::set<int>>
{
  size_t operator()(const std::set<int>& s) const
  {
    size_t hash = 0;
    for (int x : s)
    {
      hash ^= std::hash<int>{}(x) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
    }
    return hash;
  }
};
} // namespace std
//==============================================================================