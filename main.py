import customtkinter as ctk
from tkinter import filedialog, Frame, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.io import loadmat
import numpy as np
from method_smith import method_smith
from method_sundaresan import method_sundaresan
from pid_controller import pid_controller
from sys_identification import system_identification

# Global variables to hold data and results
data = None
comparison_result = None
selected_method = None
selected_control = None
result_closed = None
result_opened = None

# Global variables to hold the selected PID methods
selected_method_1 = 'Nenhum'
selected_method_2 = 'Nenhum'
selected_method_3 = 'Nenhum'

# Variables to hold the input, output, and time data
step = None
output = None
time = None

# Variables for system identification results
identification_smith = None
identification_sundaresan = None

def save_graph(fig, nome_do_arquivo):
    '''
    Saves the given figure as a PNG file.

    Args:
        fig (Figure): The matplotlib figure to save.
        nome_do_arquivo (str): The filename (without extension) to save the figure as.
    '''
    caminho = f'images/{nome_do_arquivo}.png'  # Path to save the figure
    fig.savefig(caminho)  # Save the figure as a PNG file

def select_file():
    '''
    Opens a file dialog to select a .mat file and loads the data for processing.
    '''
    global data
    global step
    global output
    global time

    path_file = filedialog.askopenfilename(title='Selecione o arquivo .mat')  # Open file dialog
    file_name = path_file.split('/')[-1]  # Extract the filename from the path
    if path_file:  # If a file is selected
        data = loadmat(path_file)  # Load the .mat file
        label.configure(text=f"Arquivo {file_name} selecionado com sucesso!")  # Update label with success message

        # Supondo que 'data' seja um dicionário contendo seus dados
        TARGET_DATA____ProjetoC213_Degrau = data['TARGET_DATA____ProjetoC213_Degrau']
        TARGET_DATA____ProjetoC213_PotenciaMotor = data['TARGET_DATA____ProjetoC213_PotenciaMotor']

        # Verifica o formato (linhas, colunas) dos dados
        lines, columns = np.shape(TARGET_DATA____ProjetoC213_Degrau)

        if lines < columns:
            # Caso com mais colunas do que linhas (dados organizados como [2, N])
            time = TARGET_DATA____ProjetoC213_Degrau[0, :]  # Primeira linha é o tempo
            step = TARGET_DATA____ProjetoC213_Degrau[1, :]  # Segunda linha é o degrau (step)
            output = TARGET_DATA____ProjetoC213_PotenciaMotor[1, :]  # Segunda linha da saída (potência)
        else:
            # Caso com mais linhas do que colunas (dados organizados como [N, 2])
            time = TARGET_DATA____ProjetoC213_Degrau[:, 0]  # Primeira coluna é o tempo
            step = TARGET_DATA____ProjetoC213_Degrau[:, 1]  # Segunda coluna é o degrau (step)
            output = TARGET_DATA____ProjetoC213_PotenciaMotor[:, 1]  # Segunda coluna da saída (potência)

        plot_graphs_initial()  # Generate initial graphs for the Smith and Sundaresan methods

