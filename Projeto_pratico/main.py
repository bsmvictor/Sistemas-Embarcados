import customtkinter as ctk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import loadmat
from Projeto_pratico.method_smith import method_smith
from Projeto_pratico.method_sundaresan import method_sundaresan
from Projeto_pratico.pid_controller import pid_controller
from Projeto_pratico.sys_identification import system_identification

data = None
comparison_result = None
selected_method = None
selected_control = None
result_closed = None
result_opened = None
selected_method_1 = 'Nenhum'
selected_method_2 = 'Nenhum'
selected_method_3 = 'Nenhum'

identification_smith = None
identification_sundaresan = None


def save_graph(fig, nome_do_arquivo):
    caminho = f'images/{nome_do_arquivo}.png'  # Define o caminho para salvar
    fig.savefig(caminho)  # Salva o gráfico


def select_file():
    global data
    path_file = filedialog.askopenfilename(title='Selecione o arquivo .mat')
    file_name = path_file.split('/')[-1]
    if path_file:
        data = loadmat(path_file)
        label.configure(text=f"Arquivo {file_name} selecionado com sucesso!")
        plot_graphs_initial()  # Gerar os gráficos dos métodos Smith e Sundaresan


def plot_graphs_initial():
    global comparison_result
    global identification_smith
    global identification_sundaresan

    if data is not None:
        # Extraindo entrada, saída e tempo
        step = data['TARGET_DATA____ProjetoC213_Degrau'][1]  # A segunda linha é a entrada
        output = data['TARGET_DATA____ProjetoC213_PotenciaMotor'][1]  # A segunda linha é a saída
        time = data['TARGET_DATA____ProjetoC213_Degrau'][0]  # A primeira linha é o tempo

        # Lógica de identificação do sistema Smith
        identification_smith = system_identification(step, time, output, 'Smith')
        identification_sundaresan = system_identification(step, time, output, 'Sundaresan')

        results_smith = method_smith(step, time, output,
                                     identification_smith['k'], identification_smith['tau'],
                                     identification_smith['theta'])

        results_sundaresan = method_sundaresan(step, time, output,
                                               identification_sundaresan['k'], identification_sundaresan['tau'],
                                               identification_sundaresan['theta'])

        print(identification_smith)
        print(identification_sundaresan)

        # Gráfico 1: Método de Smith
        fig1 = Figure(figsize=(5.5, 5), dpi=100)
        ax1 = fig1.add_subplot(111)

        # Plots do gráfico
        ax1.plot(time, output, 'g', label='Resposta Real do Sistema')
        ax1.plot(time, step, label='Entrada (Degrau)', color='blue')
        ax1.plot(results_smith['result_time'], results_smith['result_model'], 'r',
                 label='Modelo Identificado (Smith) Malha Aberta')

        # Definindo título e labels dos eixos
        ax1.set_title('Método de Smith (Malha Aberta)', fontsize=10)
        ax1.set_xlabel('Tempo (s)')
        ax1.set_ylabel('Potência do Motor')

        # Exibindo a legenda e grid
        ax1.legend(loc='lower right', fontsize=8)
        ax1.grid()

        # Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
        props = dict(boxstyle='round', facecolor='white', alpha=0.6)

        textstr = '\n'.join((
            f'Ganho (k): {identification_smith["k"]:.4f}',
            f'Tempo de Atraso (θ): {identification_smith["theta"]:.4f} s',
            f'Constante de Tempo (τ): {identification_smith["tau"]:.4f} s',
            f'(EQM): {results_smith["MSE"]:.4f}'))

        # Posicionar a caixa de parâmetros no centro verticalmente e na direita horizontalmente
        ax1.text(0.95, 0.5, textstr, transform=ax1.transAxes, fontsize=8, verticalalignment='center',
                 horizontalalignment='right', bbox=props)

        # Gráfico 2: Método de Sundaresan
        fig2 = Figure(figsize=(5.5, 5), dpi=100)
        ax2 = fig2.add_subplot(111)

        # Plots do gráfico
        ax2.plot(time, output, 'g', label='Resposta Real do Sistema')
        ax2.plot(time, step, label='Entrada (Degrau)', color='blue')
        ax2.plot(results_sundaresan['result_time'], results_sundaresan['result_model'], 'r',
                 label='Modelo Identificado (Sundaresan) Malha Aberta')

        # Definindo título e labels dos eixos
        ax2.set_title('Método de Sundaresan (Malha Aberta)', fontsize=10)
        ax2.set_xlabel('Tempo (s)')
        ax2.set_ylabel('Potência do Motor')

        # Exibindo a legenda e grid
        ax2.legend(loc='lower right', fontsize=8)
        ax2.grid()

        # Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
        props = dict(boxstyle='round', facecolor='white', alpha=0.6)

        textstr = '\n'.join((
            f'Ganho (k): {identification_sundaresan["k"]:.4f}',
            f'Tempo de Atraso (θ): {identification_sundaresan["theta"]:.4f} s',
            f'Constante de Tempo (τ): {identification_sundaresan["tau"]:.4f} s',
            f'(EQM): {results_sundaresan["MSE"]:.4f}'))

        # Posicionar a caixa de parâmetros no centro verticalmente e na direita horizontalmente
        ax2.text(0.95, 0.5, textstr, transform=ax2.transAxes, fontsize=8, verticalalignment='center',
                 horizontalalignment='right', bbox=props)

        # Limpar gráficos anteriores
        for widget in frame_plots.winfo_children():
            widget.destroy()

        # Display gráfico do método de Smith na esquerda
        canvas1 = FigureCanvasTkAgg(fig1, master=frame_plots)
        canvas1.get_tk_widget().pack(side='left', padx=10)

        # Display gráfico do método de Sundaresan na direita
        canvas2 = FigureCanvasTkAgg(fig2, master=frame_plots)
        canvas2.get_tk_widget().pack(side='right', padx=10)

        save_graph(fig1, 'Smith_malha_aberta')
        save_graph(fig2, 'Sundaresan_malha_aberta')

        # Comparação dos EQMs
        if results_smith['MSE'] < results_sundaresan['MSE']:
            comparison_result = 'Smith'
            result_label.configure(text='Smith é mais adequado', font=("Arial", 18))
        else:
            comparison_result = 'Sundaresan'
            result_label.configure(text='Sundaresan é mais adequado', font=("Arial", 18))

        result_label.pack(pady=10)  # Usando pack para posicionar a label abaixo dos gráficos

        plot_graphs_method()


