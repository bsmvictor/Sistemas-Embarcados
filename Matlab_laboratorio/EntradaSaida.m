
% Entrada e saida de dados.
% Receber a np1 e a np2 de um aluno e mostrar a sua media.

clc, clear

qtdAlunos = input('Quantidade de alunos: ');

for aluno = 1:qtdAlunos  %1:1:qtdAlunos
    fprintf('\nSituação do aluno %d:\n', aluno)
    np1 = input('Entre com a np1: ');
    np2 = input('Entre com a np2: ');

    npa = ceil((np1 + np2)/2);

    strnpa = sprintf('Média: %.0f\n\n', npa);
    fprintf('%s',strnpa)

    if npa >= 60, fprintf('O aluno está APROVADO')    
    elseif npa >= 30, fprintf('O aluno está NP3')   
    else, fprintf('O aluno está REPROVADO')     
    end, fprintf('\n------------------------')
end, fprintf('\n')