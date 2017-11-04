import os
import random
import numpy as np


def read_episode_files(dump_files):
    game_dumps = []
    for filepath in dump_files:
        state_dumps = []
        with open(filepath, 'rb+') as f:
            try:
                while True:
                    state_dumps.append(np.load(f))
            except OSError:  # end of file
                pass
        game_dumps.append(state_dumps)
    return game_dumps

def find_all_filepaths(dir, shuffle=True):
    subdirs = [subdir
               for subdir in os.listdir(dir)
               if os.path.isdir(os.path.join(dir, subdir))]

    dump_files = [os.path.join(dir, subdir, filename)
                  for subdir in subdirs
                  for filename in os.listdir(os.path.join(dir, subdir))]
    if shuffle:
        random.shuffle(dump_files)
    return dump_files
