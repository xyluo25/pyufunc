.. _util_ai_tutorial:

=======
util_ai
=======

Introduction:
The util_ai package is a collection of utility functions that are used in AI and ML projects. The package includes functions for error measurement, pytorch model, scikit-learn model, scipy model, tensorflow model, and other utility functions.

Below are the functions available in the util_ai package:

Error Measurement
-----------------
It's important to measure the performance of an AI model. The following are some of the error measurement techniques:

- Mean Squared Error (MSE)

  For detailed input and output parameters, please refer to the :func:`mean_squared_error` function.

  .. code-block:: python

    from pyufunc import mean_squared_error
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    mean_squared_error(y_true, y_pred)
    0.375


- Mean Absolute Error (MAE)

  .. code-block:: python

    from pyufunc import mean_absolute_error
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    mean_absolute_error(y_true, y_pred)
    0.5

- Mean Absolute Percentage Error (MAPE)

  .. code-block:: python

    from pyufunc import mean_absolute_percentage_error
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    mean_absolute_percentage_error(y_true, y_pred)
    0.3273

- Mean Percentage Error (MPE)

  .. code-block:: python

    from pyufunc import mean_percentage_error
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    mean_percentage_error(y_true, y_pred)
    0.3273

- Mean Square Log Error (MSLE)

  .. code-block:: python

    from pyufunc import mean_squared_log_error
    y_true = [3, 5, 2.5, 7]
    y_pred = [2.5, 5, 4, 8]
    mean_squared_log_error(y_true, y_pred)
    0.0397

- Root Mean Squared Error (RMSE)

  .. code-block:: python

    from pyufunc import root_mean_squared_error
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    root_mean_squared_error(y_true, y_pred)
    0.6123

- R2 Score

  .. code-block:: python

    from pyufunc import r2_score
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0.0, 2, 8]
    r2_score(y_true, y_pred)
    0.9486
