close all, clear all, clc

%%
original_folder = pwd;
path_to_data = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\MetaMotion\Jan25_AndreaSOP_Left_clean'
path_to_test_data = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\MetaMotion\Jan25_AndreaSOP_Left_clean\testing\data_ankle_35.txt'

pitch_and_labels = loadAllData(path_to_data);
cd(original_folder)


path_to_test_data = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\MetaMotion\Jan25_AndreaSOP_Left_clean\testing\data_ankle_35.txt'
testing_data = loadDataFromTxtFile(path_to_test_data);
[t, roll, dataForVisualization] = preprocessData(testing_data);
%%
window_sizes = {25,30,40,50};
window_sizes = {50,40,30,20,10,5};


for window_size_ind = 1:length(window_sizes)
    window_size = window_sizes{window_size_ind};
    [dataForVisualizationFormatted] = formatDataForClassifier(dataForVisualization, window_size);
    [classifier_data, classifier_labels] = formatDataForTraining(pitch_and_labels, window_size);
    
    testAllClassifierCombos(classifier_data,classifier_labels, window_size, dataForVisualization, dataForVisualizationFormatted);
end