def plot_graphs_method():
    global comparison_result

    global identification_smith
    global identification_sundaresan

    global result_closed
    global result_opened

    if data is not None and comparison_result is not None:

        # Extraindo entrada, saída e tempo
        step = data['TARGET_DATA____ProjetoC213_Degrau'][1]  # A segunda linha é a entrada
        output = data['TARGET_DATA____ProjetoC213_PotenciaMotor'][1]  # A segunda linha é a saída
        time = data['TARGET_DATA____ProjetoC213_Degrau'][0]  # A primeira linha é o tempo

        if comparison_result == 'Smith':
            result_opened = method_smith(step, time, output,
                                         identification_smith['k'], identification_smith['tau'],
                                         identification_smith['theta'], 'Opened')
            result_closed = method_smith(step, time, output,
                                         identification_smith['k'], identification_smith['tau'],
                                         identification_smith['theta'], 'Closed')

        if (comparison_result == 'Sundaresan'):
            result_opened = method_sundaresan(step, time, output,
                                              identification_sundaresan['k'], identification_sundaresan['tau'],
                                              identification_sundaresan['theta'], 'Opened')
            result_closed = method_sundaresan(step, time, output,
                                              identification_sundaresan['k'], identification_sundaresan['tau'],
                                              identification_sundaresan['theta'], 'Closed')

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(result_opened['result_time'], result_opened['result_model'], 'r',
                label=f'Modelo Identificado {comparison_result} Malha Aberta')
        ax.plot(result_closed['result_time'], result_closed['result_model'], 'b',
                label=f'Modelo Identificado {comparison_result} Malha Fechada')

        # Definindo título e labels dos eixos
        ax.set_title(f'Comparação entre Malha Aberta e Fechada ({comparison_result})', fontsize=10)
        ax.set_xlabel('Tempo (s)')
        ax.set_ylabel('Potência do Motor')

        # Exibindo a legenda e grid
        ax.legend(loc='lower right', fontsize=8)
        ax.grid()

        # Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
        props = dict(boxstyle='round', facecolor='white', alpha=0.6)

        textstr = '\n'.join((
            f'Tempo de subida (Malha Aberta): {result_opened['response_info']['RiseTime']:.4f} s',
            f'Tempo de acomodação (Malha Aberta): {result_opened['response_info']['SettlingTime']:.4f} s',
            f'Valor final(pico) (Malha Aberta): {result_opened['response_info']['Peak']:.4f}\n',
            f'Tempo de subida (Malha Fechada): {result_closed['response_info']['RiseTime']:.4f} s',
            f'Tempo de acomodação (Malha Fechada): {result_closed['response_info']['SettlingTime']:.4f} s',
            f'Valor final(pico) (Malha Fechada): {result_closed['response_info']['Peak']:.4f}'))

        # Posicionar a caixa de parâmetros no centro verticalmente e na direita horizontalmente
        ax.text(0.95, 0.5, textstr, transform=ax.transAxes, fontsize=8, verticalalignment='center',
                horizontalalignment='right', bbox=props)

        # Limpar gráficos anteriores
        for widget in frame_method_plots.winfo_children():
            widget.destroy()

        # Display gráfico do método de Smith na esquerda
        canvas = FigureCanvasTkAgg(fig, master=frame_method_plots)
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10)

        save_graph(fig, f'comparacao_aberta_fechada')

        # Comparação entre os sistemas em malha aberta e fechada

        if result_opened['response_info']['RiseTime'] < result_closed['response_info']['RiseTime']:
            rise_time_label.configure(text='O sistema em malha aberta tem menor tempo de subida.', font=("Arial", 16))
        else:
            rise_time_label.configure(text='O sistema em malha fechada tem menor tempo de subida.', font=("Arial", 16))

        if result_opened['response_info']['SettlingTime'] < result_closed['response_info']['SettlingTime']:
            settling_time_label.configure(text='O sistema em malha aberta tem menor tempo de acomodação.',
                                          font=("Arial", 16))
        else:
            settling_time_label.configure(text='O sistema em malha fechada tem menor tempo de acomodação.',
                                          font=("Arial", 16))

        if result_opened['response_info']['Peak'] > result_closed['response_info']['Peak']:
            peak_label.configure(text='O sistema em malha aberta tem maior valor final (pico).', font=("Arial", 16))
        else:
            peak_label.configure(text='O sistema em malha aberta tem maior valor final (pico).', font=("Arial", 16))

        # Exibindo os resultados
        eqm_opened_label.configure(text=f'\nErro Quadrático Médio (EQM) para Malha Aberta: {result_opened['MSE']:.4f}',
                                   font=("Arial", 16))
        eqm_closed_label.configure(text=f'\nErro Quadrático Médio (EQM) para Malha Fechada: {result_closed['MSE']:.4f}',
                                   font=("Arial", 16))


