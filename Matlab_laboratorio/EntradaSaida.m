
% Entrada e saida de dados.
% Receber a np1 e a np2 de um aluno e mostrar a sua media.

clc, clear

qtdAlunos = input('Quantidade de alunos: ');

for aluno = 1:qtdAlunos  %1:1:qtdAlunos
    fprintf('\nSitua��o do aluno %d:\n', aluno)
    np1 = input('Entre com a np1: ');
    np2 = input('Entre com a np2: ');

    npa = ceil((np1 + np2)/2);

    strnpa = sprintf('M�dia: %.0f\n\n', npa);
    fprintf('%s',strnpa)

    if npa >= 60, fprintf('O aluno est� APROVADO')    
    elseif npa >= 30, fprintf('O aluno est� NP3')   
    else, fprintf('O aluno est� REPROVADO')     
    end, fprintf('\n------------------------')
end, fprintf('\n')