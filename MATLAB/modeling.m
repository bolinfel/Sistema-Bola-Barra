%   Toolboxes Used:
%       Symbolic Math Toolbox

%define constants
fs = 50;
massaBola = 0.006;
raioBola = 0.0046;
gravidade = 9.8051;
haste = 0.0050;
barra = 0.0248;
momentoInercia = 2/5 * massaBola * raioBola^2;

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

num = K * [1];
den = [1 0 0];

% Discretização pelo método bilinear (Tustin)
[numd, dend] = bilinear(num, den, fs);

% Criar a função de transferência discreta
Hd = tf(numd, dend, 1/fs);

% Mostrar o resultado
disp('Função de Transferência Discretizada (Tustin):');
Hd