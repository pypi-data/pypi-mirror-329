import os

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.utils import shuffle
from tensorflow.keras.utils import Sequence

class SantoGenerator(Sequence):
    def __init__(self, lcs_dir, target_files, input_size=500, step_size=1, batch_size=500, shuffle=True, zero_epsilon=1e-7):
        self.lcs_dir = lcs_dir
        self.target_files = target_files
        self.input_size = input_size
        self.step_size = step_size
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.zero_epsilon = zero_epsilon
        self.steps_count, self.generator_info_df = self._count_inputs()

    def _count_inputs(self):
        batch_index = 0
        generator_info_df: pd.DataFrame = pd.DataFrame(columns=['filename', 'file_index', 'batch_index'])
        for target_file in self.target_files:
            flux = np.loadtxt(f'{self.lcs_dir}/{target_file}', delimiter=',')
            file_batch_indexes = np.arange(0, flux.shape[1], self.batch_size)
            for file_index in file_batch_indexes:
                generator_info_df = pd.concat([generator_info_df, pd.DataFrame.from_dict(
                                    {'filename': [target_file], 'file_index': [file_index],
                                     'batch_index': [batch_index]})], ignore_index=True)
                batch_index = batch_index + 1
        return batch_index - 1, generator_info_df

    def __len__(self):
        return self.generator_info_df['batch_index'].max()

    def __getitem__(self, index):
        filename: str = self.generator_info_df.iloc[index]['filename']
        file_index: int = self.generator_info_df.loc[index]['file_index']
        flux = np.loadtxt(f'{self.lcs_dir}/{filename}', delimiter=',')
        max_index = np.min([flux.shape[1] - self.input_size, file_index + self.batch_size])
        train_fluxes = np.full((self.batch_size, self.input_size), 0.5)
        train_tags = np.full((self.batch_size, 1), float(0))
        for iteration_index in np.arange(file_index, max_index):
            flux_data = flux[0][iteration_index:iteration_index + self.input_size] / 2
            train_fluxes[iteration_index - file_index] = flux_data
            tags_data_index = iteration_index + self.input_size // 2 - 1
            tags_data = np.array(flux[1][tags_data_index]).flatten()
            oot_mask = np.abs(tags_data - 1) < 1e-6
            tags_data[oot_mask] = float(0)
            tags_data[~oot_mask] = float(1)
            train_tags[iteration_index - file_index] = tags_data
        self.assert_in_range(filename, train_fluxes)
        np.all(train_tags != train_tags.astype(int)), "train_tags contains integer values!"
        return np.reshape(train_fluxes, (self.batch_size, 500, 1)), train_tags

    def assert_in_range(self, object_id, array, values_range=(0, 1)):
        if np.isnan(array).any():
            raise ValueError("Target " + str(object_id) + " contains NaN values")
        elif np.max(array) >= values_range[1]:
            raise ValueError("Target " + str(object_id) + " contains values > 1")
        elif np.min(array) <= values_range[0]:
            raise ValueError("Target " + str(object_id) + " contains values < 0")
        elif np.all(array == values_range[0]):
            raise ValueError("Target " + str(object_id) + " contains all values == 0")

    def on_epoch_end(self):
        if self.shuffle:
            self.generator_info_df = shuffle(self.generator_info_df)

    def class_weights(self):
        return {0: 1, 1: 1}

    def steps_per_epoch(self):
        return self.steps_count