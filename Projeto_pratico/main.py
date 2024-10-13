import customtkinter as ctk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import loadmat
from Projeto_pratico.identificacao_sistemas import identificacaoSistemas

data = None
comparison_result = None
selected_method = None
selected_control = None

def select_file():
    global data
    path_file = filedialog.askopenfilename(title='Selecione o arquivo .mat')
    if path_file:
        data = loadmat(path_file)
        label.configure(text="Arquivo .mat selecionado com sucesso!")
        plot_graphs_initial()  # Gerar os gráficos dos métodos Smith e Sundaresan

def plot_graphs_initial():
    global comparison_result

    if data is not None:
        # Extraindo entrada, saída e tempo
        step = data['TARGET_DATA____ProjetoC213_Degrau'][1]  # A segunda linha é a entrada
        output = data['TARGET_DATA____ProjetoC213_PotenciaMotor'][1]  # A segunda linha é a saída
        time = data['TARGET_DATA____ProjetoC213_Degrau'][0]  # A primeira linha é o tempo

        # Lógica de identificação do sistema Smith
        results_smith = identificacaoSistemas(step, time, output, 'Smith')
        results_sundaresan = identificacaoSistemas(step, time, output, 'Sundaresan')

        # Gráfico 1: Método de Smith
        fig1 = Figure(figsize=(4, 4), dpi=100)
        ax1 = fig1.add_subplot(111)

        # Plots do gráfico
        ax1.plot(time, output, 'black', label='Resposta Real do Sistema')
        ax1.plot(time, step, label='Entrada (Degrau)', color='blue')
        ax1.plot(results_smith['t_sim'], results_smith['y_modelo'], 'r',
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
            f'Ganho (k): {results_smith["k"]:.4f}',
            f'Tempo de Atraso (θ): {results_smith["theta"]:.4f} s',
            f'Constante de Tempo (τ): {results_smith["tau"]:.4f} s',
            f'(EQM): {results_smith["EQM"]:.4f}'))

        # Posicionar a caixa de parâmetros no centro verticalmente e na direita horizontalmente
        ax1.text(0.95, 0.5, textstr, transform=ax1.transAxes, fontsize=8, verticalalignment='center', horizontalalignment='right', bbox=props)

        # Gráfico 2: Método de Sundaresan
        fig2 = Figure(figsize=(4, 4), dpi=100)
        ax2 = fig2.add_subplot(111)

        # Plots do gráfico
        ax2.plot(time, output, 'black', label='Resposta Real do Sistema')
        ax2.plot(time, step, label='Entrada (Degrau)', color='blue')
        ax2.plot(results_sundaresan['t_sim'], results_sundaresan['y_modelo'], 'r',
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
            f'Ganho (k): {results_sundaresan["k"]:.4f}',
            f'Tempo de Atraso (θ): {results_sundaresan["theta"]:.4f} s',
            f'Constante de Tempo (τ): {results_sundaresan["tau"]:.4f} s',
            f'(EQM): {results_sundaresan["EQM"]:.4f}'))

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

        # Comparação dos EQMs
        if results_smith['EQM'] < results_sundaresan['EQM']:
            comparison_result = 'Smith'
            result_label.configure(text='Smith é mais adequado', font=("Arial", 18))
        else:
            comparison_result = 'Sundaresan'
            result_label.configure(text='Sundaresan é mais adequado', font=("Arial", 18))

        result_label.pack(pady=10)  # Usando pack para posicionar a label abaixo dos gráficos

        plot_graphs_method()

