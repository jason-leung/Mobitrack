%%
close all, clear all, clc

%% Load data
cd ('C:\Users\Jason\Desktop\Mobitrack\data\Nov16');
% filename = 'roll_test.mat';
filename = 'RA_extended_flx';

% filename = 'yaw_test.mat';
% filename = 'stationary';

data = load(strcat(filename, '.mat'));
t = data.time - data.time(1);
dt = diff(t);
Ax = data.ax; Ay = data.ay; Az = data.az;
Gx = data.gx; Gy = data.gy; Gz = data.gz;

%% Plot FFT
% Fs = 1/mean(dt);
% X = data.ax; L = length(X); Y = fft(X);
% P2 = abs(Y/L); P1 = P2(1:L/2+1);
% P1(2:end-1) = 2*P1(2:end-1);
% f = Fs*(0:(L/2))/L;
% 
% figure, plot(f,P1), title('Single-Sided Amplitude Spectrum of X(t)'),
% xlabel('f (Hz)'), ylabel('|P1(f)|')

%% Pre-processing: remove high frequency component
fc = exp(-1); % normalized frequency
fs = 1/mean(dt); % sampling frequency [Hz]

% Butterworth filter
[b,a] = butter(1, fc/(fs/2));
Ax = filter(b,a,Ax); Ay = filter(b,a,Ay); Az = filter(b,a,Az);
Gx = filter(b,a,Gx); Gy = filter(b,a,Gy); Gz = filter(b,a,Gz);

%% Convert data to proper units
g = 9.81; % gravitational constant (m/s^2)
A_sens = 16384; % for acceleration limit of 2g
G_sens = 131; % for angular velocity limit of 250 degrees / second
Ax = Ax / A_sens * g; Ay = Ay / A_sens * g; Az = Az / A_sens * g; % m/s^2
Gx = Gx / G_sens; Gy = Gy / G_sens; Gz = Gz / G_sens; % degrees/s
Gx_rad = Gx * pi / 180.0; Gy_rad = Gy * pi / 180.0; Gz_rad = Gz * pi / 180.0; % rad/s

%% Plot raw data
% Acceleration
figure, plot(t, [Ax; Ay; Az])
title('Acceleration','fontweight','bold')
legend('x','y','z')
xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');

% Angular Velocity
figure, plot(t, [Gx; Gy; Gz])
title('Angular Velocity','fontweight','bold')
legend('x','y','z')
xlabel('Time (s)');
ylabel('Angular Velocity (degrees/s)');

%% Estimation based on accelerometer or gyroscope only
% roll = X; pitch = Y
epsilon = 0.1; % magnitude threshold from actual g

% Accelerometer only
roll_est_acc  = atan2(Ay, sqrt(Ax .^ 2 + Az .^ 2)); % range [-90, 90]
pitch_est_acc = atan2(Ax, sqrt(Ay .^ 2 + Az .^ 2)); % range [-90, 90]

% Gyroscope only
roll_est_gyr = zeros(1, length(t));
pitch_est_gyr = zeros(1, length(t));
yaw_est_gyr = zeros(1, length(t));
for i = 2:length(t)
   if (abs(sqrt(Ax(i).^2 + Ay(i).^2 + Az(i).^2)- 9.81) < epsilon)
       yaw_est_gyr(i) = yaw_est_gyr(i-1);
       roll_est_gyr(i) = roll_est_gyr(i-1);
       pitch_est_gyr(i) = pitch_est_gyr(i-1);
       fprintf('AA');
   else
       roll_est_gyr(i) = roll_est_gyr(i-1) + dt(i-1) * Gx_rad(i);
       pitch_est_gyr(i) = pitch_est_gyr(i-1) + dt(i-1) * Gy_rad(i);
       yaw_est_gyr(i) = yaw_est_gyr(i-1) + dt(i-1) * Gz_rad(i);
   end
end

%% 3) Complimentary Filter
alpha = 0.1; % parameter to tune (higher alpha = more acceleration, lower alpha = more gyro)

roll_est_comp = zeros(1, length(t));
pitch_est_comp = zeros(1, length(t));
roll_est_gyr_comp = zeros(1, length(t));
pitch_est_gyr_comp = zeros(1, length(t));

