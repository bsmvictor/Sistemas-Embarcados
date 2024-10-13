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
        amplitude_degrau = step.mean()  # Amplitude do degrau de entrada
        k = (final_value - output[0]) / amplitude_degrau

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def modelo_identificado(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            Pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(G_s, Pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        resposta_modelo = modelo_identificado(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        t_sim, y_modelo = ctrl.step_response(resposta_modelo * amplitude_degrau, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        EQM = np.sqrt(np.sum((y_modelo - output) ** 2) / len(output))
          
        # Exibir os resultados
        print(f'Método de Identificação: Smith (Malha Aberta)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(
            f'Função de Transferência do Modelo Identificado: G(s) = {k:.4f} * e^(-{theta:.4f} * s) / ({tau:.4f} * s + 1)')
        print(f'Erro Quadrático Médio (EQM): {EQM}')

        info = ctrl.step_info(resposta_modelo)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida(tr): {info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação(ts): {info['SettlingTime']:.4f} s")
        print(f"valor de pico: {info['Peak']:.4f}")

        # Retornando os resultados
        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'EQM': EQM,
            'resposta_modelo': resposta_modelo,
            't_sim': t_sim,
            'y_modelo': y_modelo,
            'info': info,
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
        amplitude_degrau = step.mean()  # Amplitude do degrau de input
        k = (final_value - output[0]) / amplitude_degrau

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def modelo_identificado(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            H_s = ctrl.feedback(G_s, 1)
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            Pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(H_s, Pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        resposta_modelo = modelo_identificado(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        t_sim, y_modelo = ctrl.step_response(resposta_modelo * amplitude_degrau, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        EQM = np.sqrt(np.sum((y_modelo - step) ** 2) / len(step))

        # Exibir os resultados
        print(f'Método de Identificação: Smith (Malha Fechada)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(f'Erro Quadrático Médio (EQM): {EQM}')

        info = ctrl.step_info(resposta_modelo)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida(tr): {info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação(ts): {info['SettlingTime']:.4f} s")
        print(f"valor de pico: {info['Peak']:.4f}")

        # Retornando os resultados
        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'EQM': EQM,
            'resposta_modelo': resposta_modelo,
            't_sim': t_sim,
            'y_modelo': y_modelo,
            'info': info,
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
        amplitude_degrau = step.mean()  # Amplitude do degrau de entrada
        k = (final - output[0]) / amplitude_degrau

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def modelo_identificado(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            Pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(G_s, Pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        resposta_modelo = modelo_identificado(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        t_sim, y_modelo = ctrl.step_response(resposta_modelo*amplitude_degrau, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        EQM = np.sqrt(np.sum((y_modelo - output) ** 2) / len(output))
        
        # Exibir os resultados
        print(f'Método de Identificação: Sundaresan (Malha Aberta)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(
            f'Função de Transferência do Modelo Identificado: G(s) = {k:.4f} * e^(-{theta:.4f} * s) / ({tau:.4f} * s + 1)')
        print(f'Erro Quadrático Médio (EQM): {EQM}')

        info = ctrl.step_info(resposta_modelo)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida: {info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação: {info['SettlingTime']:.4f} s")

        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'EQM': EQM,
            'resposta_modelo': resposta_modelo,
            't_sim': t_sim,
            'y_modelo': y_modelo,
            'info': info,
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
        amplitude_degrau = step.mean()  # Amplitude do degrau de entrada
        k = (final - output[0]) / amplitude_degrau

        # 5. Modelo Identificado usando a Função de Transferência
        # Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
        def modelo_identificado(k, tau, theta):
            # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
            G_s = ctrl.tf([k], [tau, 1])
            H_s = ctrl.feedback(G_s, 1)
            # Aproximação de Pade para o atraso
            num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
            Pade_approx = ctrl.tf(num_pade, den_pade)
            # Função de transferência com atraso
            return ctrl.series(H_s, Pade_approx)

        # 6. Calcular a resposta estimada usando o modelo
        resposta_modelo = modelo_identificado(k, tau, theta)

        # 7. Simular a resposta ao degrau do modelo identificado
        t_sim, y_modelo = ctrl.step_response(resposta_modelo * amplitude_degrau, T=time)

        # 8. Cálculo do Erro Quadrático Médio (EQM)
        EQM = np.sqrt(np.sum((y_modelo - output) ** 2) / len(output))

        # Exibir os resultados
        print(f'Método de Identificação: Sundaresan (Malha Fechada)')
        print(f'Parâmetros Identificados:')
        print(f'Ganho (k): {k:.4f}')
        print(f'Tempo de Atraso (θ): {theta:.4f} s')
        print(f'Constante de Tempo (τ): {tau:.4f} s')
        print(
            f'Função de Transferência do Modelo Identificado: G(s) = {k:.4f} * e^(-{theta:.4f} * s) / ({tau:.4f} * s + 1)')
        print(f'Erro Quadrático Médio (EQM): {EQM}')

        info = ctrl.step_info(resposta_modelo)
        # Exibir o tempo de subida e o tempo de acomodação
        print(f"Tempo de subida: {info['RiseTime']:.4f} s")
        print(f"Tempo de acomodação: {info['SettlingTime']:.4f} s")

        return {
            'k': k,
            'theta': theta,
            'tau': tau,
            'EQM': EQM,
            'resposta_modelo': resposta_modelo,
            't_sim': t_sim,
            'y_modelo': y_modelo,
            'info': info,
        }