def plot_graphs_initial():
    '''
    Plots initial graphs using the identified system parameters for both Smith and Sundaresan methods.
    '''
    global comparison_result
    global identification_smith
    global identification_sundaresan

    global step
    global output
    global time

    if data is not None:  # Check if data is loaded

        # Identify system using Smith and Sundaresan methods
        identification_smith = system_identification(step, time, output, 'Smith')
        identification_sundaresan = system_identification(step, time, output, 'Sundaresan')

        # Compute results for both methods
        results_smith = method_smith(step, time, output,
                                     identification_smith['k'], identification_smith['tau'],
                                     identification_smith['theta'])

        results_sundaresan = method_sundaresan(step, time, output,
                                               identification_sundaresan['k'], identification_sundaresan['tau'],
                                               identification_sundaresan['theta'])
        
        # Graph 1: Smith Method
        fig1 = Figure(figsize=(5.5, 5), dpi=100)  # Create a new figure
        ax1 = fig1.add_subplot(111)  # Add a subplot

        # Plotting the graph
        ax1.plot(time, output, 'g', label='Resposta Real do Sistema')  # Actual system response
        ax1.plot(time, step, label='Entrada (Degrau)', color='blue')  # Step input
        ax1.plot(results_smith['result_time'], results_smith['result_model'], 'r',
                 label='Modelo Identificado (Smith) Malha Aberta')  # Identified model

        # Setting title and axis labels
        ax1.set_title('Método de Smith (Malha Aberta)', fontsize=10)  # Title
        ax1.set_xlabel('Tempo (s)')  # X-axis label
        ax1.set_ylabel('Potência do Motor')  # Y-axis label

        # Show legend and grid
        ax1.legend(loc='lower right', fontsize=8)  # Legend location
        ax1.grid()  # Show grid

        # Adding identified parameters in a box
        props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Box properties

        # Text to display in the box
        textstr = '\n'.join((
            f'Ganho (k): {identification_smith["k"]:.4f}',
            f'Tempo de Atraso (θ): {identification_smith["theta"]:.4f} s',
            f'Constante de Tempo (τ): {identification_smith["tau"]:.4f} s',
            f'(EQM): {results_smith["MSE"]:.4f}'))  # Identified parameters

        # Position the box in the upper right corner
        ax1.text(0.95, 0.5, textstr, transform=ax1.transAxes, fontsize=8,
                 verticalalignment='center', horizontalalignment='right', bbox=props)

        # Graph 2: Sundaresan Method
        fig2 = Figure(figsize=(5.5, 5), dpi=100)  # Create a new figure
        ax2 = fig2.add_subplot(111)  # Add a subplot

        # Plotting the graph
        ax2.plot(time, output, 'g', label='Resposta Real do Sistema')  # Actual system response
        ax2.plot(time, step, label='Entrada (Degrau)', color='blue')  # Step input
        ax2.plot(results_sundaresan['result_time'], results_sundaresan['result_model'], 'r',
                 label='Modelo Identificado (Sundaresan) Malha Aberta')  # Identified model

        # Setting title and axis labels
        ax2.set_title('Método de Sundaresan (Malha Aberta)', fontsize=10)  # Title
        ax2.set_xlabel('Tempo (s)')  # X-axis label
        ax2.set_ylabel('Potência do Motor')  # Y-axis label

        # Show legend and grid
        ax2.legend(loc='lower right', fontsize=8)  # Legend location
        ax2.grid()  # Show grid

        # Adding identified parameters in a box
        props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Box properties

        # Text to display in the box
        textstr = '\n'.join((
            f'Ganho (k): {identification_sundaresan["k"]:.4f}',
            f'Tempo de Atraso (θ): {identification_sundaresan["theta"]:.4f} s',
            f'Constante de Tempo (τ): {identification_sundaresan["tau"]:.4f} s',
            f'(EQM): {results_sundaresan["MSE"]:.4f}'))  # Identified parameters

        # Position the box in the upper right corner
        ax2.text(0.95, 0.5, textstr, transform=ax2.transAxes, fontsize=8,
                 verticalalignment='center', horizontalalignment='right', bbox=props)

        # Clear previous plots
        for widget in frame_plots.winfo_children():
            widget.destroy()  # Remove old widgets from the frame

        # Display the Smith method graph on the left
        canvas1 = FigureCanvasTkAgg(fig1, master=frame_plots)
        canvas1.get_tk_widget().pack(side='left', padx=10)  # Pack left

        # Display the Sundaresan method graph on the right
        canvas2 = FigureCanvasTkAgg(fig2, master=frame_plots)
        canvas2.get_tk_widget().pack(side='right', padx=10)  # Pack right

        # Save the graphs to files
        save_graph(fig1, 'Smith_malha_aberta')  # Save Smith graph
        save_graph(fig2, 'Sundaresan_malha_aberta')  # Save Sundaresan graph

        # Comparing MSE (Mean Squared Error)
        if results_smith['MSE'] < results_sundaresan['MSE']:
            comparison_result = 'Smith'  # Smith is more suitable
            result_label.configure(text='Smith é mais adequado', font=("Arial", 18))
        else:
            comparison_result = 'Sundaresan'  # Sundaresan is more suitable
            result_label.configure(text='Sundaresan é mais adequado', font=("Arial", 18))

        result_label.pack(pady=10)  # Pack the label below the graphs

        plot_graphs_method()  # Call method to plot additional graphs


