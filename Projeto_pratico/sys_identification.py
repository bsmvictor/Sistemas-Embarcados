import numpy as np


def system_identification(step, time, output, method='Smith'):
    '''
    Identifies control systems using the Smith or Sundaresan methods based on
    test data, considering a first-order model with transport delay (FOPDT).

    Args:
        - step (float): Amplitude of the input step. Must be a finite, non-zero number.
        - time (array-like): Sampling time points of the process. Must be non-empty.
        - output (array-like): Output samples of the process at the given sampling times. Must be non-empty.
        - method (str): Identification method to be used: 'Smith' (default) or 'Sundaresan'. Must be a valid string.

    Returns:
        - dict: Structure containing the identified system parameters.
    '''

    # Smith method for system identification
    if method == 'Smith':
        # 1. Find the output values corresponding to 28.3% and 63.2% of the final value
        y1 = 0.283 * output[-1]
        y2 = 0.632 * output[-1]

        # Find t1 and t2 in the data (time points corresponding to y1 and y2)
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 2. Calculate τ and θ using the Smith method
        tau = 1.5 * (t2 - t1)
        theta = t2 - tau

        # 3. Calculate system gain k
        step_amp = step.mean()  # Amplitude of the input step
        k = (output[-1] - output[0]) / step_amp

        return {
            'k': k,  # System gain
            'tau': tau,  # Time constant
            'theta': theta  # Transport delay
        }

    # Sundaresan method for system identification
    if method == 'Sundaresan':
        # 1. Find the output values corresponding to 35.3% and 85.3% of the final value
        y1 = 0.353 * output[-1]
        y2 = 0.853 * output[-1]

        # Find t1 and t2 in the data (time points corresponding to y1 and y2)
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 2. Calculate τ and θ using the Sundaresan method
        tau = (2 / 3) * (t2 - t1)
        theta = (1.3 * t1) - (0.29 * t2)

        # 3. Calculate system gain k
        step_amp = step.mean()  # Amplitude of the input step
        k = (output[-1] - output[0]) / step_amp

        return {
            'k': k,  # System gain
            'tau': tau,  # Time constant
            'theta': theta  # Transport delay
        }
