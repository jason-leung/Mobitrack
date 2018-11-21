close all, clear all, clc

%% Load data
cd ('C:\Users\Jason\Desktop\data_1120');
filename = 'LA_flx_full_noisy_2.mat'; % range [-90,0]
% filename = 'LA_noise_1.mat';
% filename = 'RL_ankle_flx_full_1.mat'; % range [0,90]
data = load(filename);

%% Preprocess
[t, roll, pitch] = preprocessData(data);

%% Segmentation Real Time
y = pitch; % data
lag = 1000; % samples
threshold = 0.8; % standard deviations
influence = 1;
[signals,avg,dev] = ThresholdingAlgo(y,lag,threshold,influence);

figure; subplot(2,1,1); hold on;
x = 1:length(y); ix = lag+1:length(y);
area(x(ix),avg(ix)+threshold*dev(ix),'FaceColor',[0.9 0.9 0.9],'EdgeColor','none');
area(x(ix),avg(ix)-threshold*dev(ix),'FaceColor',[1 1 1],'EdgeColor','none');
plot(x(ix),avg(ix),'LineWidth',1,'Color','cyan','LineWidth',1.5);
plot(x(ix),avg(ix)+threshold*dev(ix),'LineWidth',1,'Color','green','LineWidth',1.5);
plot(x(ix),avg(ix)-threshold*dev(ix),'LineWidth',1,'Color','green','LineWidth',1.5);
plot(1:length(y),y,'b');
xlabel('Sample');
ylabel('Angle (degrees)');
subplot(2,1,2);
stairs(signals,'r','LineWidth',1.5); ylim([-1.5 1.5]);
xlabel('Sample');
ylabel('Signals');