def plot_graphs_method():
    global comparison_result
    global identification_smith
    global identification_sundaresan
    global result_closed
    global result_opened

    global step
    global output
    global time

    # Check if data and comparison results are available
    if data is not None and comparison_result is not None:


        # Process results based on comparison method
        if comparison_result == 'Smith':
            result_opened = method_smith(
                step, time, output,
                identification_smith['k'], identification_smith['tau'],
                identification_smith['theta'], 'Opened'
            )
            result_closed = method_smith(
                step, time, output,
                identification_smith['k'], identification_smith['tau'],
                identification_smith['theta'], 'Closed'
            )

        if comparison_result == 'Sundaresan':
            result_opened = method_sundaresan(
                step, time, output,
                identification_sundaresan['k'], identification_sundaresan['tau'],
                identification_sundaresan['theta'], 'Opened'
            )
            result_closed = method_sundaresan(
                step, time, output,
                identification_sundaresan['k'], identification_sundaresan['tau'],
                identification_sundaresan['theta'], 'Closed'
            )

        # Create a new figure for the plot
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Plot model results
        ax.plot(result_opened['result_time'], result_opened['result_model'], 'r',
                label=f'Identified Model {comparison_result} Open Loop')
        ax.plot(result_closed['result_time'], result_closed['result_model'], 'b',
                label=f'Identified Model {comparison_result} Closed Loop')

        # Set title and axis labels
        ax.set_title(f'Comparação entre MALHA ABERTA e FECHADA ({comparison_result})', fontsize=10)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Motor Power')

        # Show legend and grid on the plot
        ax.legend(loc='lower right', fontsize=8)
        ax.grid()

        # Add identified parameters to the plot in a bounded box
        props = dict(boxstyle='round', facecolor='white', alpha=0.6)

        # Text with performance information of the methods
        textstr = '\n'.join((
            f'Tempo de subida (Malha Aberta): {result_opened["response_info"]["RiseTime"]:.4f} s',
            f'Tempo de acomodação (Malha Aberta): {result_opened["response_info"]["SettlingTime"]:.4f} s',
            f'Valor final (Pico) (Malha Aberta): {result_opened["response_info"]["Peak"]:.4f}\n',
            f'Tempo de subida (Malha Fechada): {result_closed["response_info"]["RiseTime"]:.4f} s',
            f'Tempo de acomodação (Malha Fechada): {result_closed["response_info"]["SettlingTime"]:.4f} s',
            f'Valor final (Pico) (Malha Fechada): {result_closed["response_info"]["Peak"]:.4f}'
        ))

        # Position the parameter box centrally vertically and to the right horizontally
        ax.text(0.95, 0.5, textstr, transform=ax.transAxes, fontsize=8,
                verticalalignment='center', horizontalalignment='right', bbox=props)

        # Clear previous plots in the plotting area
        for widget in frame_method_plots.winfo_children():
            widget.destroy()

        # Display the Smith method graph in the plotting area
        canvas = FigureCanvasTkAgg(fig, master=frame_method_plots)
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10)

        # Save the generated graph
        save_graph(fig, f'comparacao_aberta_fechada')

        # Create frames for each row of 3 items
        row1 = Frame(frame_method_plots)
        row1.pack(fill="x", pady=5, padx=10)

        row2 = Frame(frame_method_plots)
        row2.pack(fill="x", pady=5, padx=10)

        # Labels for the first row
        rise_time_label = Label(row1, text="...", font=("Arial", 12))
        rise_time_label.pack()

        settling_time_label = Label(row1, text="...", font=("Arial", 12))
        settling_time_label.pack()

        peak_label = Label(row1, text="...", font=("Arial", 12))
        peak_label.pack()

        # Labels for the second row
        eqm_opened_label = Label(row2, text="...", font=("Arial", 12))
        eqm_opened_label.pack(side="top")

        eqm_closed_label = Label(row2, text="...", font=("Arial", 12))
        eqm_closed_label.pack(side="bottom")

        # Update label texts based on results
        if result_opened['response_info']['RiseTime'] < result_closed['response_info']['RiseTime']:
            rise_time_label.configure(text='O sistema em MALHA ABERTA tem menor tempo de subida')
        else:
            rise_time_label.configure(text='O sistema em MALHA FECHADA tem menor tempo de subida')

        if result_opened['response_info']['SettlingTime'] < result_closed['response_info']['SettlingTime']:
            settling_time_label.configure(text='O sistema em MALHA ABERTA tem menor tempo de acomodação')
        else:
            settling_time_label.configure(text='O sistema em MALHA FECHADA tem menor tempo de acomodação')

        if result_opened['response_info']['Peak'] > result_closed['response_info']['Peak']:
            peak_label.configure(text='O sistema em MALHA ABERTA tem maior valor final (pico)')
        else:
            peak_label.configure(text='O sistema em MALHA FECHADA tem maior valor final (pico)')

        # Display MSE results
        eqm_opened_label.configure(text=f'Erro Quadrático Médio (EQM) para MALHA ABERTA: {result_opened["MSE"]:.4f}')
        eqm_closed_label.configure(text=f'Erro Quadrático Médio (EQM) para MALHA FECHADA: {result_closed["MSE"]:.4f}')


