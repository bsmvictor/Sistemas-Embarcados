import control as ctrl
from matplotlib import pyplot as plt


def pid_controller(k, tau, theta, result_estimated_model, step_amp, pid='Nenhum'):
    """
    Implements a PID controller based on various tuning methods, including Ziegler-Nichols,
    IMC, CHR, Cohen and Coon, and ITAE, and applies it to a first-order model with transport delay.

    Args:
        - k (float): System gain.
        - tau (float): Time constant of the system.
        - theta (float): Transport delay of the system.
        - result_estimated_model (TransferFunction): Identified transfer function of the system.
        - step_amp (float): Amplitude of the input step.
        - pid (str): PID tuning method to be applied. Default is 'Nenhum' (no controller).

    Returns:
        dict or str: If 'Nenhum' is selected, a message indicating no PID is returned.
                     Otherwise, a dictionary containing:
                     - result_time (array-like): Time points for the step response of the system.
                     - result_model (array-like): Step response data of the system.
                     - response_info (dict): Step response characteristics.
                     - title (str): Title describing the PID tuning method used.
    """

    if pid == 'Nenhum':
        return 'PID controller not defined'

    # Ziegler-Nichols method for open-loop systems
    if pid == 'Ziegler Nichols Malha Aberta':
        kp = (1.2 * tau) / (k * theta)
        ti = 2 * theta
        td = 0.5 * theta

        def funcao_PID(kp, ti, td):
            # PID transfer function
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        # Closed-loop system with PID controller
        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        # Step response simulation
        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'Ziegler Nichols\n Sistema rápido, com overshoot'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    # Internal Model Control (IMC) method
    if pid == 'IMC':
        lamb = 20
        kp = ((2 * tau) + theta) / (k * ((2 * lamb) + theta))
        ti = tau + (theta / 2)
        td = (tau * theta) / ((2 * tau) + theta)

        def function_pid(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = function_pid(kp, ti, td)

        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'IMC\n Sistema lento, sem overshoot (ts elevado)'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    # CHR method without overshoot
    if pid == 'CHR sem Sobrevalor':
        kp = (0.6 * tau) / (k * theta)
        ti = tau
        td = 0.5 * theta

        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'CHR sem Sobrevalor\n Sistema rápido, sem overshoot'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    # CHR method with overshoot
    if pid == 'CHR com Sobrevalor':
        kp = (0.95 * tau) / (k * theta)
        ti = 1.357 * tau
        td = 0.473 * theta

        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'CHR com Sobrevalor\n Sistema lento, com overshoot'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    # Cohen and Coon method
    if pid == 'Cohen e Coon':
        kp = (tau / (k * theta)) * ((16 * tau + 3 * theta) / (12 * tau))
        ti = theta * ((32 + (6 * theta / tau)) / (13 + (8 * theta / tau)))
        td = (4 * theta) / (11 + (2 * theta / tau))

        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'Cohen e Coon'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    # ITAE method
    if pid == 'ITAE':
        A = 0.965
        B = -0.85
        C = 0.796
        D = -0.147
        E = 0.308
        F = 0.929

        kp = (A / k) * (theta / tau) ** B
        ti = tau / (C + D * (theta / tau))
        td = tau * E * (theta / tau) ** F

        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'ITAE'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }
