close all, clear all, clc
% Load data
%cd ('C:\Users\andre\OneDrive\School\4A\BME 461\Mobitrack\data\Nov17');
filename = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\Nov17\RA_flx_full.mat';
data = load(filename);

% Load Classifier
classifier = load('classifier_simple.mat');
SVMModel = classifier.SVMModel;

dataMatrix = [data.ax; data.ay; data.az; data.gx; data.gy; data.gz];
time = data.time;

processor = DataProcessor(SVMModel, 10);

for i = 1:length(time)
    processor.processStep(dataMatrix(:,i), time(i));
    
    if(processor.repDetected)
        fprintf('Andrea');
    end
    
end


%%
figure, hold on
plot(time, processor.pitchSinceLastSegment * 180.0 / pi), title('Real-time processing pitch')