def plot_graphs_pid():
    global result_closed
    global result_opened

    # Check if data and result_closed are available
    if data is not None and result_closed is not None:

        first_graph = None
        second_graph = None
        third_graph = None

        # Generate graphs based on the comparison result
        if comparison_result == 'Smith':
            first_graph = pid_controller(
                identification_smith['k'],
                identification_smith['tau'],
                identification_smith['theta'],
                result_opened['result_estimated_model'],
                result_opened['step_amp'],
                selected_method_1
            )

            second_graph = pid_controller(
                identification_smith['k'],
                identification_smith['tau'],
                identification_smith['theta'],
                result_opened['result_estimated_model'],
                result_opened['step_amp'],
                selected_method_2
            )

            third_graph = pid_controller(
                identification_smith['k'],
                identification_smith['tau'],
                identification_smith['theta'],
                result_opened['result_estimated_model'],
                result_opened['step_amp'],
                selected_method_3
            )

        if comparison_result == 'Sundaresan':
            first_graph = pid_controller(
                identification_sundaresan['k'],
                identification_sundaresan['tau'],
                identification_sundaresan['theta'],
                result_opened['result_estimated_model'],
                result_opened['step_amp'],
                selected_method_1
            )

            second_graph = pid_controller(
                identification_sundaresan['k'],
                identification_sundaresan['tau'],
                identification_sundaresan['theta'],
                result_opened['result_estimated_model'],
                result_opened['step_amp'],
                selected_method_2
            )

            third_graph = pid_controller(
                identification_sundaresan['k'],
                identification_sundaresan['tau'],
                identification_sundaresan['theta'],
                result_opened['result_estimated_model'],
                result_opened['step_amp'],
                selected_method_3
            )

        fig1 = Figure(figsize=(3.7, 3.7), dpi=100)
        ax1 = fig1.add_subplot(111)

        # Plot the first graph if it is a valid dictionary
        if isinstance(first_graph, dict):

            ax1.plot(first_graph['result_time'], first_graph['result_model'], 'red', label='PID')
            ax1.axvline(first_graph['response_info']['RiseTime'], color='green', linestyle='--', label='Rise Time')
            ax1.axvline(first_graph['response_info']['SettlingTime'], color='purple', linestyle='--', label='Settling Time')
            ax1.text(first_graph['response_info']['RiseTime'], 0.9 * result_opened['step_amp'],
                     f'Rise Time: {first_graph["response_info"]["RiseTime"]:.2f}s', color='green', fontsize=10)
            ax1.text(first_graph['response_info']['SettlingTime'], 0.8 * result_opened['step_amp'],
                     f'Settling Time: {first_graph["response_info"]["SettlingTime"]:.2f}s', color='purple', fontsize=10)
            ax1.set_title(first_graph['title'], fontsize=10)
            ax1.set_xlabel('Time (s)')
            ax1.set_ylabel('Motor Power')

            ax1.legend(loc='lower right', fontsize=8)
            ax1.grid()

            # Add identified parameters in a bounded box
            props = dict(boxstyle='round', facecolor='white', alpha=0.6)

            textstr = '\n'.join((
                f'Rise time (tr): {first_graph["response_info"]["RiseTime"]:.4f} s',
                f'Settling time (ts): {first_graph["response_info"]["SettlingTime"]:.4f} s',
                f'Peak value: {first_graph["response_info"]["Peak"]:.4f}'
            ))

            ax1.text(0.95, 0.5, textstr, transform=ax1.transAxes, fontsize=8,
                     verticalalignment='center', horizontalalignment='right', bbox=props)

            save_graph(fig1, 'method_1')

        fig2 = Figure(figsize=(3.7, 3.7), dpi=100)
        ax2 = fig2.add_subplot(111)

        # Plot the second graph if it is a valid dictionary
        if isinstance(second_graph, dict):

            ax2.plot(second_graph['result_time'], second_graph['result_model'], 'red', label='PID')
            ax2.axvline(second_graph['response_info']['RiseTime'], color='green', linestyle='--', label='Rise Time')
            ax2.axvline(second_graph['response_info']['SettlingTime'], color='purple', linestyle='--', label='Settling Time')
            ax2.text(second_graph['response_info']['RiseTime'], 0.9 * result_opened['step_amp'],
                     f'Rise Time: {second_graph["response_info"]["RiseTime"]:.2f}s', color='green', fontsize=10)
            ax2.text(second_graph['response_info']['SettlingTime'], 0.8 * result_opened['step_amp'],
                     f'Settling Time: {second_graph["response_info"]["SettlingTime"]:.2f}s', color='purple', fontsize=10)
            ax2.set_title(second_graph['title'], fontsize=10)
            ax2.set_xlabel('Time (s)')
            ax2.set_ylabel('Motor Power')

            ax2.legend(loc='lower right', fontsize=8)
            ax2.grid()

            props = dict(boxstyle='round', facecolor='white', alpha=0.6)

            textstr = '\n'.join((
                f'Rise time (tr): {second_graph["response_info"]["RiseTime"]:.4f} s',
                f'Settling time (ts): {second_graph["response_info"]["SettlingTime"]:.4f} s',
                f'Peak value: {second_graph["response_info"]["Peak"]:.4f}'
            ))

            ax2.text(0.95, 0.5, textstr, transform=ax2.transAxes, fontsize=8,
                     verticalalignment='center', horizontalalignment='right', bbox=props)

            save_graph(fig2, 'method_2')

        fig3 = Figure(figsize=(3.7, 3.7), dpi=100)
        ax3 = fig3.add_subplot(111)

        # Plot the third graph if it is a valid dictionary
        if isinstance(third_graph, dict):

            ax3.plot(third_graph['result_time'], third_graph['result_model'], 'red', label='PID')
            ax3.axvline(third_graph['response_info']['RiseTime'], color='green', linestyle='--', label='Rise Time')
            ax3.axvline(third_graph['response_info']['SettlingTime'], color='purple', linestyle='--', label='Settling Time')
            ax3.text(third_graph['response_info']['RiseTime'], 0.9 * result_opened['step_amp'],
                     f'Rise Time: {third_graph["response_info"]["RiseTime"]:.2f}s', color='green', fontsize=10)
            ax3.text(third_graph['response_info']['SettlingTime'], 0.8 * result_opened['step_amp'],
                     f'Settling Time: {third_graph["response_info"]["SettlingTime"]:.2f}s', color='purple', fontsize=10)
            ax3.set_title(third_graph['title'], fontsize=10)
            ax3.set_xlabel('Time (s)')
            ax3.set_ylabel('Motor Power')

            ax3.legend(loc='lower right', fontsize=8)
            ax3.grid()

            props = dict(boxstyle='round', facecolor='white', alpha=0.6)

            textstr = '\n'.join((
                f'Rise time (tr): {third_graph["response_info"]["RiseTime"]:.4f} s',
                f'Settling time (ts): {third_graph["response_info"]["SettlingTime"]:.4f} s',
                f'Peak value: {third_graph["response_info"]["Peak"]:.4f}'
            ))

            ax3.text(0.95, 0.5, textstr, transform=ax3.transAxes, fontsize=8,
                     verticalalignment='center', horizontalalignment='right', bbox=props)

            save_graph(fig3, 'method_3')

        # Clear previous widgets from the plot area
        for widget in frame_pid_plots.winfo_children():
            widget.destroy()

        # Pack and display the graphs in the PID plot frame
        canvas1 = FigureCanvasTkAgg(fig1, master=frame_pid_plots)
        canvas1.get_tk_widget().pack(side='left', padx=10)

        canvas2 = FigureCanvasTkAgg(fig2, master=frame_pid_plots)
        canvas2.get_tk_widget().pack(side='left', padx=10)

        canvas3 = FigureCanvasTkAgg(fig3, master=frame_pid_plots)
        canvas3.get_tk_widget().pack(side='left', padx=10)


