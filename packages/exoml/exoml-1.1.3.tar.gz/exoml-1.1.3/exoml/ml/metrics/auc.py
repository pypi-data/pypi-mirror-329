import abc
import tensorflow as tf
import numpy as np
import tensorflow.keras.backend as K

from keras import backend
from keras.utils import metrics_utils
from keras.utils.generic_utils import to_list
from keras_core import Metric
from keras_core.src.utils import tf_utils
#from tf_keras.src.metrics import base_metric


#from tf_keras.src.metrics import base_metric
# from keras.src import backend
# from keras.src.utils import tf_utils
# from keras.metrics import Metric
# from keras.src.utils import metrics_utils
# from keras.src.utils.generic_utils import to_list
# from keras.src.metrics import base_metric
# from keras.src import backend

def inject_mesh(init_method):
    """Inject DTensor mesh information to an object.

    This is useful for keras object like `Metric` and `Optimizer` which need
    DTensor mesh to create the weights, but doesn't want to change the current
    public API interface.

    This is for temporary usage and eventually the mesh/layout information will
    be public arguments in the `__init__` method.

    Sample usage:
    ```python
    class Accuracy(tf.keras.metrics.Metric):

      @inject_mesh
      def __init__(self, name='accuracy', dtype=None):
         super().__init__(**kwargs)

      acc = Accuracy(mesh=mesh)
      assert acc._mesh == mesh
    ```

    Args:
      init_method: the `__init__` method of the Keras class to annotate.

    Returns:
      the annotated __init__ method.
    """

    def _wrap_function(instance, *args, **kwargs):
        mesh = kwargs.pop("mesh", None)
        # Note that the injection of _mesh need to happen before the invocation
        # of __init__, since the class might need the mesh to create weights in
        # the __init__.
        if mesh is not None:
            instance._mesh = mesh
        init_method(instance, *args, **kwargs)

    return tf.__internal__.decorator.make_decorator(
        target=init_method, decorator_func=_wrap_function
    )


class SensitivitySpecificityBase(Metric, metaclass=abc.ABCMeta):
    """Abstract base class for computing sensitivity and specificity.

    For additional information about specificity and sensitivity, see
    [the following](https://en.wikipedia.org/wiki/Sensitivity_and_specificity).
    """

    def __init__(
        self, value, num_thresholds=200, class_id=None, name=None, dtype=None
    ):
        super().__init__(name=name, dtype=dtype)
        if num_thresholds <= 0:
            raise ValueError(
                "Argument `num_thresholds` must be an integer > 0. "
                f"Received: num_thresholds={num_thresholds}"
            )
        self.value = value
        self.class_id = class_id
        self.true_positives = self.add_weight(
            name="true_positives", shape=(num_thresholds,), initializer="zeros"
        )
        self.true_negatives = self.add_weight(
            name="true_negatives", shape=(num_thresholds,), initializer="zeros"
        )
        self.false_positives = self.add_weight(
            name="false_positives", shape=(num_thresholds,), initializer="zeros"
        )
        self.false_negatives = self.add_weight(
            name="false_negatives", shape=(num_thresholds,), initializer="zeros"
        )

        # Compute `num_thresholds` thresholds in [0, 1]
        if num_thresholds == 1:
            self.thresholds = [0.5]
            self._thresholds_distributed_evenly = False
        else:
            thresholds = [
                (i + 1) * 1.0 / (num_thresholds - 1)
                for i in range(num_thresholds - 2)
            ]
            self.thresholds = [0.0] + thresholds + [1.0]
            self._thresholds_distributed_evenly = True

    def update_state(self, y_true, y_pred, sample_weight=None):
        """Accumulates confusion matrix statistics.

        Args:
          y_true: The ground truth values.
          y_pred: The predicted values.
          sample_weight: Optional weighting of each example. Defaults to 1. Can
            be a `Tensor` whose rank is either 0, or the same rank as `y_true`,
            and must be broadcastable to `y_true`.

        Returns:
          Update op.
        """
        return metrics_utils.update_confusion_matrix_variables(
            {
                metrics_utils.ConfusionMatrix.TRUE_POSITIVES: self.true_positives,  # noqa: E501
                metrics_utils.ConfusionMatrix.TRUE_NEGATIVES: self.true_negatives,  # noqa: E501
                metrics_utils.ConfusionMatrix.FALSE_POSITIVES: self.false_positives,  # noqa: E501
                metrics_utils.ConfusionMatrix.FALSE_NEGATIVES: self.false_negatives,  # noqa: E501
            },
            y_true,
            y_pred,
            thresholds=self.thresholds,
            thresholds_distributed_evenly=self._thresholds_distributed_evenly,
            class_id=self.class_id,
            sample_weight=sample_weight,
        )

    def reset_state(self):
        num_thresholds = len(self.thresholds)
        confusion_matrix_variables = (
            self.true_positives,
            self.true_negatives,
            self.false_positives,
            self.false_negatives,
        )
        backend.batch_set_value(
            [
                (v, np.zeros((num_thresholds,)))
                for v in confusion_matrix_variables
            ]
        )

    def get_config(self):
        config = {"class_id": self.class_id}
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def _find_max_under_constraint(self, constrained, dependent, predicate):
        """Returns the maximum of dependent_statistic that satisfies the
        constraint.

        Args:
          constrained: Over these values the constraint
            is specified. A rank-1 tensor.
          dependent: From these values the maximum that satiesfies the
            constraint is selected. Values in this tensor and in
            `constrained` are linked by having the same threshold at each
            position, hence this tensor must have the same shape.
          predicate: A binary boolean functor to be applied to arguments
          `constrained` and `self.value`, e.g. `tf.greater`.

        Returns:
          maximal dependent value, if no value satiesfies the constraint 0.0.
        """
        feasible = tf.where(predicate(constrained, self.value))
        feasible_exists = tf.greater(tf.size(feasible), 0)
        max_dependent = tf.reduce_max(tf.gather(dependent, feasible))

        return tf.where(feasible_exists, max_dependent, 0.0)



