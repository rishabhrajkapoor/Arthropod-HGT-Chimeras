import pickle
import pandas as pd
import multiprocessing as mp
import numpy as np
import pickle
import matplotlib.pyplot as plt
from Bio import SeqIO
import os
import subprocess
import ast

with open('inter_scan_blast.pickle', 'rb') as handle:
    b = pickle.load(handle)