import os

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.utils import shuffle
from tensorflow.keras.utils import Sequence

class SantoPredictGenerator(Sequence):
    def __init__(self, times, lcs, input_size=500, step_size=1, batch_size=500, zero_epsilon=1e-7):
        self.times = times
        self.lcs = lcs
        self.input_size = input_size
        self.step_size = step_size
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.zero_epsilon = zero_epsilon
        self.steps_count, self.generator_info_df = self._count_inputs()

    def _count_inputs(self):
        generator_info_df: pd.DataFrame = pd.DataFrame(columns=['filename', 'file_index', 'batch_index'])
        lcs_to_original_lcs: list[tuple[int, int, int, list[float]]] = []
        for curve_index, times in enumerate(self.times):
            diff = np.diff(times)
            jump_indices = np.where(abs(diff) > 12 / 24)[0]
            previous_jump_index = 0
            jump_index = len(self.lcs[curve_index])
            if len(jump_indices) == 0:
                lcs_to_original_lcs = lcs_to_original_lcs + [(curve_index, previous_jump_index, jump_index, self.lcs[curve_index])]
            else:
                for jump_index in jump_indices:
                    lcs_to_original_lcs = lcs_to_original_lcs + [(curve_index, previous_jump_index, jump_index, self.lcs[curve_index][previous_jump_index:jump_index + 1])]
                    previous_jump_index = jump_index + 1
                if jump_index < len(self.lcs[curve_index]) - 1:
                    jump_index = len(self.lcs[curve_index]) - 1
                    lcs_to_original_lcs = lcs_to_original_lcs + [(curve_index, previous_jump_index, jump_index, self.lcs[curve_index][previous_jump_index:jump_index + 1])]
        batch_index = 0
        for lc_to_original_lc in lcs_to_original_lcs:
            flux = lc_to_original_lc[3]
            file_batch_indexes = np.arange(0, len(flux), self.batch_size)
            for file_index in file_batch_indexes:
                generator_info_df = pd.concat([generator_info_df, pd.DataFrame.from_dict(
                                    {'curve_index': [lc_to_original_lc[0]], 'initial_jump_index': [lc_to_original_lc[1]],
                                     'end_jump_index': [lc_to_original_lc[2]], 'file_index': [file_index],
                                     'batch_index': [batch_index]})], ignore_index=True)
                batch_index = batch_index + 1
        return batch_index - 1 , generator_info_df

    def __len__(self):
        return len(self.generator_info_df['batch_index'])

    def __getitem__(self, index):
        curve_index: int = int(self.generator_info_df.iloc[index]['curve_index'])
        initial_jump_index: int = int(self.generator_info_df.iloc[index]['initial_jump_index'])
        end_jump_index: int = int(self.generator_info_df.iloc[index]['end_jump_index'])
        file_index: int = int(self.generator_info_df.iloc[index]['file_index'])
        flux = self.lcs[curve_index][initial_jump_index:end_jump_index + 1]
        max_index = np.min([len(flux) - self.input_size, file_index + self.batch_size])
        train_fluxes = np.full((self.batch_size,  self.input_size), self.zero_epsilon)
        train_tags = np.full((self.batch_size, 1), 0)
        for iteration_index in np.arange(file_index, max_index):
            flux_data = flux[iteration_index:iteration_index + self.input_size] / 2
            train_fluxes[iteration_index - file_index] = flux_data
        return train_fluxes, None

    def on_epoch_end(self):
        if self.shuffle:
            self.generator_info_df = shuffle(self.generator_info_df)

    def class_weights(self):
        return {0: 1, 1: 1}

    def steps_per_epoch(self):
        return self.steps_count