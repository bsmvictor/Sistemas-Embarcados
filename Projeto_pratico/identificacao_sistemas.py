import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from scipy.io import loadmat

def identificacaoSistemas (step, time, output, method = 'Smith', mesh = 'Opened'):
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

    # Inserir valores default caso ausência de parâmetro
    if method is None:
        method = 'Smith'

    if mesh is None:
        method = 'Open'

    if method == 'Smith' and mesh == 'Opened':
        # 1. Determinar o valor final da saída
        final_value = output[-1]

        # 2. Encontrar os tempos correspondentes a 28,3% e 63,2% do valor final
        y1 = 0.283 * final_value
        y2 = 0.632 * final_value

        # Encontrar t1 e t2 nos dados
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 3. Calcular τ e θ usando o Método de Smith
        tau = 1.5 * (t2 - t1)
        theta = t2 - tau

        # 4. Calcular o ganho k
        step_amp = step.mean()  # Amplitude do degrau de entrada
        k = (final_value - output[0]) / step_amp
        set_point = step_amp

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def identified_model(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(G_s, pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        result_estimated_model = identified_model(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        MSE = np.sqrt(np.sum((result_model - output) ** 2) / len(output))
          
        # Exibir os resultados
        print(f'Método de Identificação: Smith (Malha Aberta)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(
            f'Função de Transferência do Modelo Identificado: G(s) = {k:.4f} * e^(-{theta:.4f} * s) / ({tau:.4f} * s + 1)')
        print(f'Erro Quadrático Médio (EQM): {MSE}')

        response_info = ctrl.step_info(result_estimated_model)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida(tr): {response_info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação(ts): {response_info['SettlingTime']:.4f} s")
        print(f"valor de pico: {response_info['Peak']:.4f}")

        # Retornando os resultados
        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'set_point': set_point
        }

    if method == 'Smith' and mesh == 'Closed':
        # 1. Determinar o valor final da saída
        final_value = output[-1]

        # 2. Encontrar os tempos correspondentes a 28,3% e 63,2% do valor final
        y1 = 0.283 * final_value
        y2 = 0.632 * final_value

        # Encontrar t1 e t2 nos dados
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 3. Calcular τ e θ usando o Método de Smith
        tau = 1.5 * (t2 - t1)
        theta = t2 - tau

        # 4. Calcular o ganho k
        step_amp = step.mean()  # Amplitude do degrau de input
        k = (final_value - output[0]) / step_amp
        set_point = step_amp

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def identifed_model(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            H_s = ctrl.feedback(G_s, 1)
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(H_s, pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        result_estimated_model = identifed_model(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        MSE = np.sqrt(np.sum((result_model - step) ** 2) / len(step))

        # Exibir os resultados
        print(f'Método de Identificação: Smith (Malha Fechada)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(f'Erro Quadrático Médio (EQM): {MSE}')

        response_info = ctrl.step_info(result_estimated_model)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida(tr): {response_info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação(ts): {response_info['SettlingTime']:.4f} s")
        print(f"valor de pico: {response_info['Peak']:.4f}")

        # Retornando os resultados
        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'set_point': set_point
        }

    if method == 'Sundaresan' and mesh == 'Opened':

        # 1. Determinar o valor final da saída
        final = output[-1]

        # 2. Encontrar os tempos correspondentes a 35,3% e 85,3% do valor final
        y1 = 0.353 * final
        y2 = 0.853 * final

        # Encontrar t1 e t2 nos dados
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 3. Calcular τ e θ usando o Método de Sundaresan
        tau = (2/3) * (t2 - t1)
        theta = (1.3*t1) - (0.29*t2)

        # 4. Calcular o ganho k
        step_amp = step.mean()  # Amplitude do degrau de entrada
        k = (final - output[0]) / step_amp
        set_point = step_amp

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def identified_model(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(G_s, pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        result_estimated_model = identified_model(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        MSE = np.sqrt(np.sum((result_model - output) ** 2) / len(output))
        
        # Exibir os resultados
        print(f'Método de Identificação: Sundaresan (Malha Aberta)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(
            f'Função de Transferência do Modelo Identificado: G(s) = {k:.4f} * e^(-{theta:.4f} * s) / ({tau:.4f} * s + 1)')
        print(f'Erro Quadrático Médio (EQM): {MSE}')

        response_info = ctrl.step_info(result_estimated_model)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida: {response_info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação: {response_info['SettlingTime']:.4f} s")

        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'set_point': set_point
        }

    if method == 'Sundaresan' and mesh == 'Closed':
        # 1. Determinar o valor final da saída
        final = output[-1]

        # 2. Encontrar os tempos correspondentes a 35,3% e 85,3% do valor final
        y1 = 0.353 * final
        y2 = 0.853 * final

        # Encontrar t1 e t2 nos dados
        t1 = time[np.where(output >= y1)[0][0]]
        t2 = time[np.where(output >= y2)[0][0]]

        # 3. Calcular τ e θ usando o Método de Sundaresan
        tau = (2 / 3) * (t2 - t1)
        theta = (1.3 * t1) - (0.29 * t2)

        # 4. Calcular o ganho k
        step_amp = step.mean()  # Amplitude do degrau de entrada
        k = (final - output[0]) / step_amp
        set_point = step_amp

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def identified_model(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            H_s = ctrl.feedback(G_s, 1)
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(H_s, pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        result_estimated_model = identified_model(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        result_time, result_model = ctrl.step_response(result_estimated_model * step_amp, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        MSE = np.sqrt(np.sum((result_model - output) ** 2) / len(output))

        # Exibir os resultados
        print(f'Método de Identificação: Sundaresan (Malha Fechada)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(
            f'Função de Transferência do Modelo Identificado: G(s) = {k:.4f} * e^(-{theta:.4f} * s) / ({tau:.4f} * s + 1)')
        print(f'Erro Quadrático Médio (EQM): {MSE}')

        response_info = ctrl.step_info(result_estimated_model)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida: {response_info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação: {response_info['SettlingTime']:.4f} s")

        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'MSE': MSE,
            'result_estimated_model': result_estimated_model,
            'result_time': result_time,
            'result_model': result_model,
            'response_info': response_info,
            'set_point': set_point
        }
