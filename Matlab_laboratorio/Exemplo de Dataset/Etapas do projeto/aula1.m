clc
clear all
fprintf('\nDigite as notas do aluno x\n');
np1 = input(' Entre com a a primeira nota do aluno: ');
np2 = input(' Entre com a a segunda nota do aluno: ');

np1 = (np1 + np2)/2;

% fazer cometario

%f - apresenta numero decimal
%d - apresenta numeros inteiros
%e - numero em notação cientifica
%c ou %s - apresenta caracteres

if np1 >= 60
    fprintf('Aprovado!\n')
    
elseif (np1 >=30 && np1 < 60)
        fprintf('NP3\n')
        
elseif (np1 < 30 && np1 >= 0)
        fprintf('Reprovado!\n')

else
    fprintf('erro'\n)
        

fprintf('%.2f é a media do aluno',np1);