# Function to process the selection of the first PID method
def select_pid_method_1(value):
    global selected_method_1
    selected_method_1 = value
    print(f"PID method selected for the first field: {value}")


# Function to process the selection of the second PID method
def select_pid_method_2(value):
    global selected_method_2
    selected_method_2 = value
    print(f"PID method selected for the second field: {value}")


# Function to process the selection of the third PID method
def select_pid_method_3(value):
    global selected_method_3
    selected_method_3 = value
    print(f"PID method selected for the third field: {value}")


# Function to switch between different screens in the application
def switch_screen(screen):
    frame_initial.pack_forget()
    frame_comparisons.pack_forget()
    frame_pid.pack_forget()
    screen.pack(fill='both', expand=True)


# Configuring the main application window
app = ctk.CTk()
app.geometry('1366x768')
ctk.set_appearance_mode("light")

# Creating the sidebar for navigation
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side='right', fill='y', padx=10)

# Button to switch to the initial screen
button_to_initial = ctk.CTkButton(sidebar, text='Tele inicial', command=lambda: switch_screen(frame_initial))
button_to_initial.pack(pady=10, padx=10)

# Button to switch to the comparisons analysis screen
button_to_comparisons = ctk.CTkButton(sidebar, text='Análise - Método',
                                      command=lambda: switch_screen(frame_comparisons))
