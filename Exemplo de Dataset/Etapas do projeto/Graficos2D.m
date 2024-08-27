
% Plotagem de Gráficos 2D
clc, clear, close all, fprintf('\n')

% 1a Etapa: definir valores de x.
%eixoX = -2*pi:0.01:2*pi;
eixoX = -3:0.001:3;

% 2a Etapa: Definir a lei de formação da função.
%eixoY = cos(eixoX.*1);
reta = eixoX.*2 + 6;
parabola = eixoX.^2;

%3a Etapa: Plotagem e personalização do gráfico
%plot(eixoX, eixoY, 'r--', 'linewidth', 1.25)
%title({'\itExemplo de plotagem de gráficos 2D'
%    'Gráfico do Cosseno'}, 'fontsize', 14)

figure
plot(eixoX, reta, 'r--', eixoX, parabola, 'm')
legend('y_{1} = 2x + 6', 'y_{2} = x^2')

% Label do eixo x
%xlabel({'Valores de x' '-2\pi \leq x \leq 2\pi'}, 'fontsize', 12)
%xlim([min(eixoX) eixoX(end)])
%xticks(-2*pi:pi/2:2*pi)
%xticklabels({'-2\pi', '-3\pi/2', '-\pi/2', 0, '\pi/2', '\pi', '3\pi/2', '2\pi'})

% Label do eixo y
%ylabel('Amplitude')
%ylim([min(eixoY)*1.1 max(eixoY)*1.1])

% Legenda
%legend('y = cos(x)', 'Location', 'southeast')

% Grade
%grid on

% Exportando como arquivo
%print('-dpng', 'Grafico_Cosseno')



