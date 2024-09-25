
function identificacao = IdentificacaoSistemas(Step, Time, Output, Method)
  % IdentificacaoSistemas identifies control systems using the Smith or Sundaresan methods based on test data, 
  % considering a first-order model with transport delay.
  %
  % identificacao = IdentificacaoSistemas(Step, Time, Output, Method) performs system identification based on 
  % the step response with amplitude Step and the output samples Output over the sampling times Time. 
  % The default method is Smith.
  %
  % Inputs:
  %   - Step   (scalar) Amplitude of the input step. Must be a finite, non-zero number.
  %   - Time   (array)  Sampling time points of the process. Must be non-empty.
  %   - Output (array)  Output samples of the process at the given sampling times. Must be non-empty.
  %   - Method (str)    Identification method to be used: 'Smith' (default) or 'Sundaresan'. Must be a valid string.
  %
  % Output:
  %   - identificacao (map) Structure containing the identified system parameters.
  %
end
