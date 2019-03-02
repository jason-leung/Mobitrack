%% Load in the feature data
trainingFeaturesFile =  "~/Documents/MATLAB/Version_10_Refactor/features/trainFeatures.txt";

% Load in the csv - ignore the first line which contains the feature headings
trainingData = dlmread(trainingFeaturesFile, ',', 1, 0);
trainingData = dlmread(trainingFeaturesFile, ',');

trainingData = trainingData(:,1:end);

testingFeaturesFile = "~/Documents/MATLAB/Version_10_Refactor/features/testFeatures.txt";
testingData = readFeatureData(testingFeaturesFile, true);
testingData = testingData(:,1:end);


%% Load in the supplementary information

% Load the label matrices and RGB images for visualizing results
load('/home/asabo/Documents/MATLAB/Version_10_Refactor/LargeWatershedControl/labelMatrix.mat');
supplementaryInfo.testLabelMatrix = labelMatrix;
load('/home/asabo/Documents/MATLAB/Version_10_Refactor/TMA_Section2_40x/labelMatrix.mat');
supplementaryInfo.trainLabelMatrix = labelMatrix;


load('/home/asabo/Documents/MATLAB/Version_10_Refactor/LargeWatershedControl/RGBimage.mat');
load('/home/asabo/Documents/MATLAB/Version_10_Refactor/TMA_Section2_40x/RGBimage.mat');
supplementaryInfo.testRGBimage = testRGBimage;
supplementaryInfo.trainRGBimage = trainRGBimage;

% Set the location where the results should be saved
filepaths.root = '/home/asabo/Documents/MATLAB/';
subFolder1 = 'ClassifierResults/';
subFolder2 = 'AllFeatures_comprehensiveTest';

filepaths.testRoot = strcat(filepaths.root, subFolder1);
filepaths.full = strcat(filepaths.testRoot, subFolder2);

supplementaryInfo.filepaths = filepaths;
supplementaryInfo.outputCSV = strcat(filepaths.full, '/', 'classifier_metric.txt'); % Where the metrics will be exported


% Create the directory where the results will be saved
createDirectories(filepaths, 0);

% Load the full label features for the testing dataset

testingData_full = readFeatureData(testingFeaturesFile, false);
supplementaryInfo.testingData_full = testingData_full(:,1:end);

supplementaryInfo.generatePlots = 0;

%% Set up testing parameters - key-value pairs from https://www.mathworks.com/help/stats/fitcsvm.html
svmOptions.standardize = {true, false};
svmOptions.kernel = {'rbf', 'linear', 'polynomial'};
svmOptions.polynomialOrder = {2, 3, 4};

svmOptions.solver = {'ISDA', 'SMO'};
svmOptions.kernelScale = {1, 'auto'}; % TODO: test different kernel scales 
svmOptions.boxConstraint = {1, 10, 100, 500, 1000, 1500, 2000, 5000, 10000}; % 1 is Matlab default

% Current best performer
% svmOptions.standardize = {true};
% svmOptions.kernel = {'linear'};
% svmOptions.polynomialOrder = {2};
% 
% svmOptions.solver = {'ISDA'};
% svmOptions.kernelScale = {'auto'};  % or 1
% svmOptions.boxConstraint = {1000}; % 1 is Matlab default



%% Run the tests
tic
runClassificationTests(svmOptions, trainingData, testingData, supplementaryInfo);
toc