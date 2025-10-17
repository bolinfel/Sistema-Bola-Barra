% ---------------------------------------------------------------
% Script: analyze_RC_noise.m
% Description:
%   Reads multiple sensor CSV files in a folder, analyzes noise frequency
%   via FFT, and computes a suitable RC low-pass filter (R given C).
% ---------------------------------------------------------------

clear; clc; close all;

%% === USER CONFIGURATION ===

dataFolder = 'D:\Users\Bolinfel\Documents\0-PRJ Sistema Bola Barra\Sistema-Bola-Barra\MATLAB\Sensor Test Files';   % <-- change this to your folder
filePattern = fullfile(dataFolder, 'SensorData*.csv');

% --- RC Filter Parameters ---
C_value = 4.7e-6;             % Capacitance in Farads (example: 4.7 uF)
use_attenuation_method = false; % true: use desired attenuation method, false: simple ratio
atten_dB = -20;               % Desired attenuation at main noise frequency (in dB)
rule_of_thumb_ratio = 2;      % Used if attenuation method = false, fc = f_noise / ratio

%% === READ AND ANALYZE FILES ===
files = dir(filePattern);
if isempty(files)
    error('No files found matching pattern "%s"', filePattern);
end

fprintf('Found %d files in folder "%s".\n', numel(files), dataFolder);

for k = 1:numel(files)
    fileName = files(k).name;
    filePath = fullfile(files(k).folder, fileName);
    fprintf('\n=== Processing file: %s ===\n', fileName);

    % --- Load data ---
    data = readtable(filePath);
    if ~all(ismember({'Timestamp', 'Dado'}, data.Properties.VariableNames))
        error('File "%s" missing required columns [Timestamp, Dado]', fileName);
    end

    % --- Parse time and data ---
    t = datetime(data.Timestamp, 'InputFormat', 'yyyy-MM-dd HH:mm:ss.SSSSSS');
    y = data.Dado;

    % --- Compute sampling frequency ---
    dt = seconds(diff(t));
    Ts = mean(dt);          % sample period
    Fs = 1 / Ts;            % sample frequency (Hz)
    N = length(y);

    % --- FFT ---
    Y = fft(y - mean(y));   % remove DC offset
    f = (0:N-1) * (Fs / N);
    P2 = abs(Y / N);
    P1 = P2(1:floor(N/2)+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f = f(1:length(P1));

    % --- Find main noise frequency ---
    [~, idx] = max(P1(2:end));
    mainFreq = f(idx + 1);

    fprintf('Sampling Frequency (Fs): %.2f Hz\n', Fs);
    fprintf('Dominant Noise Frequency: %.2f Hz\n', mainFreq);

    %% === RC FILTER DESIGN ===
    if use_attenuation_method
        A = 10^(atten_dB / 20);  % Convert dB attenuation to linear gain
        if A <= 0 || A >= 1
            error('atten_dB must be negative and produce 0 < A < 1.');
        end
        fc = mainFreq / sqrt((1 / (A^2)) - 1);  % cutoff freq
    else
        fc = mainFreq / rule_of_thumb_ratio;    % simple rule of thumb
    end

    R = 1 / (2 * pi * C_value * fc);  % Ohms

    fprintf('Desired attenuation at f_noise: %.1f dB\n', atten_dB);
    fprintf('Calculated cutoff frequency (fc): %.4f Hz\n', fc);
    fprintf('Chosen capacitance (C): %.3g F\n', C_value);
    fprintf('Recommended resistor (R): %.3g Ω (%.3f kΩ)\n', R, R/1e3);

    % --- Warn if R is impractical ---
    if R > 1e6
        warning('R = %.2f MΩ may be too large (consider increasing C).', R/1e6);
    elseif R < 1e3
        warning('R = %.2f Ω may be too low (check input impedance).', R);
    end

    %% === PLOTS ===
    % Frequency response of RC low-pass
    f_plot = linspace(0, max(5*fc, mainFreq*5), 2000);
    H = 1 ./ sqrt(1 + (f_plot ./ fc).^2);

    figure('Name', fileName, 'NumberTitle', 'off');
    subplot(2,1,1);
    plot(f_plot, 20*log10(H), 'LineWidth', 1.5);
    grid on;
    xlabel('Frequency (Hz)');
    ylabel('Magnitude (dB)');
    title(sprintf('RC Low-Pass Filter Response (fc = %.3f Hz)', fc));
    hold on;
    xline(mainFreq, '--r', sprintf('Noise: %.3f Hz', mainFreq));
    if use_attenuation_method
        yline(atten_dB, '--', sprintf('Target Attenuation: %.1f dB', atten_dB));
    end

    subplot(2,1,2);
    plot(f, P1, 'b', 'LineWidth', 1);
    grid on;
    xlabel('Frequency (Hz)');
    ylabel('|Amplitude|');
    title('Signal Spectrum');
    hold on;
    xline(mainFreq, '--r', sprintf('Noise = %.2f Hz', mainFreq));
    xline(fc, '--g', sprintf('fc = %.2f Hz', fc));
end

disp('All files processed successfully.');
