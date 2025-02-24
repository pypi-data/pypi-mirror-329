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

-- runs-with:
-- [
--  [ "-dm:memoize" ],
--  [ "-dm:memoize", "-lg:no_fence_elision" ],
--  [ "-dm:memoize", "-lg:no_trace_optimization" ]
-- ]

import "regent"

local launcher = require("std/launcher")
local cmapper = launcher.build_library("optimize_tracing_invalidate1")

fspace fs
{
  input : int;
  output : int;
}

task init(r : region(ispace(int1d), fs))
where reads writes(r)
do
  for e in r do
    e.input = 0
    e.output = 0
  end
end

task inc(r : region(ispace(int1d), fs))
where reads(r.input), writes(r.output)
do
  for e in r do
    e.output = e.input + 1
  end
end

task step(r : region(ispace(int1d), fs))
where writes(r.input), reads(r.output)
do
  for e in r do
    e.input = e.output
  end
end

task check(r : region(ispace(int1d), fs), n : int)
where reads(r)
do
  for e in r do
    regentlib.assert(e.input % 3 == n, "test, failed")
  end
end

task main()
  var n = 2
  var r = region(ispace(int1d, n), fs)
  var cs = ispace(int1d, n)
  var p = partition(equal, r, cs)
  var q = partition(equal, r, cs)

  for color in cs do init(p[color]) end
  for k = 0, 3 do
    __demand(__trace)
    for i = 0, 2 do
      for color in cs do inc(p[color]) end
      for color in cs do step(p[color]) end
    end
    for color in cs do check(q[color], 2 * (k + 1) % 3) end
  end
  for color in cs do init(p[color]) end
  for k = 0, 3 do
    __demand(__trace)
    for i = 0, 2 do
      for color in cs do inc(p[color]) end
      for color in cs do step(p[color]) end
      for color in cs do inc(q[color]) end
      for color in cs do step(q[color]) end
    end
    for color in cs do check(q[color], 4 * (k + 1) % 3) end
  end
  for color in cs do init(p[color]) end
  for k = 0, 2 do
    __demand(__trace)
    do
      for color in cs do inc(p[color]) end
      for color in cs do step(p[color]) end
    end
    __demand(__trace)
    do
      for color in cs do inc(q[color]) end
      for color in cs do step(q[color]) end
    end
  end
  for color in cs do check(p[color], 1) end
end
launcher.launch(main, "optimize_tracing_invalidate1", cmapper.register_mappers, {"-loptimize_tracing_invalidate1"})