def plot_graphs_pid():
    global result_closed
    global result_opened

    if data is not None and result_closed is not None:

        if comparison_result == 'Smith':
            first_graph = pid_controller(identification_smith['k'], identification_smith['tau'], identification_smith['theta'],
                                         result_opened['result_estimated_model'], result_opened['step_amp'], selected_method_1)

            second_graph = pid_controller(identification_smith['k'], identification_smith['tau'], identification_smith['theta'],
                                          result_opened['result_estimated_model'], result_opened['step_amp'], selected_method_2)

            third_graph = pid_controller(identification_smith['k'], identification_smith['tau'], identification_smith['theta'],
                                         result_opened['result_estimated_model'], result_opened['step_amp'], selected_method_3)

        if comparison_result == 'Sundaresan':
            first_graph = pid_controller(identification_sundaresan['k'], identification_sundaresan['tau'], identification_sundaresan['theta'],
                                         result_opened['result_estimated_model'], result_opened['step_amp'], selected_method_1)

            second_graph = pid_controller(identification_sundaresan['k'], identification_sundaresan['tau'], identification_sundaresan['theta'],
                                          result_opened['result_estimated_model'], result_opened['step_amp'], selected_method_2)

            third_graph = pid_controller(identification_sundaresan['k'], identification_sundaresan['tau'], identification_sundaresan['theta'],
                                         result_opened['result_estimated_model'], result_opened['step_amp'], selected_method_3)


        if isinstance(first_graph, dict):
            # Gráfico 1:
            fig1 = Figure(figsize=(3.7, 3.7), dpi=100)
            ax1 = fig1.add_subplot(111)

            ax1.plot(first_graph['result_time'], first_graph['result_model'], 'red', label='PID')
            ax1.axvline(first_graph['response_info']['RiseTime'], color='green', linestyle='--',
                        label='Tempo de Subida')
            ax1.axvline(first_graph['response_info']['SettlingTime'], color='purple', linestyle='--',
                        label='Tempo de Acomodação')
            ax1.text(first_graph['response_info']['RiseTime'], 0.9 * result_opened['step_amp'],
                     f'Tempo de Subida: {first_graph['response_info']['RiseTime']:.2f}s', color='green', fontsize=10)
            ax1.text(first_graph['response_info']['SettlingTime'], 0.8 * result_opened['step_amp'],
                     f'Tempo de Acomodação: {first_graph['response_info']['SettlingTime']:.2f}s', color='purple',
                     fontsize=10)
            ax1.set_title(first_graph['title'], fontsize=10)
            ax1.set_xlabel('Tempo (s)')
            ax1.set_ylabel('Potência do Motor')

            ax1.legend(loc='lower right', fontsize=8)
            ax1.grid()

            # Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
            props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Estilo da caixa

            textstr = '\n'.join((
                f'Tempo de subida(tr): {first_graph['response_info']['RiseTime']:.4f} s',
                f'Tempo de acomodação(ts): {first_graph['response_info']['SettlingTime']:.4f} s',
                f"valor de pico: {first_graph['response_info']['Peak']:.4f}"))

            # Posicionar a caixa com os resultados no gráfico
            ax1.text(0.95, 0.5, textstr, transform=ax1.transAxes, fontsize=8, verticalalignment='center',
                     horizontalalignment='right', bbox=props)

            save_graph(fig1, 'metodo_1')

        if isinstance(second_graph, dict):
            # Gráfico 2:
            fig2 = Figure(figsize=(3.7, 3.7), dpi=100)
            ax2 = fig2.add_subplot(111)

            ax2.plot(second_graph['result_time'], second_graph['result_model'], 'red', label='PID')
            ax2.axvline(second_graph['response_info']['RiseTime'], color='green', linestyle='--',
                        label='Tempo de Subida')
            ax2.axvline(second_graph['response_info']['SettlingTime'], color='purple', linestyle='--',
                        label='Tempo de Acomodação')
            ax2.text(second_graph['response_info']['RiseTime'], 0.9 * result_opened['step_amp'],
                     f'Tempo de Subida: {second_graph['response_info']['RiseTime']:.2f}s', color='green', fontsize=10)
            ax2.text(second_graph['response_info']['SettlingTime'], 0.8 * result_opened['step_amp'],
                     f'Tempo de Acomodação: {second_graph['response_info']['SettlingTime']:.2f}s', color='purple',
                     fontsize=10)
            ax2.set_title(second_graph['title'], fontsize=10)
            ax2.set_xlabel('Tempo (s)')
            ax2.set_ylabel('Potência do Motor')

            ax2.legend(loc='lower right', fontsize=8)
            ax2.grid()

            # Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
            props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Estilo da caixa

            textstr = '\n'.join((
                f'Tempo de subida(tr): {second_graph['response_info']['RiseTime']:.4f} s',
                f'Tempo de acomodação(ts): {second_graph['response_info']['SettlingTime']:.4f} s',
                f"valor de pico: {second_graph['response_info']['Peak']:.4f}"))

            # Posicionar a caixa com os resultados no gráfico
            ax2.text(0.95, 0.5, textstr, transform=ax2.transAxes, fontsize=8, verticalalignment='center',
                     horizontalalignment='right', bbox=props)

            save_graph(fig2, 'metodo_2')

        if isinstance(third_graph, dict):
            # Gráfico 3:
            fig3 = Figure(figsize=(3.7, 3.7), dpi=100)
            ax3 = fig3.add_subplot(111)

            ax3.plot(third_graph['result_time'], third_graph['result_model'], 'red', label='PID')
            ax3.axvline(third_graph['response_info']['RiseTime'], color='green', linestyle='--',
                        label='Tempo de Subida')
            ax3.axvline(third_graph['response_info']['SettlingTime'], color='purple', linestyle='--',
                        label='Tempo de Acomodação')
            ax3.text(third_graph['response_info']['RiseTime'], 0.9 * result_opened['step_amp'],
                     f'Tempo de Subida: {third_graph['response_info']['RiseTime']:.2f}s', color='green', fontsize=10)
            ax3.text(third_graph['response_info']['SettlingTime'], 0.8 * result_opened['step_amp'],
                     f'Tempo de Acomodação: {third_graph['response_info']['SettlingTime']:.2f}s', color='purple',
                     fontsize=10)
            ax3.set_title(third_graph['title'], fontsize=10)
            ax3.set_xlabel('Tempo (s)')
            ax3.set_ylabel('Potência do Motor')

            ax3.legend(loc='lower right', fontsize=8)
            ax3.grid()

            # Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
            props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Estilo da caixa

            textstr = '\n'.join((
                f'Tempo de subida(tr): {third_graph['response_info']['RiseTime']:.4f} s',
                f'Tempo de acomodação(ts): {third_graph['response_info']['SettlingTime']:.4f} s',
                f"valor de pico: {third_graph['response_info']['Peak']:.4f}"))

            # Posicionar a caixa com os resultados no gráfico
            ax3.text(0.95, 0.5, textstr, transform=ax3.transAxes, fontsize=8, verticalalignment='center',
                     horizontalalignment='right', bbox=props)

            save_graph(fig3, 'metodo_3')

        for widget in frame_pid_plots.winfo_children():
            widget.destroy()

        canvas1 = FigureCanvasTkAgg(fig1, master=frame_pid_plots)
        canvas1.get_tk_widget().pack(side='left', padx=10)

        canvas2 = FigureCanvasTkAgg(fig2, master=frame_pid_plots)
        canvas2.get_tk_widget().pack(side='left', padx=10)

        canvas3 = FigureCanvasTkAgg(fig3, master=frame_pid_plots)
        canvas3.get_tk_widget().pack(side='left', padx=10)




