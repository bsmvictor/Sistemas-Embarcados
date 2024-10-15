import numpy as np
import matplotlib.pyplot as plt
import control as ctrl


def method_smith(step, time, output, k, thau, theta, mesh='Opened'):
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

    if mesh == 'Opened':

        step_amp = step.mean()  # Amplitude do degrau de entrada

        def identified_model(k, tau, theta):
            G_s = ctrl.tf([k], [tau, 1])
            num_pade, den_pade = ctrl.pade(theta, 5)
            pade_prox = ctrl.tf(num_pade, den_pade)

            return ctrl.series(G_s, pade_prox)

        result_estimated_model = identified_model(k, thau, theta)

        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        MSE = np.sqrt(np.sum((result_model - output) ** 2)/ len(output))

        print(result_estimated_model)

        response_info = ctrl.step_info(result_estimated_model)

        return {
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'step_amp': step_amp
        }

    if mesh == 'Closed':
        step_amp = step.mean()  # Amplitude do degrau de entrada

        def identified_model(k, tau, theta):
            G_s = ctrl.tf([k], [tau, 1])
            H_s = ctrl.feedback(G_s, 1)
            num_pade, den_pade = ctrl.pade(theta, 5)
            pade_prox = ctrl.tf(num_pade, den_pade)

            return ctrl.series(H_s, pade_prox)

        result_estimated_model = identified_model(k, thau, theta)

        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        MSE = np.sqrt(np.sum((result_model - output) ** 2) / len(output))

        response_info = ctrl.step_info(result_estimated_model)

        return {
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'step_amp': step_amp
        }
