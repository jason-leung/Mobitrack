clear all

%% Load in the feature data
trainingFeaturesFile =  'D:\OneDrive\School\4A\BME 461\Mobitrack\processing\trainingData\training.mat';
load(trainingFeaturesFile)

% TODO: change these to be different
testingFeaturesFile = 'D:\OneDrive\School\4A\BME 461\Mobitrack\processing\trainingData\testing.mat';
load(testingFeaturesFile)

% Set the location where the results should be saved
filepaths.root = 'D:\OneDrive\School\4A\BME 461\Mobitrack\';
subFolder1 = 'processing\results\';
subFolder2 = 'testFeatureSet';

% Extract features to train the classifier
% Pitch
% 1 - mean, 2 - std, 3 - skewness, 4 - kurtosis, 5 - max, 6 - min, 7 -
% signal range, 8 - duration, 9 - 25th percentile, 10 - median, 11 - 75th
% percentile, 12 - mean freq, 13 - energy of spectrum, 14 - entropy of
% spectrum

% Roll
% 15 - mean, 16 - std, 17 - skewness, 18 - kurtosis, 19 - max, 20 - min, 21 -
% signal range, 22 - duration, 23 - 25th percentile, 24 - median, 25 - 75th
% percentile, 26 - mean freq, 27 - energy of spectrum, 28 - entropy of
% spectrum

featureSets = {...
               [2, 7, 16, 21], ...  % std, range of both
               [2, 3, 4, 7, 13, 16, 17, 18, 21, 27]
               };

%% Load in the supplementary information

filepaths.testRoot = strcat(filepaths.root, subFolder1);
filepaths.full = strcat(filepaths.testRoot, subFolder2);

supplementaryInfo.filepaths = filepaths;
supplementaryInfo.outputCSV = strcat(filepaths.full, filesep, 'classifier_metric.txt'); % Where the metrics will be exported

% Create the directory where the results will be saved
if(exist(filepaths.full, 'dir') ~= 7)
    mkdir(filepaths.full);
end

%% Set up testing parameters - key-value pairs from https://www.mathworks.com/help/stats/fitcsvm.html
svmOptions.standardize = {true, false};
svmOptions.kernel = {'rbf', 'linear', 'polynomial'};
svmOptions.polynomialOrder = {2, 3, 4};

svmOptions.solver = {'ISDA', 'SMO'};
svmOptions.kernelScale = {1, 'auto'};
svmOptions.boxConstraint = {1, 5, 10, 100, 500, 1000, 1500, 2000, 5000, 10000}; % 1 is Matlab default

svmOptions.featureSets = featureSets;
%% Run the tests
tic
runClassificationTests(svmOptions, trainingData, testingData, supplementaryInfo);
toc

