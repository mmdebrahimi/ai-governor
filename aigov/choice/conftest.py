import os
import sys

# Put the project root on sys.path so `import models.resource_sim` resolves
# when pytest is invoked from the repo root.
sys.path.insert(0, os.path.dirname(__file__))