for i=2:length(t)
   roll_est_gyr_comp(i)  = roll_est_comp(i-1) + dt(i-1) * Gx_rad(i);
   pitch_est_gyr_comp(i) = pitch_est_comp(i-1) + dt(i-1) * Gy_rad(i);
       
   roll_est_comp(i)  = (1 - alpha) * roll_est_gyr_comp(i)  + alpha * roll_est_acc(i);
   pitch_est_comp(i) = (1 - alpha) * pitch_est_gyr_comp(i) + alpha * pitch_est_acc(i);    
end

%% Convert all estimates to degrees and save
roll_est_acc = roll_est_acc * 180.0 / pi; pitch_est_acc = pitch_est_acc * 180.0 / pi;
roll_est_gyr = roll_est_gyr * 180.0 / pi; pitch_est_gyr = pitch_est_gyr * 180.0 / pi;
yaw_est_gyr = yaw_est_gyr * 180.0 / pi;
roll_est_comp = roll_est_comp * 180.0 / pi; pitch_est_comp = pitch_est_comp * 180.0 / pi;
save (strcat(filename, '_comp.mat'), 't', 'roll_est_comp', 'pitch_est_comp')

%% 4) Kalman Filter
% state variables X = [roll roll_bias pitch pitch_bias]'
% A = [1 -dt 0 0; 0 1 0 0; 0 0 1 -dt; 0 0 0 1];
% B = [dt 0 0 0; 0 0 dt 0]';
C = [1 0 0 0; 0 0 1 0];
P = eye(4);
Q = eye(4) * 0.01;
R = eye(2) * 10;
state_estimate = [0 0 0 0]';

roll_est_kal  = zeros(1, length(t)); roll_bias_kal  = zeros(1, length(t));
pitch_est_kal = zeros(1, length(t)); pitch_bias_kal = zeros(1, length(t));

for i=2:length(t)
    
    A = [1 -dt(i-1) 0 0; 0 1 0 0; 0 0 1 -dt(i-1); 0 0 0 1];
    B = [dt(i-1) 0 0 0; 0 0 dt(i-1) 0]';
    
    p = Gx_rad(i);
    q = Gy_rad(i);
    r = Gz_rad(i);
   
    phi_hat   = roll_est_kal(i - 1);
    theta_hat = pitch_est_kal(i - 1);
    
    phi_dot   = p + sin(phi_hat) * tan(theta_hat) * q + cos(phi_hat) * tan(theta_hat) * r;
    theta_dot = cos(phi_hat) * q - sin(phi_hat) * r;
          
    % Predict
    state_estimate = A * state_estimate + B * [phi_dot, theta_dot]';
    P = A * P * A' + Q;
    
    % Update
    measurement = [roll_est_acc(i) pitch_est_acc(i)]';
    y_tilde = measurement - C * state_estimate;
    S = R + C * P * C';
    K = P * C' * (S^-1);
    state_estimate = state_estimate + K * y_tilde;
    P = (eye(4) - K * C) * P;
    
    roll_est_kal(i)    = state_estimate(1);
    roll_bias_kal(i)   = state_estimate(2);
    pitch_est_kal(i)  = state_estimate(3);
    pitch_bias_kal(i) = state_estimate(4);
    
end

% Convert all estimates to degrees
% roll_est_kal = roll_est_kal * 180.0 / pi; pitch_est_kal = pitch_est_kal * 180.0 / pi;

%% Plots
figure,
subplot(3, 1, 1);
plot(t, roll_est_comp, t, roll_est_acc, t, roll_est_gyr, t, roll_est_kal)
legend('Complimentary', 'Accelerometer', 'Gyro', 'Kalman')
xlabel('Time (s)')
ylabel('Angle (Degrees)')
title('Roll')

subplot(3, 1, 2);
plot(t, pitch_est_comp, t, pitch_est_acc, t, pitch_est_gyr, t, pitch_est_kal)
legend('Complimentary', 'Accelerometer', 'Gyro', 'Kalman')
xlabel('Time (s)')
ylabel('Angle (Degrees)')
title('Pitch')

subplot(3, 1, 3);
plot(t, yaw_est_gyr)
legend('Gyro')
xlabel('Time (s)')
ylabel('Angle (Degrees)')
title('Yaw')