def plot_graphs_method():
    global comparison_result

    if data is not None and comparison_result is not None:
        
        # Extraindo entrada, saída e tempo
        step = data['TARGET_DATA____ProjetoC213_Degrau'][1]  # A segunda linha é a entrada
        output = data['TARGET_DATA____ProjetoC213_PotenciaMotor'][1]  # A segunda linha é a saída
        time = data['TARGET_DATA____ProjetoC213_Degrau'][0]  # A primeira linha é o tempo

        result_opened = identificacaoSistemas(step, time, output, comparison_result, 'Opened')
        result_closed = identificacaoSistemas(step, time, output, comparison_result, 'Closed')

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(result_opened['t_sim'], result_opened['y_modelo'], 'r', label=f'Modelo Identificado {comparison_result} Malha Aberta')
        ax.plot(result_closed['t_sim'], result_closed['y_modelo'], 'b', label=f'Modelo Identificado {comparison_result} Malha Fechada')

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
            f'Tempo de subida (Malha Aberta): {result_opened['info']['RiseTime']:.4f} s',
            f'Tempo de acomodação (Malha Aberta): {result_opened['info']['SettlingTime']:.4f} s',
            f'Valor final(pico) (Malha Aberta): {result_opened['info']['Peak']:.4f}\n',
            f'Tempo de subida (Malha Fechada): {result_closed['info']['RiseTime']:.4f} s',
            f'Tempo de acomodação (Malha Fechada): {result_closed['info']['SettlingTime']:.4f} s',
            f'Valor final(pico) (Malha Fechada): {result_closed['info']['Peak']:.4f}'))

        # Posicionar a caixa de parâmetros no centro verticalmente e na direita horizontalmente
        ax.text(0.95, 0.5, textstr, transform=ax.transAxes, fontsize=8, verticalalignment='center', horizontalalignment='right', bbox=props)

        # Limpar gráficos anteriores
        for widget in frame_method_plots.winfo_children():
            widget.destroy()

        # Display gráfico do método de Smith na esquerda
        canvas = FigureCanvasTkAgg(fig, master=frame_method_plots)
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10)

        # Comparação entre os sistemas em malha aberta e fechada
        print('\nComparação entre Resposta do Sistema em Malha Aberta e Fechada:\n')

        if result_opened['info']['RiseTime'] < result_closed['info']['RiseTime']:
            rise_time_label.configure(text='O sistema em malha aberta tem menor tempo de subida.', font=("Arial", 16))
        else:
            rise_time_label.configure(text='O sistema em malha fechada tem menor tempo de subida.', font=("Arial", 16))

        if result_opened['info']['SettlingTime'] < result_closed['info']['SettlingTime']:
            settling_time_label.configure(text='O sistema em malha aberta tem menor tempo de acomodação.', font=("Arial", 16))
        else:
            settling_time_label.configure(text='O sistema em malha fechada tem menor tempo de acomodação.', font=("Arial", 16))

        if result_opened['info']['Peak'] > result_closed['info']['Peak']:
            peak_label.configure(text='O sistema em malha aberta tem maior valor final (pico).', font=("Arial", 16))
        else:
            peak_label.configure(text='O sistema em malha aberta tem maior valor final (pico).', font=("Arial", 16))

        # Exibindo os resultados
        eqm_opened_label.configure(text=f'\nErro Quadrático Médio (EQM) para Malha Aberta: {result_opened['EQM']:.4f}', font=("Arial", 16))
        eqm_closed_label.configure(text=f'\nErro Quadrático Médio (EQM) para Malha Fechada: {result_closed['EQM']:.4f}', font=("Arial", 16))


def switch_screen(screen):
    frame_initial.pack_forget()
    frame_comparisons.pack_forget()
    frame_advanced.pack_forget()
    screen.pack(fill='both', expand=True)


# Configurando interface principal
app = ctk.CTk()
app.geometry('1000x700')

# Barra lateral de navegação
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side='right', fill='y')

button_to_initial = ctk.CTkButton(sidebar, text='Tela Inicial', command=lambda: switch_screen(frame_initial))
button_to_initial.pack(pady=10)

button_to_comparisons = ctk.CTkButton(sidebar, text='Análise - Método', command=lambda: switch_screen(frame_comparisons))
button_to_comparisons.pack(pady=10)

button_to_advanced = ctk.CTkButton(sidebar, text='Definir Controle', command=lambda: switch_screen(frame_advanced))
button_to_advanced.pack(pady=10)

# Criando Frames para diferentes telas
frame_initial = ctk.CTkFrame(app)
frame_comparisons = ctk.CTkFrame(app)
frame_advanced = ctk.CTkFrame(app)

# Título centralizado no topo
title_label = ctk.CTkLabel(app, text="Comparação de Métodos de Identificação", font=("Arial", 24))
title_label.pack(side='top', pady=10)

# Tela Inicial - Botão para selecionar arquivo e gráficos Smith e Sundaresan
button_file = ctk.CTkButton(frame_initial, text='Selecionar arquivo .mat', command=select_file)
button_file.pack(side='top', anchor='nw', padx=10, pady=10)

label = ctk.CTkLabel(frame_initial, text='Clique no botão para selecionar o arquivo .mat')
label.pack(side='top', anchor='nw', padx=10)

frame_plots = ctk.CTkFrame(frame_initial)
frame_plots.pack(fill='both', expand=True, padx=20, pady=20)

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
label_advanced = ctk.CTkLabel(frame_advanced, text="Escolha o método avançado:")
label_advanced.pack(pady=10)

button_generate = ctk.CTkButton(frame_advanced, text="Gerar Gráfico", command=plot_graphs_initial)
button_generate.pack(pady=20)

button_back = ctk.CTkButton(frame_advanced, text="Voltar", command=lambda: switch_screen(frame_initial))
button_back.pack(pady=10)

# Iniciando com a tela inicial
frame_initial.pack(fill='both', expand=True)

app.mainloop()
