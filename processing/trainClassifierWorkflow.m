close all, clear all, clc

saveTrainingData = 1;
baseFolderPath = 'D:\OneDrive\School\4A\BME 461\Mobitrack';
cd(baseFolderPath);

data_directory = 'data\Nov17';
training_filename = 'training';
testing_filename = 'testing';
classifier_save_path = strcat(baseFolderPath, filesep, 'processing', filesep, 'classifiers');
trainingSet_save_path = strcat(baseFolderPath, filesep, 'processing', filesep, 'trainingData');
testingSet_save_path = strcat(baseFolderPath, filesep, 'processing', filesep, 'trainingData');
path_to_data = strcat(baseFolderPath, filesep, data_directory, filesep);

files = {'RA_flx_full', 'LA_flx_full_good', 'RA_flx_small', 'LA_flx_small', 'RA_noise_1', 'LA_noise_1', 'RA_noise_2','LA_noise_2', 'LA_noise_3'};
features = [];
labels = [];

% Load and segment data
for i = 1:length(files)
    file = files(i);
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
SVMModel = fitcsvm(features, labels);

%% Save
save(strcat(classifier_save_path, filesep,'classifier_simple.mat'), 'SVMModel')
if(saveTrainingData)
    trainingData = horzcat(labels, features);
    testingData = trainingData;
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





