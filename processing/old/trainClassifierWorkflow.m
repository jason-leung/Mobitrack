close all, clear all, clc

saveTrainingData = 1;
baseFolderPath = 'D:\OneDrive\School\4A\BME 461\Mobitrack';
%cd(baseFolderPath);

data_directory = 'data\TrainingData';
training_filename = 'training_nov17.20-0 striated';
testing_filename = 'testing_nov17.20-0 striated';
classifier_filename = 'classifier_simple_2.mat';
classifier_save_path = strcat(baseFolderPath, filesep, 'processing', filesep, 'classifiers');
trainingSet_save_path = strcat(baseFolderPath, filesep, 'processing', filesep, 'trainingData');
testingSet_save_path = strcat(baseFolderPath, filesep, 'processing', filesep, 'trainingData');
path_to_data = strcat(baseFolderPath, filesep, data_directory, filesep);

% files = {'RL_knee_flx_full_nov20_1'};
% trainingFiles = {'RA_flx_full', 'LA_flx_full_good', 'RA_flx_small', 'LA_flx_small', 'RA_noise_1', 'LA_noise_1', 'RA_noise_2','LA_noise_2', 'LA_noise_3'};
% testingFiles = {'LA_flx_full_nov20_1', 'LA_flx_full_nov20_2', 'LA_noise_nov20_1', 'LA_noise_nov20_2', 'LA_flx_full_nov20_3'...
% 'RA_noise_1_nov20', 'RA_noise_2_nov20', 'RA_flx_full_nov20_0', 'RA_flx_full_nov20_1', 'RA_flx_full_nov20_2', 'RA_flx_full_nov20_3'};
trainingFiles = {'RA_flx_full', 'LA_flx_full_good', 'RA_flx_small', 'LA_flx_small', 'RA_noise_1', 'LA_noise_1', 'RA_noise_2','LA_noise_2', 'LA_noise_3', ...
'LA_flx_full_nov20_1', 'LA_flx_full_nov20_2', 'LA_noise_nov20_1', 'LA_noise_nov20_2', 'LA_flx_full_nov20_3'...
'RA_noise_1_nov20', 'RA_noise_2_nov20', 'RA_flx_full_nov20_0', 'RA_flx_full_nov20_1', 'RA_flx_full_nov20_2', 'RA_flx_full_nov20_3'};

features = [];
labels = [];

% Load and segment training data
for i = 1:length(trainingFiles)
    file = trainingFiles(i);
    file = file{1};
    data = load(strcat(path_to_data, file, '.mat'));
    
    [t, roll, pitch] = preprocessData(data);

    % Segment
    segment_inds = segmentData(t, roll, pitch);
    segments = extractSegments(t, roll, pitch, segment_inds);

    % Features
    features_from_file = extract_Features(segments);
    
    % Labels
    labels_from_file = csvread(strcat(path_to_data, filesep,file, '_labels.csv'));
    
    labels = [labels; labels_from_file];
    features = [features; features_from_file];
end


%% Train SVM
% SVMModel = fitcsvm(features, labels);

%% Save
% save(strcat(classifier_save_path, filesep, classifier_filename), 'SVMModel')
if(saveTrainingData)
    trainingData = horzcat(labels, features);
    
    features = [];
    labels = [];
    

    try
    % Load and segment testing data
    for i = 1:length(testingFiles)
        file = testingFiles(i);
        file = file{1};
        data = load(strcat(path_to_data, file, '.mat'));

        [t, roll, pitch] = preprocessData(data);

        % Segment
        segment_inds = segmentData(t, roll, pitch, 1);
        segments = extractSegments(t, roll, pitch, segment_inds);

        % Features
        features_from_file = extract_Features(segments);

        % Labels
        labels_from_file = csvread(strcat(path_to_data, filesep,file, '_labels.csv'));

        labels = [labels; labels_from_file];
        features = [features; features_from_file];
    end
        testingData = horzcat(labels, features);

    catch
        testingData = trainingData(2:2:end, :);
        trainingData = trainingData(1:2:end, :);
    end
    

    
    save(strcat(trainingSet_save_path, filesep, training_filename, '.mat'), 'trainingData')
    save(strcat(trainingSet_save_path, filesep, testing_filename, '.mat'), 'testingData')
end


%% Visualize results
% feature_1 = 2;
% feature_2 = 13;
% 
% signal_features = [features(labels>0,feature_1), features(labels>0,feature_2)];
% noise_features = [features(labels<1,feature_1), features(labels<1,feature_2)];
% 
% figure, hold on,
% scatter(signal_features(:,1), signal_features(:,2), 'g');
% scatter(noise_features(:,1), noise_features(:,2), 'r');
% title('Feature Space', 'fontweight', 'bold');
% legend('Exercise', 'Noise');
% xlabel(strcat('Feature ', int2str(feature_1)));
% ylabel(strcat('Feature ', int2str(feature_2)));

% %% Visualize Features -> for 2D visualization
% % Predict scores over the grid
% d = 0.02;
% [x1Grid,x2Grid] = meshgrid(min(features(:,1)):d:max(features(:,1)),...
%     min(features(:,2)):d:max(features(:,2)));
% xGrid = [x1Grid(:),x2Grid(:)];
% [~,scores] = predict(SVMModel,xGrid);
% 
% % Plot the data and the decision boundary
% figure;
% h(1:2) = gscatter(features(:,1),features(:,2),labels,'rb','.');
% hold on
% ezpolar(@(x)1);
% h(3) = plot(features(SVMModel.IsSupportVector,1),features(SVMModel.IsSupportVector,2),'ko');
% contour(x1Grid,x2Grid,reshape(scores(:,2),size(x1Grid)),[0 0],'k');
% legend(h,{'-1','+1','Support Vectors'});
% axis equal
% hold off





