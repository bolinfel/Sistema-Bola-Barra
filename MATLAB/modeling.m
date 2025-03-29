%   Toolboxes Used:
%       Symbolic Math Toolbox

%define constants
massaBola = 0.103;
raioBola = 0.01465;
gravidade = 9.8051;
haste = 0.034;
barra = 0.15425;
momentoInercia = 8.842 * power(10,-6);

%calculate constant
raioBola_sq = raioBola * raioBola;
Knum = (massaBola * gravidade * haste * raioBola_sq);
Kdenum = barra * ((massaBola * raioBola_sq) + momentoInercia);
K = Knum / Kdenum;

% Define Transfer Function H(s) = X(s) / Θ(s)
num = [1];          % Numerator (X(s) coefficient)
den = [1 0 0];      % Denominator (s^2 term from d^2x/dt^2)
H = tf(num, den) * K;

% Display the transfer function
disp('Função de Transferencia:');
H