class ThresholdAtPrecision(SensitivitySpecificityBase):
    """Computes best recall where precision is >= specified value.

    For a given score-label-distribution the required precision might not
    be achievable, in this case 0.0 is returned as recall.

    This metric creates four local variables, `true_positives`,
    `true_negatives`, `false_positives` and `false_negatives` that are used to
    compute the recall at the given precision. The threshold for the given
    precision value is computed and used to evaluate the corresponding recall.

    If `sample_weight` is `None`, weights default to 1.
    Use `sample_weight` of 0 to mask values.

    If `class_id` is specified, we calculate precision by considering only the
    entries in the batch for which `class_id` is above the threshold
    predictions, and computing the fraction of them for which `class_id` is
    indeed a correct label.

    Args:
      precision: A scalar value in range `[0, 1]`.
      num_thresholds: (Optional) Defaults to 200. The number of thresholds to
        use for matching the given precision.
      class_id: (Optional) Integer class ID for which we want binary metrics.
        This must be in the half-open interval `[0, num_classes)`, where
        `num_classes` is the last dimension of predictions.
      name: (Optional) string name of the metric instance.
      dtype: (Optional) data type of the metric result.

    Standalone usage:

    >>> m = tf.keras.metrics.RecallAtPrecision(0.8)
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9])
    >>> m.result().numpy()
    0.5

    >>> m.reset_state()
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9],
    ...                sample_weight=[1, 0, 0, 1])
    >>> m.result().numpy()
    1.0

    Usage with `compile()` API:

    ```python
    model.compile(
        optimizer='sgd',
        loss='mse',
        metrics=[tf.keras.metrics.RecallAtPrecision(precision=0.8)])
    ```
    """

    @inject_mesh
    def __init__(
        self,
        precision,
        num_thresholds=200,
        class_id=None,
        name=None,
        dtype=None,
    ):
        if precision < 0 or precision > 1:
            raise ValueError(
                "Argument `precision` must be in the range [0, 1]. "
                f"Received: precision={precision}"
            )
        self.precision = precision
        self.num_thresholds = num_thresholds
        super().__init__(
            value=precision,
            num_thresholds=num_thresholds,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )

    def result(self):
        precisions = tf.math.divide_no_nan(
            self.true_positives,
            tf.math.add(self.true_positives, self.false_positives),
        )
        recalls = tf.math.divide_no_nan(
            self.true_positives,
            tf.math.add(self.true_positives, self.false_negatives),
        )
        return self._find_max_threshold_under_constraint(
            precisions, recalls, tf.greater_equal
        )

    def _find_max_threshold_under_constraint(self, constrained, dependent, predicate):
        """Returns the maximum of dependent_statistic that satisfies the
        constraint.

        Args:
          constrained: Over these values the constraint
            is specified. A rank-1 tensor.
          dependent: From these values the maximum that satiesfies the
            constraint is selected. Values in this tensor and in
            `constrained` are linked by having the same threshold at each
            position, hence this tensor must have the same shape.
          predicate: A binary boolean functor to be applied to arguments
          `constrained` and `self.value`, e.g. `tf.greater`.

        Returns:
          maximal dependent value, if no value satiesfies the constraint 0.0.
        """
        variable_dtype = self.true_positives.dtype
        thresholds = tf.convert_to_tensor(self.thresholds, dtype=variable_dtype)
        feasible = tf.where(predicate(constrained, self.value))
        feasible_exists = tf.greater(tf.size(feasible), 0)
        try:
            return tf.where(feasible_exists, tf.gather(thresholds, tf.gather(feasible, [0])), 0.0)
        except Exception as e:
            print("Error " + str(e))
            return 0.0 

    def get_config(self):
        config = {
            "num_thresholds": self.num_thresholds,
            "precision": self.precision,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class ThresholdAtRecall(SensitivitySpecificityBase):
    """Computes best recall where precision is >= specified value.

    For a given score-label-distribution the required precision might not
    be achievable, in this case 0.0 is returned as recall.

    This metric creates four local variables, `true_positives`,
    `true_negatives`, `false_positives` and `false_negatives` that are used to
    compute the recall at the given precision. The threshold for the given
    precision value is computed and used to evaluate the corresponding recall.

    If `sample_weight` is `None`, weights default to 1.
    Use `sample_weight` of 0 to mask values.

    If `class_id` is specified, we calculate precision by considering only the
    entries in the batch for which `class_id` is above the threshold
    predictions, and computing the fraction of them for which `class_id` is
    indeed a correct label.

    Args:
      recall: A scalar value in range `[0, 1]`.
      num_thresholds: (Optional) Defaults to 200. The number of thresholds to
        use for matching the given precision.
      class_id: (Optional) Integer class ID for which we want binary metrics.
        This must be in the half-open interval `[0, num_classes)`, where
        `num_classes` is the last dimension of predictions.
      name: (Optional) string name of the metric instance.
      dtype: (Optional) data type of the metric result.

    Standalone usage:

    >>> m = tf.keras.metrics.RecallAtPrecision(0.8)
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9])
    >>> m.result().numpy()
    0.5

    >>> m.reset_state()
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9],
    ...                sample_weight=[1, 0, 0, 1])
    >>> m.result().numpy()
    1.0

    Usage with `compile()` API:

    ```python
    model.compile(
        optimizer='sgd',
        loss='mse',
        metrics=[tf.keras.metrics.RecallAtPrecision(precision=0.8)])
    ```
    """

    @inject_mesh
    def __init__(
        self,
        recall,
        num_thresholds=200,
        class_id=None,
        name=None,
        dtype=None,
    ):
        if recall < 0 or recall > 1:
            raise ValueError(
                "Argument `recall` must be in the range [0, 1]. "
                f"Received: recall={recall}"
            )
        self.recall = recall
        self.num_thresholds = num_thresholds
        super().__init__(
            value=recall,
            num_thresholds=num_thresholds,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )

    def result(self):
        precisions = tf.math.divide_no_nan(
            self.true_positives,
            tf.math.add(self.true_positives, self.false_positives),
        )
        recalls = tf.math.divide_no_nan(
            self.true_positives,
            tf.math.add(self.true_positives, self.false_negatives),
        )
        return self._find_max_threshold_under_constraint(
            recalls, precisions, tf.greater_equal
        )

    def _find_max_threshold_under_constraint(self, constrained, dependent, predicate):
        """Returns the maximum of dependent_statistic that satisfies the
        constraint.

        Args:
          constrained: Over these values the constraint
            is specified. A rank-1 tensor.
          dependent: From these values the maximum that satiesfies the
            constraint is selected. Values in this tensor and in
            `constrained` are linked by having the same threshold at each
            position, hence this tensor must have the same shape.
          predicate: A binary boolean functor to be applied to arguments
          `constrained` and `self.value`, e.g. `tf.greater`.

        Returns:
          maximal dependent value, if no value satiesfies the constraint 0.0.
        """
        variable_dtype = self.true_positives.dtype
        thresholds = tf.convert_to_tensor(self.thresholds, dtype=variable_dtype)
        feasible = tf.where(predicate(constrained, self.value))
        feasible_exists = tf.greater(tf.size(feasible), 0)
        return tf.where(feasible_exists, tf.gather(thresholds, tf.gather(feasible, [0])), 0.0)

    def get_config(self):
        config = {
            "num_thresholds": self.num_thresholds,
            "recall": self.recall,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class ThresholdAtNPV(SensitivitySpecificityBase):
    """Computes best recall where precision is >= specified value.

    For a given score-label-distribution the required precision might not
    be achievable, in this case 0.0 is returned as recall.

    This metric creates four local variables, `true_positives`,
    `true_negatives`, `false_positives` and `false_negatives` that are used to
    compute the recall at the given precision. The threshold for the given
    precision value is computed and used to evaluate the corresponding recall.

    If `sample_weight` is `None`, weights default to 1.
    Use `sample_weight` of 0 to mask values.

    If `class_id` is specified, we calculate precision by considering only the
    entries in the batch for which `class_id` is above the threshold
    predictions, and computing the fraction of them for which `class_id` is
    indeed a correct label.

    Args:
      npv: A scalar value in range `[0, 1]`.
      num_thresholds: (Optional) Defaults to 200. The number of thresholds to
        use for matching the given precision.
      class_id: (Optional) Integer class ID for which we want binary metrics.
        This must be in the half-open interval `[0, num_classes)`, where
        `num_classes` is the last dimension of predictions.
      name: (Optional) string name of the metric instance.
      dtype: (Optional) data type of the metric result.

    Standalone usage:

    >>> m = tf.keras.metrics.RecallAtPrecision(0.8)
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9])
    >>> m.result().numpy()
    0.5

    >>> m.reset_state()
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9],
    ...                sample_weight=[1, 0, 0, 1])
    >>> m.result().numpy()
    1.0

    Usage with `compile()` API:

    ```python
    model.compile(
        optimizer='sgd',
        loss='mse',
        metrics=[tf.keras.metrics.RecallAtPrecision(precision=0.8)])
    ```
    """

    @inject_mesh
    def __init__(
        self,
        npv,
        num_thresholds=200,
        class_id=None,
        name=None,
        dtype=None,
    ):
        if npv < 0 or npv > 1:
            raise ValueError(
                "Argument `npv` must be in the range [0, 1]. "
                f"Received: npv={npv}"
            )
        self.npv = npv
        self.num_thresholds = num_thresholds
        super().__init__(
            value=npv,
            num_thresholds=num_thresholds,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )

    def result(self):
        npvs = tf.math.divide_no_nan(
            self.true_negatives,
            tf.math.add(self.true_negatives, self.false_negatives),
        )
        specificities = tf.math.divide_no_nan(
            self.true_negatives,
            tf.math.add(self.true_negatives, self.false_positives),
        )
        return self._find_max_threshold_under_constraint(
            npvs, specificities, tf.greater_equal
        )

    def _find_max_threshold_under_constraint(self, constrained, dependent, predicate):
        """Returns the maximum of dependent_statistic that satisfies the
        constraint.

        Args:
          constrained: Over these values the constraint
            is specified. A rank-1 tensor.
          dependent: From these values the maximum that satiesfies the
            constraint is selected. Values in this tensor and in
            `constrained` are linked by having the same threshold at each
            position, hence this tensor must have the same shape.
          predicate: A binary boolean functor to be applied to arguments
          `constrained` and `self.value`, e.g. `tf.greater`.

        Returns:
          maximal dependent value, if no value satiesfies the constraint 0.0.
        """
        variable_dtype = self.true_negatives.dtype
        thresholds = tf.convert_to_tensor(self.thresholds, dtype=variable_dtype)
        feasible = tf.where(predicate(constrained, self.value))
        feasible_exists = tf.greater(tf.size(feasible), 0)
        index = tf.size(feasible) - 1
        index = tf.where(tf.greater_equal(index, 0), index, 0)
        try:
            return tf.where(feasible_exists,
                            # tf.gather(thresholds, tf.gather(feasible, [tf.shape(feasible)[0] - 1])),
                            tf.gather(thresholds, tf.gather(feasible, [index])),
                            0.0)
        except Exception as e:
            print("Unexpected exception in thresholdAtNPV. " + str(e))
            return 0.0

    def get_config(self):
        config = {
            "num_thresholds": self.num_thresholds,
            "npv": self.npv,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


@tf.function
def tp_tf(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = y_true
    y_pred_label = y_pred
    real_positive_indexes_mask = tf.math.greater(y_true_label, 0)
    predicted_positive_indexes_mask = tf.math.greater(y_pred_label, threshold)
    positive_indexes_intersect_mask = tf.math.logical_and(predicted_positive_indexes_mask, real_positive_indexes_mask)
    predicted_positives = tf.cast(tf.size(tf.where(predicted_positive_indexes_mask)), tf.float32)
    predicted_positives_in_true_set = tf.cast(tf.size(tf.where(positive_indexes_intersect_mask)), tf.float32)
    tp = predicted_positives_in_true_set / (predicted_positives + tf.keras.backend.epsilon())
    return tp


@tf.function
def fp_tf(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = y_true
    y_pred_label = y_pred
    real_positive_indexes_mask = tf.math.greater(y_true_label, 0)
    predicted_positive_indexes_mask = tf.math.greater(y_pred_label, threshold)
    positive_indexes_intersect_mask = tf.math.logical_and(predicted_positive_indexes_mask, real_positive_indexes_mask)
    predicted_positives = tf.cast(tf.size(tf.where(predicted_positive_indexes_mask)), tf.float32)
    predicted_positives_in_true_set = tf.cast(tf.size(tf.where(positive_indexes_intersect_mask)), tf.float32)
    fp = (predicted_positives - predicted_positives_in_true_set) / (predicted_positives + K.epsilon())
    return fp


@tf.function
def fn_tf(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    real_negative_indexes_mask = tf.math.equal(y_true_label, 0)
    predicted_negative_indexes_mask = tf.math.less_equal(y_pred_label, threshold)
    negative_indexes_intersect_mask = tf.math.logical_and(predicted_negative_indexes_mask, real_negative_indexes_mask)
    predicted_negative_indexes_mask = tf.math.less_equal(y_pred_label, threshold)
    predicted_negatives = tf.cast(tf.size(tf.where(predicted_negative_indexes_mask)), tf.float32)
    predicted_negatives_in_true_set = tf.cast(tf.size(tf.where(negative_indexes_intersect_mask)), tf.float32)
    fn = (predicted_negatives - predicted_negatives_in_true_set) / (predicted_negatives + K.epsilon())
    return fn


@tf.function
def tn_tf(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    real_negative_indexes_mask = tf.math.equal(y_true_label, 0)
    predicted_negative_indexes_mask = tf.math.less_equal(y_pred_label, threshold)
    negative_indexes_intersect_mask = tf.math.logical_and(predicted_negative_indexes_mask, real_negative_indexes_mask)
    predicted_negative_indexes_mask = tf.math.less_equal(y_pred_label, threshold)
    predicted_negatives = tf.cast(tf.size(tf.where(predicted_negative_indexes_mask)), tf.float32)
    predicted_negatives_in_true_set = tf.cast(tf.size(tf.where(negative_indexes_intersect_mask)), tf.float32)
    tn = predicted_negatives_in_true_set / (predicted_negatives + tf.keras.backend.epsilon())
    return tn


@tf.function
def precision_tf(y_true, y_pred, label_index=0, threshold=0.5):
    tp = tp_tf(y_true, y_pred, label_index, threshold)
    fp = fp_tf(y_true, y_pred, label_index, threshold)
    return tp / (tp + fp + K.epsilon())


@tf.function
def recall_tf(y_true, y_pred, label_index=0, threshold=0.5):
    tp = tp_tf(y_true, y_pred, label_index, threshold)
    fn = fn_tf(y_true, y_pred, label_index, threshold)
    return tp / (tp + fn + K.epsilon())


@tf.function
def f1_score_tf(y_true, y_pred, label_index=0, threshold=0.5):
    precision = precision_tf(y_true, y_pred, label_index, threshold)
    recall = recall_tf(y_true, y_pred, label_index, threshold)
    return 2 * precision * recall / (precision + recall + K.epsilon())

@tf.function
def precision_at_k(y_true, y_pred, label_index=0, k=100, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    values, indices = tf.math.top_k(y_pred_label, k=k)
    y_true_label = tf.gather(y_true_label, indices)
    y_pred_label = tf.gather(y_pred_label, indices)
    return precision_tf(y_true_label, y_pred_label, label_index=0, threshold=threshold)

@tf.function
def mean_positive_value(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    positive_pred_indexes = tf.where(tf.greater(y_pred_label, threshold))
    return tf.reduce_mean(tf.gather(y_pred_label, positive_pred_indexes))

@tf.function
def mean_true_positive_value(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    tp_pred_indexes = tf.where(tf.logical_and(tf.greater(y_pred_label, threshold), tf.equal(y_true_label, 1)))
    return tf.reduce_mean(tf.gather(y_pred_label, tp_pred_indexes))

@tf.function
def mean_false_positive_value(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    fp_pred_indexes = tf.where(tf.logical_and(tf.greater(y_pred_label, threshold), tf.equal(y_true_label, 0)))
    return tf.reduce_mean(tf.gather(y_pred_label, fp_pred_indexes))

@tf.function
def mean_negative_value(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    negative_pred_indexes = tf.where(tf.less(y_pred_label, threshold))
    return tf.reduce_mean(tf.gather(y_pred_label, negative_pred_indexes))

@tf.function
def mean_true_negative_value(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    tp_pred_indexes = tf.where(tf.logical_and(tf.less(y_pred_label, threshold), tf.equal(y_true_label, 0)))
    return tf.reduce_mean(tf.gather(y_pred_label, tp_pred_indexes))

@tf.function
def mean_false_negative_value(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_true_label = y_true_label[:, 0]
    y_pred_label = y_pred_label[:, 0]
    tp_pred_indexes = tf.where(tf.logical_and(tf.less(y_pred_label, threshold), tf.equal(y_true_label, 1)))
    return tf.reduce_mean(tf.gather(y_pred_label, tp_pred_indexes))

@tf.function
def confusion_matrix_values_tf(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = tf.gather(y_true, [label_index], axis=1)
    y_pred_label = tf.gather(y_pred, [label_index], axis=1)
    y_pred_label = tf.reshape(y_pred_label, tf.shape(y_pred_label)[0])
    y_true_label = tf.reshape(y_true_label, tf.shape(y_true_label)[0])
    real_positive_indexes_mask = tf.math.greater(y_true_label, 0)
    predicted_positive_indexes_mask = tf.math.greater(y_pred_label, threshold)
    positive_indexes_intersect_mask = tf.math.logical_and(predicted_positive_indexes_mask, real_positive_indexes_mask)
    predicted_positives = tf.where(predicted_positive_indexes_mask).shape.as_list()[0]
    predicted_positives_in_true_set = tf.where(positive_indexes_intersect_mask).shape.as_list()[0]
    tp = predicted_positives_in_true_set / (predicted_positives + tf.keras.backend.epsilon())
    real_negative_indexes_mask = tf.math.equal(y_true_label, 0)
    predicted_negative_indexes_mask = tf.math.less_equal(y_pred_label, threshold)
    negative_indexes_intersect_mask = tf.math.logical_and(predicted_negative_indexes_mask, real_negative_indexes_mask)
    predicted_negatives = tf.where(predicted_negative_indexes_mask).shape.as_list()[0]
    predicted_negatives_in_true_set = tf.where(negative_indexes_intersect_mask).shape.as_list()[0]
    correct_predictions = predicted_positives_in_true_set + predicted_negatives_in_true_set
    total_predictions = y_true.shape.as_list()[0]
    accuracy = correct_predictions / (total_predictions + K.epsilon())
    error_rate = 1 - accuracy
    #TODO decide what values to be returned when no positives are detected
    if predicted_positives == 0:
        return [[np.nan, np.nan], [np.nan, np.nan]], accuracy, error_rate, np.nan, np.nan, np.nan, np.nan
    else:
        tn = predicted_negatives_in_true_set / (predicted_negatives + tf.keras.backend.epsilon())
        fp = (predicted_positives - predicted_positives_in_true_set) / (predicted_positives + K.epsilon())
        fn = (predicted_negatives - predicted_negatives_in_true_set) / (predicted_negatives + K.epsilon())
        precision = tp / (tp + fp + K.epsilon())
        recall = tp / (tp + fn + K.epsilon())
        f1_score = 2 * precision * recall / (precision + recall + K.epsilon())
        return [[tp, fp], [fn, tn]], accuracy, error_rate, precision, recall, f1_score, np.nan


def confusion_matrix_values(y_true, y_pred, label_index=0, threshold=0.5):
    y_true_label = np.transpose(y_true)[label_index]
    y_pred_label = np.transpose(y_pred)[label_index]
    real_positive_indexes_mask = y_true_label > 0
    predicted_positive_indexes_mask = y_pred_label > threshold
    positive_indexes_intersect_mask = np.logical_and(predicted_positive_indexes_mask, real_positive_indexes_mask)
    predicted_positives = len(np.argwhere(predicted_positive_indexes_mask).flatten())
    predicted_positives_in_true_set = len(np.argwhere(positive_indexes_intersect_mask).flatten())
    tp = predicted_positives_in_true_set / (predicted_positives + tf.keras.backend.epsilon())
    real_negative_indexes_mask = y_true_label == 0
    predicted_negative_indexes_mask = y_pred_label < threshold
    negative_indexes_intersect_mask = np.logical_and(predicted_negative_indexes_mask, real_negative_indexes_mask)
    predicted_negatives = len(np.argwhere(predicted_negative_indexes_mask).flatten())
    predicted_negatives_in_true_set = len(np.argwhere(negative_indexes_intersect_mask).flatten())
    correct_predictions = predicted_positives_in_true_set + predicted_negatives_in_true_set
    total_predictions = len(y_true)
    accuracy = correct_predictions / (total_predictions + K.epsilon())
    error_rate = 1 - accuracy
    #TODO decide what values to be returned when no positives are detected
    if predicted_positives == 0:
        return [[np.nan, np.nan], [np.nan, np.nan]], accuracy, error_rate, np.nan, np.nan, np.nan
    else:
        tn = predicted_negatives_in_true_set / (predicted_negatives + K.epsilon())
        fp = (predicted_positives - predicted_positives_in_true_set) / (predicted_positives + K.epsilon())
        fn = (predicted_negatives - predicted_negatives_in_true_set) / (predicted_negatives + K.epsilon())
        precision = tp / (tp + fp + K.epsilon())
        recall = tp / (tp + fn + K.epsilon())
        f1_score = 2 * precision * recall / (precision + recall + K.epsilon())
        return [[tp, fp], [fn, tn]], accuracy, error_rate, precision, recall, f1_score

def area_under_curve(y_true, y_pred, label_index=0, thresholds=100, method='roc'):
    confusion_matrixes = np.empty((thresholds, 2, 2))
    accuracies = np.zeros(thresholds)
    error_rates = np.zeros(thresholds)
    precisions = np.zeros(thresholds)
    recalls = np.zeros(thresholds)
    f1_scores = np.zeros(thresholds)
    threshold_values = np.flip(np.linspace(0, 1, thresholds))
    for index, threshold in enumerate(threshold_values):
        confusion_matrixes[index], accuracies[index], error_rates[index], precisions[index], recalls[index], \
            f1_scores[index] = confusion_matrix_values(y_true, y_pred, label_index=label_index, threshold=threshold)
    nan_values = np.logical_and(np.isnan(recalls), np.isnan(precisions))
    x = recalls[~nan_values]
    y = precisions[~nan_values]
    threshold_values = threshold_values[~nan_values]
    return x, y, threshold_values, np.trapz(y, x)


class CategoricalClassMetric(tf.keras.metrics.Metric):
    def __init__(self, class_index, metric_function, batch_size, name="categorical_class_metric", metric_threshold=0.5,
                 **kwargs):
        super(CategoricalClassMetric, self).__init__(name=name, **kwargs)
        self.batch_size = batch_size
        self.metric_function = metric_function
        self.metric_threshold = metric_threshold
        self.class_index = class_index
        self.metric = 0

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.metric = self.metric_function(y_true, y_pred, self.class_index, self.metric_threshold)

    def result(self):
        return self.metric

class NegativePredictiveValue(Metric):
    """Computes the NPV of the predictions with respect to the labels.

    The metric creates two local variables, `true_positives` and
    `false_positives` that are used to compute the precision. This value is
    ultimately returned as `precision`, an idempotent operation that simply
    divides `true_positives` by the sum of `true_positives` and
    `false_positives`.

    If `sample_weight` is `None`, weights default to 1.
    Use `sample_weight` of 0 to mask values.

    If `top_k` is set, we'll calculate precision as how often on average a class
    among the top-k classes with the highest predicted values of a batch entry
    is correct and can be found in the label for that entry.

    If `class_id` is specified, we calculate precision by considering only the
    entries in the batch for which `class_id` is above the threshold and/or in
    the top-k highest predictions, and computing the fraction of them for which
    `class_id` is indeed a correct label.

    Args:
      thresholds: (Optional) A float value, or a Python list/tuple of float
        threshold values in [0, 1]. A threshold is compared with prediction
        values to determine the truth value of predictions (i.e., above the
        threshold is `true`, below is `false`). If used with a loss function
        that sets `from_logits=True` (i.e. no sigmoid applied to predictions),
        `thresholds` should be set to 0. One metric value is generated for each
        threshold value. If neither thresholds nor top_k are set, the default is
        to calculate precision with `thresholds=0.5`.
      top_k: (Optional) Unset by default. An int value specifying the top-k
        predictions to consider when calculating precision.
      class_id: (Optional) Integer class ID for which we want binary metrics.
        This must be in the half-open interval `[0, num_classes)`, where
        `num_classes` is the last dimension of predictions.
      name: (Optional) string name of the metric instance.
      dtype: (Optional) data type of the metric result.

    Standalone usage:

    >>> m = tf.keras.metrics.Precision()
    >>> m.update_state([0, 1, 1, 1], [1, 0, 1, 1])
    >>> m.result().numpy()
    0.6666667

    >>> m.reset_state()
    >>> m.update_state([0, 1, 1, 1], [1, 0, 1, 1], sample_weight=[0, 0, 1, 0])
    >>> m.result().numpy()
    1.0

    >>> # With top_k=2, it will calculate precision over y_true[:2]
    >>> # and y_pred[:2]
    >>> m = tf.keras.metrics.Precision(top_k=2)
    >>> m.update_state([0, 0, 1, 1], [1, 1, 1, 1])
    >>> m.result().numpy()
    0.0

    >>> # With top_k=4, it will calculate precision over y_true[:4]
    >>> # and y_pred[:4]
    >>> m = tf.keras.metrics.Precision(top_k=4)
    >>> m.update_state([0, 0, 1, 1], [1, 1, 1, 1])
    >>> m.result().numpy()
    0.5

    Usage with `compile()` API:

    ```python
    model.compile(optimizer='sgd',
                  loss='binary_crossentropy',
                  metrics=[tf.keras.metrics.Precision()])
    ```

    Usage with a loss with `from_logits=True`:

    ```python
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=[tf.keras.metrics.Precision(thresholds=0)])
    ```
    """

    @inject_mesh
    def __init__(
        self, thresholds=None, top_k=None, class_id=None, name=None, dtype=None
    ):
        super().__init__(name=name, dtype=dtype)
        self.init_thresholds = thresholds
        self.top_k = top_k
        self.class_id = class_id

        default_threshold = 0.5 if top_k is None else metrics_utils.NEG_INF
        self.thresholds = metrics_utils.parse_init_thresholds(
            thresholds, default_threshold=default_threshold
        )
        self._thresholds_distributed_evenly = (
            metrics_utils.is_evenly_distributed_thresholds(self.thresholds)
        )
        self.true_negatives = self.add_weight(
            name="true_negatives", shape=(len(self.thresholds),), initializer="zeros"
        )
        self.false_negatives = self.add_weight(
            name="false_negatives",
            shape=(len(self.thresholds),),
            initializer="zeros",
        )

    def update_state(self, y_true, y_pred, sample_weight=None):
        """Accumulates true positive and false positive statistics.

        Args:
          y_true: The ground truth values, with the same dimensions as `y_pred`.
            Will be cast to `bool`.
          y_pred: The predicted values. Each element must be in the range
            `[0, 1]`.
          sample_weight: Optional weighting of each example. Can
            be a `Tensor` whose rank is either 0, or the same rank as `y_true`,
            and must be broadcastable to `y_true`. Defaults to `1`.

        Returns:
          Update op.
        """
        return metrics_utils.update_confusion_matrix_variables(
            {
                metrics_utils.ConfusionMatrix.TRUE_NEGATIVES: self.true_negatives,  # noqa: E501
                metrics_utils.ConfusionMatrix.FALSE_NEGATIVES: self.false_negatives,  # noqa: E501
            },
            y_true,
            y_pred,
            thresholds=self.thresholds,
            thresholds_distributed_evenly=self._thresholds_distributed_evenly,
            top_k=self.top_k,
            class_id=self.class_id,
            sample_weight=sample_weight,
        )

    def result(self):
        result = tf.math.divide_no_nan(
            self.true_negatives,
            tf.math.add(self.true_negatives, self.false_negatives),
        )
        return result[0] if len(self.thresholds) == 1 else result

    def reset_state(self):
        num_thresholds = len(to_list(self.thresholds))
        backend.batch_set_value(
            [
                (v, np.zeros((num_thresholds,)))
                for v in (self.true_negatives, self.false_negatives)
            ]
        )

    def get_config(self):
        config = {
            "thresholds": self.init_thresholds,
            "top_k": self.top_k,
            "class_id": self.class_id,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class Specificity(Metric):
    """Computes the NPV of the predictions with respect to the labels.

    The metric creates two local variables, `true_positives` and
    `false_positives` that are used to compute the precision. This value is
    ultimately returned as `precision`, an idempotent operation that simply
    divides `true_positives` by the sum of `true_positives` and
    `false_positives`.

    If `sample_weight` is `None`, weights default to 1.
    Use `sample_weight` of 0 to mask values.

    If `top_k` is set, we'll calculate precision as how often on average a class
    among the top-k classes with the highest predicted values of a batch entry
    is correct and can be found in the label for that entry.

    If `class_id` is specified, we calculate precision by considering only the
    entries in the batch for which `class_id` is above the threshold and/or in
    the top-k highest predictions, and computing the fraction of them for which
    `class_id` is indeed a correct label.

    Args:
      thresholds: (Optional) A float value, or a Python list/tuple of float
        threshold values in [0, 1]. A threshold is compared with prediction
        values to determine the truth value of predictions (i.e., above the
        threshold is `true`, below is `false`). If used with a loss function
        that sets `from_logits=True` (i.e. no sigmoid applied to predictions),
        `thresholds` should be set to 0. One metric value is generated for each
        threshold value. If neither thresholds nor top_k are set, the default is
        to calculate precision with `thresholds=0.5`.
      top_k: (Optional) Unset by default. An int value specifying the top-k
        predictions to consider when calculating precision.
      class_id: (Optional) Integer class ID for which we want binary metrics.
        This must be in the half-open interval `[0, num_classes)`, where
        `num_classes` is the last dimension of predictions.
      name: (Optional) string name of the metric instance.
      dtype: (Optional) data type of the metric result.

    Standalone usage:

    >>> m = tf.keras.metrics.Precision()
    >>> m.update_state([0, 1, 1, 1], [1, 0, 1, 1])
    >>> m.result().numpy()
    0.6666667

    >>> m.reset_state()
    >>> m.update_state([0, 1, 1, 1], [1, 0, 1, 1], sample_weight=[0, 0, 1, 0])
    >>> m.result().numpy()
    1.0

    >>> # With top_k=2, it will calculate precision over y_true[:2]
    >>> # and y_pred[:2]
    >>> m = tf.keras.metrics.Precision(top_k=2)
    >>> m.update_state([0, 0, 1, 1], [1, 1, 1, 1])
    >>> m.result().numpy()
    0.0

    >>> # With top_k=4, it will calculate precision over y_true[:4]
    >>> # and y_pred[:4]
    >>> m = tf.keras.metrics.Precision(top_k=4)
    >>> m.update_state([0, 0, 1, 1], [1, 1, 1, 1])
    >>> m.result().numpy()
    0.5

    Usage with `compile()` API:

    ```python
    model.compile(optimizer='sgd',
                  loss='binary_crossentropy',
                  metrics=[tf.keras.metrics.Precision()])
    ```

    Usage with a loss with `from_logits=True`:

    ```python
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=[tf.keras.metrics.Precision(thresholds=0)])
    ```
    """

    @inject_mesh
    def __init__(
        self, thresholds=None, top_k=None, class_id=None, name=None, dtype=None
    ):
        super().__init__(name=name, dtype=dtype)
        self.init_thresholds = thresholds
        self.top_k = top_k
        self.class_id = class_id

        default_threshold = 0.5 if top_k is None else metrics_utils.NEG_INF
        self.thresholds = metrics_utils.parse_init_thresholds(
            thresholds, default_threshold=default_threshold
        )
        self._thresholds_distributed_evenly = (
            metrics_utils.is_evenly_distributed_thresholds(self.thresholds)
        )
        self.true_negatives = self.add_weight(
            name="true_negatives", shape=(len(self.thresholds),), initializer="zeros"
        )
        self.false_positives = self.add_weight(
            name="false_positives",
            shape=(len(self.thresholds),),
            initializer="zeros",
        )

    def update_state(self, y_true, y_pred, sample_weight=None):
        """Accumulates true positive and false positive statistics.

        Args:
          y_true: The ground truth values, with the same dimensions as `y_pred`.
            Will be cast to `bool`.
          y_pred: The predicted values. Each element must be in the range
            `[0, 1]`.
          sample_weight: Optional weighting of each example. Can
            be a `Tensor` whose rank is either 0, or the same rank as `y_true`,
            and must be broadcastable to `y_true`. Defaults to `1`.

        Returns:
          Update op.
        """
        return metrics_utils.update_confusion_matrix_variables(
            {
                metrics_utils.ConfusionMatrix.TRUE_NEGATIVES: self.true_negatives,  # noqa: E501
                metrics_utils.ConfusionMatrix.FALSE_POSITIVES: self.false_positives,  # noqa: E501
            },
            y_true,
            y_pred,
            thresholds=self.thresholds,
            thresholds_distributed_evenly=self._thresholds_distributed_evenly,
            top_k=self.top_k,
            class_id=self.class_id,
            sample_weight=sample_weight,
        )

    def result(self):
        result = tf.math.divide_no_nan(
            self.true_negatives,
            tf.math.add(self.true_negatives, self.false_positives),
        )
        return result[0] if len(self.thresholds) == 1 else result

    def reset_state(self):
        num_thresholds = len(to_list(self.thresholds))
        backend.batch_set_value(
            [
                (v, np.zeros((num_thresholds,)))
                for v in (self.true_negatives, self.false_positives)
            ]
        )

    def get_config(self):
        config = {
            "thresholds": self.init_thresholds,
            "top_k": self.top_k,
            "class_id": self.class_id,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class SpecificityAtNPV(SensitivitySpecificityBase):
    """Computes best recall where precision is >= specified value.

    For a given score-label-distribution the required precision might not
    be achievable, in this case 0.0 is returned as recall.

    This metric creates four local variables, `true_positives`,
    `true_negatives`, `false_positives` and `false_negatives` that are used to
    compute the recall at the given precision. The threshold for the given
    precision value is computed and used to evaluate the corresponding recall.

    If `sample_weight` is `None`, weights default to 1.
    Use `sample_weight` of 0 to mask values.

    If `class_id` is specified, we calculate precision by considering only the
    entries in the batch for which `class_id` is above the threshold
    predictions, and computing the fraction of them for which `class_id` is
    indeed a correct label.

    Args:
      npv: A scalar value in range `[0, 1]`.
      num_thresholds: (Optional) The number of thresholds to
        use for matching the given precision. Defaults to `200`.
      class_id: (Optional) Integer class ID for which we want binary metrics.
        This must be in the half-open interval `[0, num_classes)`, where
        `num_classes` is the last dimension of predictions.
      name: (Optional) string name of the metric instance.
      dtype: (Optional) data type of the metric result.

    Standalone usage:

    >>> m = tf.keras.metrics.RecallAtPrecision(0.8)
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9])
    >>> m.result().numpy()
    0.5

    >>> m.reset_state()
    >>> m.update_state([0, 0, 1, 1], [0, 0.5, 0.3, 0.9],
    ...                sample_weight=[1, 0, 0, 1])
    >>> m.result().numpy()
    1.0

    Usage with `compile()` API:

    ```python
    model.compile(
        optimizer='sgd',
        loss='binary_crossentropy',
        metrics=[tf.keras.metrics.RecallAtPrecision(precision=0.8)])
    ```
    """

    @inject_mesh
    def __init__(
        self,
        npv,
        num_thresholds=200,
        class_id=None,
        name=None,
        dtype=None,
    ):
        if npv < 0 or npv > 1:
            raise ValueError(
                "Argument `npv` must be in the range [0, 1]. "
                f"Received: npv={npv}"
            )
        self.npv = npv
        self.num_thresholds = num_thresholds
        super().__init__(
            value=npv,
            num_thresholds=num_thresholds,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )

    def result(self):
        npvs = tf.math.divide_no_nan(
            self.true_negatives,
            tf.math.add(self.true_negatives, self.false_negatives),
        )
        sensitivities = tf.math.divide_no_nan(
            self.true_negatives,
            tf.math.add(self.true_negatives, self.false_positives),
        )
        return self._find_max_under_constraint(
            npvs, sensitivities, tf.greater_equal
        )

    def get_config(self):
        config = {
            "num_thresholds": self.num_thresholds,
            "npv": self.npv,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))
