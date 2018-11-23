close all, clear all, clc

%% Load in the feature data
trainingFeaturesFile =  'C:\Users\Jason\Desktop\Mobitrack\data\Nov21\training_nov21.mat';
load(trainingFeaturesFile)

% TODO: change these to be different
testingFeaturesFile = 'C:\Users\Jason\Desktop\Mobitrack\data\Nov21\testing_nov21.mat';
load(testingFeaturesFile)

%% Build Classifier
% extract features of interest
trainingDataLabels = trainingData(:,1);
testingDataLabels = testingData(:,1);
trainingData = trainingData(:,[2, 7, 16, 21]+1);
testingData = testingData(:,[2, 7, 16, 21]+1);

% Train SVM
SVMModel = fitcsvm(trainingData, trainingDataLabels, 'KernelScale', 1, 'Standardize', 1,...
                        'BoxConstraint', 100, 'Solver', 'SMO', ...
                        'KernelFunction', 'rbf');
                    
