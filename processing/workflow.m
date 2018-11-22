close all, clear all, clc

%% Load data
% cd ('C:\Users\andre\OneDrive\School\4A\BME 461\Mobitrack\data\Nov17');
filename = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\Nov17\RA_flx_full.mat';
data = load(filename);

%% Preprocess
[t, roll, pitch] = preprocessData(data);
figure, 
plot(t, pitch), title('Off-line processing pitch')
%% Segment
createPlots = 1;
segment_inds = segmentData(t, roll, pitch, createPlots);
segments = extractSegments(t, roll, pitch, segment_inds);

%% Features
features = extract_Features(segments);

%% Load Classifier
classifier = load('classifier_simple.mat');
SVMModel = classifier.SVMModel;

%% Predict
predictedLabel = predict(SVMModel, features);

