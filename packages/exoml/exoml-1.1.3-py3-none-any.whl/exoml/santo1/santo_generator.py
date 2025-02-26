import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.utils import shuffle
from tensorflow.keras.utils import Sequence

class SantoGenerator(Sequence):
    def __init__(self, lcs_dir, target_files, input_size=20000, step_size=1, batch_size=500, shuffle=True,
                 zero_epsilon=1e-7, max_time_encoding=200, plot=False):
        self.lcs_dir = lcs_dir
        self.target_files = target_files
        self.input_size = input_size
        self.step_size = step_size
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.zero_epsilon = zero_epsilon
        self.steps_count, self.generator_info_df = self._count_inputs()
        self.max_time_encoding = max_time_encoding
        self.plot = plot

    def _count_inputs(self):
        batch_index = 0
        chunks_index = 0
        generator_info_df: pd.DataFrame = pd.DataFrame(columns=['filename', 'file_start_index', 'file_end_index', 'batch_index'])
        for target_file in self.target_files:
            filename = f'{self.lcs_dir}/{target_file}'
            flux = np.loadtxt(filename, delimiter=',')
            file_batch_indexes = np.arange(0, flux.shape[1], self.input_size // 2)
            stop = False
            for file_start_index in file_batch_indexes:
                if flux.shape[1] - file_start_index <= self.input_size:
                    file_start_index = flux.shape[1] - self.input_size - 1
                    if file_start_index < 0:
                        file_start_index = 0
                    stop = True
                file_end_index: int = file_start_index + self.input_size
                if file_end_index >= flux.shape[1]:
                    file_end_index = flux.shape[1] - 1
                    file_start_index = file_end_index - self.input_size
                if file_start_index < 0:
                    logging.error(
                        f"{filename} file_start_index should be greater than zero. Curve length is {file_end_index} - {file_start_index}")
                    continue
                if np.sum(flux[1, file_start_index:file_end_index] < 1e-7) / flux[1, file_start_index:file_end_index].shape[0] > 0.25:
                    continue

                # if np.all(np.abs(flux[2, file_start_index:file_end_index] - 1) < 1e-7):
                #     continue
                generator_info_df = pd.concat([generator_info_df, pd.DataFrame.from_dict(
                                    {'filename': [target_file], 'file_start_index': [file_start_index],
                                     'file_end_index': [file_end_index],
                                     'batch_index': [batch_index]})], ignore_index=True)
                chunks_index = chunks_index + 1
                if chunks_index % self.batch_size == 0:
                    batch_index = batch_index + 1
                if stop:
                    break
        generator_info_df.sort_values(['batch_index', 'filename', 'file_start_index'], ascending=True, inplace=True)
        return batch_index - 1, generator_info_df

    def __len__(self):
        return self.steps_count

    def create_tf_dataset(self):
        # Generator function to yield data in batches
        def dataset_generator():
            for batch_index in range(self.steps_count):
                batch_df = self.generator_info_df.loc[self.generator_info_df['batch_index'] == batch_index]
                train_data = np.zeros((self.batch_size, 3, self.input_size), dtype=np.float32)
                item_index = 0
                for row_index, batch_row in batch_df.iterrows():
                    filename = batch_row['filename']
                    flux = np.loadtxt(f'{self.lcs_dir}/{filename}', delimiter=',', dtype=np.float32)
                    file_start_index = batch_row['file_start_index']
                    file_end_index = batch_row['file_end_index']
                    train_data[item_index, 0] = flux[4, file_start_index:file_end_index]
                    train_data[item_index, 1] = flux[1, file_start_index:file_end_index] / 2
                    train_data[item_index, 2] = flux[3, file_start_index:file_end_index]
                    #print(np.any(flux[3, file_start_index:file_end_index] > 0.5))
                    yield (flux[[4, 1], file_start_index:file_end_index].swapaxes(0, 1),
                           flux[3, file_start_index:file_end_index])
                    item_index += 1
                train_data_swapped = train_data.swapaxes(1, 2)
                features = train_data_swapped[:, :, 0:2]
                labels = train_data_swapped[:, :, 2].reshape((self.batch_size, self.input_size))
                #yield features, labels
        dataset = tf.data.Dataset.from_generator(
            dataset_generator,
            output_signature=(
                tf.TensorSpec(shape=(self.input_size, 2), dtype=tf.float32),
                tf.TensorSpec(shape=(self.input_size), dtype=tf.float32)
            )
        )
        dataset = dataset.batch(self.batch_size).prefetch(tf.data.AUTOTUNE)
        return dataset

    def __getitem__(self, batch_index):
        batch_df = self.generator_info_df.loc[self.generator_info_df['batch_index'] == batch_index]
        train_data = np.zeros((self.batch_size, 3, self.input_size), dtype=np.float32)
        item_index = 0
        if len(batch_df) != self.batch_size:
            raise ValueError("More items than batch size")
        for row_index, batch_row in batch_df.iterrows():
            filename: str = batch_row['filename']
            flux = np.loadtxt(f'{self.lcs_dir}/{filename}', delimiter=',', dtype=np.float32)
            file_start_index: int = batch_row['file_start_index']
            file_end_index: int = batch_row['file_end_index']
            train_data[item_index, 0] = flux[4, file_start_index:file_end_index]
            train_data[item_index, 1] = flux[1, file_start_index:file_end_index] / 2
            train_data[item_index, 2] = flux[3, file_start_index:file_end_index]
            # self.assert_tags_value(filename, train_data[item_index, :, 2])
            # self.assert_in_range(filename, train_data[item_index, :])
            if self.plot:
                fig, axs = plt.subplots(2, 1, figsize=(15, 10))
                axs[0].scatter(flux[0, file_start_index:file_end_index], train_data[item_index, 1])
                axs[1].plot(flux[0, file_start_index:file_end_index], train_data[item_index, 2])
                plt.show()
            item_index = item_index + 1
        # np.all(train_data[item_index, :, 2] != train_data[item_index, :, 2].astype(int)), "train_tags contains integer values!"
        # if np.any(np.abs(train_data[item_index, :, 2]) - 1 < 1e-6):
        #     print("Train tags greater than one")
        train_data_swapped = train_data.swapaxes(1, 2)
        return train_data_swapped[:, :, 0:2], train_data_swapped[:, :, 2].reshape((self.batch_size, self.input_size))

    def assert_in_range(self, object_id, array, values_range=(0, 1)):
        if np.isnan(array).any():
            raise ValueError("Target " + str(object_id) + " contains NaN values")
        elif np.max(array) > values_range[1]:
            raise ValueError("Target " + str(object_id) + " contains values > 1")
        elif np.min(array) < values_range[0]:
            raise ValueError("Target " + str(object_id) + " contains values < 0")

    def assert_tags_value(self, object_id, array, values_range=(0, 1)):
        if np.any((array > values_range[0]) & (array < values_range[1])):
            raise ValueError("Target " + str(object_id) + " contains invalid values")

    def on_epoch_end(self):
        if self.shuffle:
            self.generator_info_df = shuffle(self.generator_info_df)

    def class_weights(self):
        return {0: 1, 1: 1}

    def steps_per_epoch(self):
        return self.steps_count

#
# class SantoGenerator2:
#     def __init__(self, lcs_dir, target_files, input_size=20000, batch_size=64, shuffle=True):
#         self.lcs_dir = lcs_dir
#         self.target_files = target_files
#         self.input_size = input_size
#         self.batch_size = batch_size
#         self.shuffle = shuffle
#         self.file_indices = self._prepare_indices()
#
#     def _prepare_indices(self):
#         indices = []
#         for file in self.target_files:
#             flux = np.loadtxt(f'{self.lcs_dir}/{file}', delimiter=',', dtype=np.float32)
#             file_length = flux.shape[1]
#             chunks = np.arange(0, file_length, self.input_size // 2)
#             for start_index in chunks:
#                 end_index = min(start_index + self.input_size, file_length)
#                 if end_index - start_index == self.input_size:
#                     indices.append((file, start_index, end_index))
#         if self.shuffle:
#             np.random.shuffle(indices)
#         return indices
#
#     def _process_file(self, file, start_index, end_index):
#         flux = np.loadtxt(f'{self.lcs_dir}/{file}', delimiter=',', dtype=np.float32)
#         time_data = np.sin((2 * np.pi / 200) * flux[0, start_index:end_index])
#         time_data = np.clip(time_data, 1e-7, 1 - 1e-7)
#         flux_data = flux[1, start_index:end_index] / 2
#         tags_data = flux[2, start_index:end_index]
#         tags_data = np.where((tags_data < 1e-5) | (np.abs(tags_data - 1) < 1e-7), 0.0, 1.0).astype(np.float32)
#         train_data = np.stack([time_data, flux_data], axis=-1)
#         return train_data, tags_data
#
#     def generator(self):
#         """Python generator function that yields batches."""
#         while True:  # Loop forever so Keras can run multiple epochs
#             batch_data = []
#             batch_labels = []
#             for file, start_index, end_index in self.file_indices:
#                 data, labels = self._process_file(file, start_index, end_index)
#                 batch_data.append(data)
#                 batch_labels.append(labels)
#                 if len(batch_data) == self.batch_size:
#                     yield np.array(batch_data, dtype=np.float32), np.array(batch_labels, dtype=np.float32)
#                     batch_data = []
#                     batch_labels = []