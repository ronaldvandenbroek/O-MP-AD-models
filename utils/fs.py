# Copyright 2018 Timo Nolle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================
from datetime import datetime
from enum import Enum
import os.path
from pathlib import Path

import random
import shutil
import numpy as np
import matplotlib.pyplot as plt
import json

from utils.enums import Perspective
from utils.enums import EncodingCategorical

# Base
ROOT_DIR = Path(__file__).parent.parent

# Output
EVENTLOG_DIR = os.path.join(ROOT_DIR,'eventlogs')  # For generated event logs
RESULTS_DIR = os.path.join(ROOT_DIR,'results')  # For the model scores
RESULTS_RAW_DIR = os.path.join(ROOT_DIR,'results','raw') # For the model raw error scores

# Cache
EVENTLOG_CACHE_DIR = os.path.join(ROOT_DIR,'eventlogs', 'cache')  # For caching datasets so the event log does not always have to be loaded

class FSSave():
    def __init__(self, start_time:datetime, run_name, model_name, categorical_encoding, numerical_encoding) -> None:
        categorical_encoding = EncodingCategorical.items_short()[categorical_encoding]

        self.perspective = 'none'
        self.bucket_size = None
        self.model_name = model_name
        start_time_str = str(start_time.strftime('%y-%m-%d-%H-%M'))
        
        self.run_path = f'{start_time_str}_{model_name}_{str(categorical_encoding)}_{get_random_id()}'
        print(self.run_path)

        self.parent = os.path.join(RESULTS_RAW_DIR, run_name)
        self.path = os.path.join(self.parent, self.run_path)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def set_bucket_size(self, bucket_size):
        self.bucket_size = str(bucket_size)

    def set_perspective(self, perspective):
        if isinstance(perspective, str) and not isinstance(perspective, int):
            self.perspective = perspective
        else:
            perspective_name = Perspective.values()[perspective]
            self.perspective = perspective_name

    def _save(self, file_name, data):
        np.savez_compressed(file=os.path.join(self.path, file_name), data=data)

    def save_config(self, config):
        serializable_config = {
            key: (value.value if isinstance(value, Enum) else value) for key, value in config.items()
        }
        file_name = self._generate_file_name(['config.json'])
        with open(os.path.join(self.path, file_name), "w") as f:
            json.dump(serializable_config, f, default=convert_to_serializable, indent=4)

    def save_raw_errors(self, errors):
        file_name = self._generate_file_name(['errors', self.model_name, self.bucket_size])
        self._save(file_name, errors)

    def save_raw_losses(self, losses):
        file_name = self._generate_file_name(['losses', self.model_name, self.bucket_size])
        self._save(file_name, losses)

    def save_raw_labels(self, level, labels):
        file_name = self._generate_file_name(['labels', self.model_name, level, self.bucket_size])
        self._save(file_name, labels)

    def save_raw_results(self, level, results):
        file_name = self._generate_file_name(['result', self.model_name, level, self.perspective, self.bucket_size])
        self._save(file_name, results)

    def save_embedding_space(self, encoder_name, pretrain_percentage, words, word_vectors):
        file_name = self._generate_file_name(['embedding', encoder_name, pretrain_percentage])

        plt.scatter(word_vectors[:, 0], word_vectors[:, 1], color='red')

        # Annotate the points with the corresponding words
        for i, word in enumerate(words):
            if int(word) < 10:
                plt.annotate(word, xy=(word_vectors[i, 0], word_vectors[i, 1]), fontsize=12, color='green')

        # Set the title and labels
        plt.title(f'{encoder_name} Word Embeddings With {pretrain_percentage * 100}% Pretraining')
        # plt.xlabel('Dimension 1')
        # plt.ylabel('Dimension 2')
        plt.grid()
        # plt.legend()
        print(f'Saving Embedding plot {file_name}')
        plt.savefig(os.path.join(self.path, file_name + ".png"), format='png', dpi=300)
    
    def _generate_file_name(self, name_parts):
        name = None
        for item in name_parts:
            if item is not None:
                if name is None:
                    name = item
                else:
                    name = f'{name}_{item}'
        return name

    def zip_results(self):
        # Compress the current folder as .zip
        zip_output_path = os.path.join(self.parent, f"{self.run_path}.zip")
        shutil.make_archive(zip_output_path.replace('.zip', ''), 'zip', self.path)

        # Remove the original folder to save space
        shutil.rmtree(self.path)

def split_eventlog_name(name):
    try:
        s = name.split('-')
        model = s[0]
        p = float(s[1])
        id = int(s[2])
    except Exception:
        model = None
        p = None
        id = None
    return model, p, id

def convert_to_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert numpy array to list
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def get_random_id():
    return str(random.randint(10000, 99999))

class File(object):
    ext = None

    def __init__(self, path):
        if not isinstance(path, Path):
            path = Path(path)

        self.path = path
        self.file = self.path.name
        self.name = self.path.stem
        self.str_path = str(path)

    def remove(self):
        import os
        if self.path.exists():
            os.remove(self.path)


class EventLogFile(File):
    def __init__(self, path):
        if not isinstance(path, Path):
            path = Path(path)
        if '.json' not in path.suffixes:
            path = Path(str(path) + '.json.gz')
        if not path.is_absolute():
            path = Path(os.path.join(EVENTLOG_DIR, path))

        super(EventLogFile, self).__init__(path)

        if len(self.path.suffixes) > 1:
            self.name = Path(self.path.stem).stem

        self.model, self.p, self.id = split_eventlog_name(self.name)

    @property
    def cache_file(self):
        if not os.path.exists(EVENTLOG_CACHE_DIR):
            os.makedirs(EVENTLOG_CACHE_DIR)
        return Path(os.path.join(EVENTLOG_CACHE_DIR , (self.name + '.pkl.gz')))