# Função para processar a escolha do método PID
def select_pid_method_1(value):
    global selected_method_1
    selected_method_1 = value
    print(f"Método PID selecionado para o primeiro campo: {value}")


def select_pid_method_2(value):
    global selected_method_2
    selected_method_2 = value
    print(f"Método PID selecionado para o segundo campo: {value}")


def select_pid_method_3(value):
    global selected_method_3
    selected_method_3 = value
    print(f"Método PID selecionado para o terceiro campo: {value}")


def switch_screen(screen):
    frame_initial.pack_forget()
    frame_comparisons.pack_forget()
    frame_pid.pack_forget()
    screen.pack(fill='both', expand=True)


# Configurando interface principal
app = ctk.CTk()
app.geometry('1366x768')
ctk.set_appearance_mode("light")

# Barra lateral de navegação
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side='right', fill='y', padx=10)

button_to_initial = ctk.CTkButton(sidebar, text='Tela Inicial', command=lambda: switch_screen(frame_initial))
button_to_initial.pack(pady=10, padx=10)

button_to_comparisons = ctk.CTkButton(sidebar, text='Análise - Método',
                                      command=lambda: switch_screen(frame_comparisons))
button_to_comparisons.pack(pady=10, padx=10)

button_to_advanced = ctk.CTkButton(sidebar, text='Definir Controle', command=lambda: switch_screen(frame_pid))
button_to_advanced.pack(pady=10, padx=10)

