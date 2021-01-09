# **Bugs:**

**Failing Tests:**
* /home/vagrant/4500/repo/6/annetta/Tests/5-in.json (local: Tests/6-in.json)
    * Output: [[2, 1], [1, 0]] Expected: [[2, 0], [1, 0]]
* /home/vagrant/4500/repo/6/oakwood/Tests/4-in.json (local: Tests/7-in.json)
    * Output: [[4, 1], [2, 0]] Expected: [[4, 0], [2, 0]]
* /home/vagrant/4500/repo/6/westmountain/Tests/4-in.json (local: Tests/8-in.json)
    * Output: [[1, 0], [2, 1]] Expected: [[0, 1], [2, 1]] 

**Issue Description:** In a tie-breaking scenario within strategy.py, the strategy was not 
choosing the penguin with the lowest row number for the place and the lowest column number within the row while 
instead choosing another penguin that can move to that valid spot.

https://github.ccs.neu.edu/CS4500-F20/dish/commit/5703d1779b5f0156122c2467dbea18e11c9c6f24
