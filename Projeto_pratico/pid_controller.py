import control as ctrl
from matplotlib import pyplot as plt


def pid_controller (k, tau, theta, result_estimated_model, step_amp ,pid = 'Nenhum'):
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

    if pid == 'Nenhum':
        return 'PID controller not defined'

    if pid == 'Ziegler Nichols Malha Aberta':
        kp = (1.2 * tau) / (k * theta)
        ti = 2 * theta
        td = 0.5 * theta

        # 7. função do PID
        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        # Sistema em malha fechada com controlador PID e modelo identificado
        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        # Simulação da resposta ao degrau
        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'Zigler Nichols\n Sistema rápido, com overshoot'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }


    if pid == 'IMC':
        # Calculando os valores de kp, ti e td
        lamb = 20
        kp = ((2 * tau) + theta) / (k * ((2 * lamb) + theta))
        ti = tau + (theta / 2)
        td = (tau * theta) / ((2 * tau) + theta)

        # 7. função do PID
        def function_pid(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = function_pid(kp, ti, td)

        # Sistema em malha fechada com controlador PID e modelo identificado
        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        # Simulação da resposta ao degrau
        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'IMC\n Sistema lento, sem overshoot (ts elevado)'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    if pid == 'CHR sem Sobrevalor':
        # Calculando os valores de kp, ti e td
        kp = (0.6 * tau) / (k * theta)
        ti = tau
        td = 0.5 * theta

        # 7. função do PID
        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        # Sistema em malha fechada com controlador PID e modelo identificado
        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        # Simulação da resposta ao degrau
        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'CHR sem Sobrevalor\n Sistema rápido, sem overshoot'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    if pid == 'CHR com Sobrevalor':
        # Calculando os valores de kp, ti e td
        kp = (0.95 * tau) / (k * theta)
        ti = 1.357 * tau
        td = 0.473 * theta

        # 7. função do PID
        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        # Sistema em malha fechada com controlador PID e modelo identificado
        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        # Simulação da resposta ao degrau
        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'CHR com Sobrevalor\n Sistema lento, com overshoot'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    if pid == 'Cohen e Coon':
        kp = (tau / (k * theta)) * ((16 * tau + 3 * theta) / (12 * tau))
        ti = theta * ((32 + (6 * theta / tau)) / (13 + (8 * theta / tau)))
        td = (4 * theta) / (11 + (2 * theta / tau))

        # 7. função do PID
        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        # Sistema em malha fechada com controlador PID e modelo identificado
        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        # Simulação da resposta ao degrau
        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'Coheen e Coon'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }

    if pid == 'ITAE':
        A = 0.965
        B = -0.85
        C = 0.796
        D = -0.147
        E = 0.308
        F = 0.929

        kp = (A/k) * (theta/tau)**B
        ti = (tau/(C + D*(theta/tau)))
        td = tau * E * (theta/tau)**F

        # 7. função do PID
        def funcao_PID(kp, ti, td):
            pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])
            return pid

        PID = funcao_PID(kp, ti, td)

        # Sistema em malha fechada com controlador PID e modelo identificado
        system_closed_mesh = ctrl.feedback(ctrl.series(PID, result_estimated_model))

        # Simulação da resposta ao degrau
        result_time, result_model = ctrl.step_response(system_closed_mesh)

        response_info = ctrl.step_info(system_closed_mesh)

        title = 'ITAE'

        return {
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'title': title
        }