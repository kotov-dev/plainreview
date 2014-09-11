#!/usr/bin/python
import os
diff = os.popen("git diff origin master")
print diff.read()