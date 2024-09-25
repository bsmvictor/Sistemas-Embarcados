
% ----- Importação de datasets -----

clc, clear

% dentro do subdiretório, abrir todo arquivo com extensão .mat
%listaArquivos = dir([pwd '\Datasets\*.mat']);


listaArquivos = dir(fullfile('..', 'Datasets', '*.mat'));

op = listdlg('ListString', {listaArquivos.name},...
    'SelectionMode', 'single',...
    'PromptString', 'Selecione um dataset:',...
    'Name', 'Importar Dados',...
    'ListSize', [250 25*length({listaArquivos.name})]);

% Salvar caminho  e nome do arquivo de index 1 em uma variável
caminhoArquivo = sprintf('%s\\%s', listaArquivos(1).folder, listaArquivos(op).name);

% Carregando o arquivo
if ~isempty(op)
    load(caminhoArquivo)
    
    % Limpando variáveis n mais utilizadas
    clear('caminhoArquivo', 'nomeArquivo')
    
    [linha, coluna] = size(TARGET_DATA____PrimeiraOr_Degrau);
    
    if linha > coluna %vetor coluna
        tempo = TARGET_DATA____PrimeiraOr_Degrau(:, 1);
        degrau = TARGET_DATA____PrimeiraOr_Degrau(:, 2);
        temperatura = TARGET_DATA____PrimeiraOr_Saida(:, 2);
    else
        tempo = TARGET_DATA____PrimeiraOr_Degrau(1,:);
        degrau = TARGET_DATA____PrimeiraOr_Degrau(2, :);
        temperatura = TARGET_DATA____PrimeiraOr_Saida(2, :);
    end
    
    clear('coluna', 'op', 'listaArquivos')
    
    plot(tempo, degrau, tempo, temperatura)

    title({'\itTrabalho Prático de C213'...
        'Identificação de Sistemas de Controle'}, 'FontSize', 12)
    ylabel('\bfTemperatura [C]')
    xlabel('\bfTime (seconds)')
    
    ylim([0 max(max(temperatura), max(degrau))*1.1])    
    grid on
    
    
    %tempInit = temperatura(1);
   % temperatura = temperatura - tempInit
    
    %tempFinal = temperatura(end);
    
    
    
else
    fprintf('Nenhum arquivo selecionado\n')
end