# Criando Frames para diferentes telas
frame_initial = ctk.CTkFrame(app)
frame_comparisons = ctk.CTkFrame(app)
frame_pid = ctk.CTkFrame(app)

# Título centralizado no topo
title_label = ctk.CTkLabel(app, text="Comparação de Métodos de Identificação", font=("Arial", 24))
title_label.pack(side='top', pady=10)

# Tela Inicial - Botão para selecionar arquivo e gráficos Smith e Sundaresan
arquive_frame = ctk.CTkFrame(frame_initial)
arquive_frame.pack(pady=5, padx=20, fill='x')

button_file = ctk.CTkButton(arquive_frame, text='Selecionar arquivo .mat', command=select_file)
button_file.pack(side='left', padx=10, pady=10)

label = ctk.CTkLabel(arquive_frame, text='Clique no botão para selecionar o arquivo .mat')
label.pack(side='left', padx=10)

frame_plots = ctk.CTkFrame(frame_initial)
frame_plots.pack(fill='both', expand=True, padx=20, pady=5)

# Label para exibir o resultado da comparação
result_label = ctk.CTkLabel(frame_initial, text="")
result_label.pack(side="top", pady=10)  # Posicionado abaixo dos gráficos

# Tela de Comparações - Seleção de métodos e tipo de controle
frame_method_plots = ctk.CTkFrame(frame_comparisons)
frame_method_plots.pack(fill='both', expand=True, padx=20, pady=20)

