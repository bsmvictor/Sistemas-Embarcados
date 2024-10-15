import numpy as np
import matplotlib.pyplot as plt
import control as ctrl


def method_smith(step, time, output, k, tau, theta, mesh='Opened'):
    """
    Identifies control systems using the Smith method based on
    test data, considering a first-order model with transport delay (FOPDT).

    Args:
        - step (float): Amplitude of the input step. Should be a finite, non-zero number.
        - time (array-like): Time points of the process sampling. Must be non-empty.
        - output (array-like): Output data of the process at the given time points. Must be non-empty.
        - k (float): System gain (steady-state gain).
        - tau (float): Time constant of the system.
        - theta (float): Transport delay (dead time) of the system.
        - mesh (str): Control mesh type, either 'Opened' or 'Closed'. Default is 'Opened'.

    Returns:
        dict: Contains identified system parameters, including:
            - MSE (float): Mean Squared Error between the model and the output.
            - result_estimated_model: Transfer function of the estimated system.
            - result_time (array): Time points for the step response of the estimated model.
            - result_model (array): Step response of the estimated model.
            - response_info (dict): Step response characteristics such as rise time, settling time, etc.
            - step_amp (float): Amplitude of the input step.
    """
    
    # Check if mesh is set to 'Opened' (Open-loop control)
    if mesh == 'Opened':
        # Calculate the mean value of the input step amplitude
        step_amp = step.mean()

        # Define the identified model for the system based on k, tau, and theta
        def identified_model(k, tau, theta):
            # First-order transfer function G(s) = k / (tau*s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            # Approximate the transport delay using Pade approximation
            num_pade, den_pade = ctrl.pade(theta, 5)
            pade_prox = ctrl.tf(num_pade, den_pade)

            # Combine the first-order system with the Pade approximation of the delay
            return ctrl.series(G_s, pade_prox)

        # Generate the identified model using the provided parameters
        result_estimated_model = identified_model(k, tau, theta)

        # Simulate the step response of the model, scaled by the step amplitude
        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        # Calculate the Mean Squared Error (MSE) between the model response and the actual output
        MSE = np.sqrt(np.sum((result_model - output) ** 2) / len(output))

        # Get step response characteristics (rise time, settling time, etc.)
        response_info = ctrl.step_info(result_estimated_model)

        # Return the results as a dictionary
        return {
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'step_amp': step_amp
        }

    # Check if mesh is set to 'Closed' (Closed-loop control)
    if mesh == 'Closed':
        # Calculate the mean value of the input step amplitude
        step_amp = step.mean()

        # Define the identified model for the closed-loop system
        def identified_model(k, tau, theta):
            # First-order transfer function G(s) = k / (tau*s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            # Create the closed-loop transfer function with unity feedback
            H_s = ctrl.feedback(G_s, 1)
            # Approximate the transport delay using Pade approximation
            num_pade, den_pade = ctrl.pade(theta, 5)
            pade_prox = ctrl.tf(num_pade, den_pade)

            # Combine the closed-loop system with the Pade approximation of the delay
            return ctrl.series(H_s, pade_prox)

        # Generate the identified model using the provided parameters
        result_estimated_model = identified_model(k, tau, theta)

        # Simulate the step response of the model, scaled by the step amplitude
        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        # Calculate the Mean Squared Error (MSE) between the model response and the actual output
        MSE = np.sqrt(np.sum((result_model - output) ** 2) / len(output))

        # Get step response characteristics (rise time, settling time, etc.)
        response_info = ctrl.step_info(result_estimated_model)

        # Return the results as a dictionary
        return {
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'step_amp': step_amp
        }
