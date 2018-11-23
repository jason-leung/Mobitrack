close all, clear all, clc

%% Load data
filename = 'C:\Users\Jason\Desktop\Mobitrack\data\Nov21\RA_flx_full_1.mat';
% filename = 'C:\Users\Jason\Desktop\Mobitrack\data\Nov21\RA_noise_4.mat';
filename = 'C:\Users\Jason\Desktop\Mobitrack\data\Nov22\RA_mixed_1.mat';
data = load(filename);

% Load Classifier
classifier = load('C:\Users\Jason\Desktop\Mobitrack\processing\classifiers\classifier_nov21.mat');
SVMModel = classifier.SVMModel;

dataMatrix = [data.ax; data.ay; data.az; data.gx; data.gy; data.gz];
time = data.time;

windowSize = 10;
lag = 1000; % samples
threshold = 0.8; % standard deviations
influence = 1;

processor = DataProcessor(SVMModel, windowSize, lag, threshold, influence);

for i = 1:length(time)
    processor.processStep(dataMatrix(:,i), time(i));
    
    if(processor.repDetected)
        fprintf(strcat('REP DETECTED at ', int2str(i), '\n'));
    end
    
end


%%
processor.plotResult();