button_to_comparisons.pack(pady=10, padx=10)

# Button to switch to the advanced control definition screen
button_to_advanced = ctk.CTkButton(sidebar, text='Definir controle', command=lambda: switch_screen(frame_pid))
button_to_advanced.pack(pady=10, padx=10)

# Creating Frames for different screens
frame_initial = ctk.CTkFrame(app)
frame_comparisons = ctk.CTkFrame(app)
frame_pid = ctk.CTkFrame(app)

# Centralized title at the top of the application
title_label = ctk.CTkLabel(app, text="Identificação de Processos e Sintonia de Controladores PID", font=("Arial", 24))
title_label.pack(side='top', pady=10)

# Initial Screen - Button to select file and display Smith and Sundaresan graphs
arquive_frame = ctk.CTkFrame(frame_initial)
arquive_frame.pack(pady=5, padx=20, fill='x')

# Button for selecting .mat file
button_file = ctk.CTkButton(arquive_frame, text='Selecione um arquivo .mat', command=select_file)
button_file.pack(side='left', padx=10, pady=10)

# Label prompting the user to select the .mat file
label = ctk.CTkLabel(arquive_frame, text='Clique no botão para selecionar um arquivo .mat')
label.pack(side='left', padx=10)

# Frame for plots on the initial screen
frame_plots = ctk.CTkFrame(frame_initial)
frame_plots.pack(fill='both', expand=True, padx=20, pady=5)

# Label to display the result of the comparison
result_label = ctk.CTkLabel(frame_initial, text="")
result_label.pack(side="top", pady=10)  # Positioned below the graphs

# Comparisons Screen - Selection of methods and type of control
frame_method_plots = ctk.CTkFrame(frame_comparisons)
frame_method_plots.pack(fill='both', expand=True, padx=20, pady=20)

# Advanced Control Screen - Selection of control methods
# PID control method options
pid_methods = ["Nenhum","Ziegler Nichols Malha Aberta","IMC","CHR sem Sobrevalor","CHR com Sobrevalor","Cohen e Coon","ITAE"]

# Frame for buttons on the advanced control screen
frame_buttons = ctk.CTkFrame(frame_pid)
frame_buttons.pack(pady=10, padx=5)

# First selection field for PID methods
option_menu_1 = ctk.CTkOptionMenu(frame_buttons, values=pid_methods, command=select_pid_method_1)
option_menu_1.pack(pady=5, padx=5, side='left')

# Second selection field for PID methods
option_menu_2 = ctk.CTkOptionMenu(frame_buttons, values=pid_methods, command=select_pid_method_2)
option_menu_2.pack(pady=5, padx=5, side='left')

# Third selection field for PID methods
option_menu_3 = ctk.CTkOptionMenu(frame_buttons, values=pid_methods, command=select_pid_method_3)
option_menu_3.pack(pady=5, padx=5, side='left')

# Button to generate data and plots based on the selected methods
button_generate_pid = ctk.CTkButton(frame_buttons, text="Generate Data", command=plot_graphs_pid)
button_generate_pid.pack(pady=5, padx=5, side='left')

# Frame for PID plots on the advanced control screen
frame_pid_plots = ctk.CTkFrame(frame_pid)
frame_pid_plots.pack(fill='both', expand=True, padx=20)

# Starting with the initial screen displayed
frame_initial.pack(fill='both', expand=True)

# Starting the application's main event loop
app.mainloop()