rise_time_label = ctk.CTkLabel(frame_comparisons)
rise_time_label.pack(side='top')

settling_time_label = ctk.CTkLabel(frame_comparisons)
settling_time_label.pack(side='top')

peak_label = ctk.CTkLabel(frame_comparisons)
peak_label.pack(side='top')

eqm_opened_label = ctk.CTkLabel(frame_comparisons)
eqm_opened_label.pack(side='top')

eqm_closed_label = ctk.CTkLabel(frame_comparisons)
eqm_closed_label.pack(side='top')

# Tela de Controle Avançado - Seleção de métodos de controle
# Opções de métodos de controle PID
pid_methods = ["Nenhum", "Ziegler Nichols Malha Aberta", "IMC", "CHR sem Sobrevalor", "CHR com Sobrevalor",
               "Cohen e Coon", "ITAE"]

frame_buttons = ctk.CTkFrame(frame_pid)
frame_buttons.pack(pady=10, padx=5)

# Primeiro campo de seleção
option_menu_1 = ctk.CTkOptionMenu(frame_buttons, values=pid_methods, command=select_pid_method_1)
option_menu_1.pack(pady=5, padx=5, side='left')

# Segundo campo de seleção
option_menu_2 = ctk.CTkOptionMenu(frame_buttons, values=pid_methods, command=select_pid_method_2)
option_menu_2.pack(pady=5, padx=5, side='left')

# Terceiro campo de seleção
option_menu_3 = ctk.CTkOptionMenu(frame_buttons, values=pid_methods, command=select_pid_method_3)
option_menu_3.pack(pady=5, padx=5, side='left')

# Botão para gerar os dados e gráficos com base na escolha
button_generate_pid = ctk.CTkButton(frame_buttons, text="Gerar dados", command=plot_graphs_pid)
button_generate_pid.pack(pady=5, padx=5, side='left')

frame_pid_plots = ctk.CTkFrame(frame_pid)
frame_pid_plots.pack(fill='both', expand=True, padx=20)

# Iniciando com a tela inicial
frame_initial.pack(fill='both', expand=True)

app.mainloop()
