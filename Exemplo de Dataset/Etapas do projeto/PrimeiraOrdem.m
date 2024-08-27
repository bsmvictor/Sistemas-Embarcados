% se eu nao tiver o inicio 0, vou ter que definir como 0
% 1 - regime transitorio vai para o regime permanente = que começa devagar
% e tende a se estabilizar
% VF = lims?0s ? SP(s) ? H(s) = teorema do valor final
% VF = AK
% ts = tempo de acomodação = 4t
% k = ganho estático
% t = constante de tempo
% Malha aberto = sinal de saida é ele mesmo e o sinal de entrada é ele
% Ele não sabe se tem noção se esta fazendo o serviço correto.
% Malha fechada = Ao comparar o setpoint(SP(s)) com o PV(s) vai ser o
% erro sistema. Se tiver erro = 5, vai agir de uma forma, se for 10,
% de outra. Sempre vai tentar corrigir.
% H1 = malha de controle. H2 = malha de realimentação. Nesse caso, na
% figurinha tem malha de realimentação padrão.
% e = SP(s) - PV(s)
% Modelagem de Função de Transferência do Sistema de Controle:
% sys = tf([num], [den]) numerador e denominador

k = 3; tau = 10;
sys = tf([k], [tau 1]);
sys2 = tf([k], [tau+5 1]);

% Resposta do Impulso:
%figure(1), impulse(sys)
% Resposta ao Degrau unitário e de outras amplitudes:
%figure(2), step(sys)
%figure(3), step(sys*2)

%Definição do valor inicial:
[Amplitudes, Tempo] = step(sys);
Amplitudes = Amplitudes + 5;
%plot(Tempo, Amplitudes)
ylim([0 max(Amplitudes)*1.1])

%Parametros da curva de resposta do sistema
infos_sys = stepinfo(sys);
ts = infos_sys.SettlingTime

% Funcao de transferencia do sistema em malha fechada
[num, den] = tfdata(feedback(sys,1));
num = cell2mat(num); den = cell2mat(den);
%sys_fechada = feedback(sys,1)
sys_fechada = tf(num/den(2), den/den(2))

% comparacao de sistemas e mmalha aberta e malha fechada
figure(4), step(sys, sys_fechada)
legend('aberta', 'fechada')





