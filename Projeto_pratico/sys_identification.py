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

    if method == 'Smith':
        # 1. Encontrar os tempos correspondentes a 28,3% e 63,2% do valor final
        y1 = 0.283 * output[-1]
        y2 = 0.632 * output[-1]

        # Encontrar t1 e t2 nos dados
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 3. Calcular τ e θ usando o Método de Smith
        tau = 1.5 * (t2 - t1)
        theta = t2 - tau

        # 4. Calcular o ganho k
        step_amp = step.mean()  # Amplitude do degrau de entrada
        k = (output[-1] - output[0]) / step_amp

        return {
            'k': k,
            'tau': tau,
            'theta': theta
        }

    if method == 'Sundaresan':
        # 1. Encontrar os tempos correspondentes a 28,3% e 63,2% do valor final
        y1 = 0.353 * output[-1]
        y2 = 0.853 * output[-1]

        # Encontrar t1 e t2 nos dados
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 3. Calcular τ e θ usando o Método de Smith
        tau = (2 / 3) * (t2 - t1)
        theta = (1.3 * t1) - (0.29 * t2)

        # 4. Calcular o ganho k
        step_amp = step.mean()  # Amplitude do degrau de entrada
        k = (output[-1] - output[0]) / step_amp

        return {
            'k': k,
            'tau': tau,
            'theta': theta
        }