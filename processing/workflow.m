close all, clear all, clc

%% Load data
cd ('C:\Users\andre\OneDrive\School\4A\BME 461\Mobitrack\data\Nov17');
filename = 'LA_noise_1.mat';
data = load(filename);

%% Preprocess
[t, roll, pitch] = preprocessData(data);

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

