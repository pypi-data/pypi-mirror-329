-- Copyright 2024 Stanford University
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

import "regent"

-- This tests the compiler's ability to reuse the same projection
-- functor multiple times.

local c = regentlib.c

terra e(x : int) : int
  return 3
end

task f1(r : region(ispace(int1d), int), i : int1d)
where reads(r) do
  for x in r do
    regentlib.assert(x == (i + 1) % 5, "test failed")
  end
end

task g1(r : region(ispace(int1d), int), i : int1d)
where reads writes(r) do
  for x in r do
    regentlib.assert(x == (i + 1) % 5, "test failed")
  end
end

task h1(r : region(ispace(int1d), int), i : int1d) : int
where reduces+(r) do
  for x in r do
    regentlib.assert(x == (i + 1) % 5, "test failed")
  end
  return 5
end

task f2(r : region(ispace(int2d), int), i : int1d)
where reads(r) do
  for x in r do
    regentlib.assert(int1d(x.x) == (i + 1) % 5, "test failed")
  end
end

task g2(r : region(ispace(int2d), int), i : int1d)
where reads writes(r) do
  for x in r do
    regentlib.assert(int1d(x.x) == (i + 1) % 5, "test failed")
  end
end

task h2(r : region(ispace(int2d), int), i : int1d) : int
where reduces+(r) do
  for x in r do
    regentlib.assert(int1d(x.x) == (i + 1) % 5, "test failed")
  end
  return 5
end

task main()
  var n = 5
  var r = region(ispace(int1d, n), int)
  var s = region(ispace(int2d, {n, 1}), int)
  fill(r, 1)
  fill(s, 1)

  var cs = ispace(int1d, n)
  var r_part = partition(equal, r, cs)
  var s_part = partition(equal, s, cs)

  var x = 0

  -- #######################################################
  -- ### case 1. no capture
  __demand(__index_launch)
  for i in cs do
    f1(r_part[(i + 1) % 5], i)
  end
  __demand(__index_launch)
  for i in cs do
    g1(r_part[(i + 1) % 5], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    x += h1(r_part[(i + 1) % 5], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- a different partition will also reuse the same projection functor
  __demand(__index_launch)
  for i in cs do
    f2(s_part[(i + 1) % 5], i)
  end
  __demand(__index_launch)
  for i in cs do
    g2(s_part[(i + 1) % 5], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    x += h2(s_part[(i + 1) % 5], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- #######################################################
  -- ### case 2. capture one variable
  __demand(__index_launch)
  for i in cs do
    f1(r_part[(i + 1) % n], i)
  end
  __demand(__index_launch)
  for i in cs do
    g1(r_part[(i + 1) % n], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    x += h1(r_part[(i + 1) % n], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- a different partition will also reuse the same projection functor
  __demand(__index_launch)
  for i in cs do
    f2(s_part[(i + 1) % n], i)
  end
  __demand(__index_launch)
  for i in cs do
    g2(s_part[(i + 1) % n], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    x += h2(s_part[(i + 1) % n], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- #######################################################
  -- ### case 3. capture two variables
  var k = 1
  __demand(__index_launch)
  for i in cs do
    f1(r_part[(i + k) % n], i)
  end
  __demand(__index_launch)
  for i in cs do
    g1(r_part[(i + k) % n], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    x += h1(r_part[(i + k) % n], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- a different partition will also reuse the same projection functor
  __demand(__index_launch)
  for i in cs do
    f2(s_part[(i + k) % n], i)
  end
  __demand(__index_launch)
  for i in cs do
    g2(s_part[(i + k) % n], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    x += h2(s_part[(i + k) % n], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- #######################################################
  -- ### case 4. local variable and no captured variables
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    f1(r_part[y % 5], i)
  end
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    g1(r_part[y % 5], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    x += h1(r_part[y % 5], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- a different partition will also reuse the same projection functor
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    f2(s_part[y % 5], i)
  end
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    g2(s_part[y % 5], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    x += h2(s_part[y % 5], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- #######################################################
  -- ### case 5. local variable and one captured variable
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    f1(r_part[y % n], i)
  end
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    g1(r_part[y % n], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    x += h1(r_part[y % n], i)
  end
  regentlib.assert(x == 25, "test failed")

  -- a different partition will also reuse the same projection functor
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    f2(s_part[y % n], i)
  end
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    g2(s_part[y % n], i)
  end
  x = 0
  __demand(__index_launch)
  for i in cs do
    var y = i + 1
    x += h2(s_part[y % n], i)
  end
  regentlib.assert(x == 25, "test failed")
end
regentlib.start(main)
print(regentlib.count_projection_functors())
assert(regentlib.count_projection_functors() == 5)
