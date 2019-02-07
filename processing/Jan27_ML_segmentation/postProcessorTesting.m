close all, clear all, clc

%% Load the model to use
path_to_model = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\Jan28ClassifierResults\short_test\50.000000, rbf_2_auto_1_SMO_500.mat';
window_size = 50;
load(path_to_model)

path_to_data = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\MetaMotion\Jan25_AndreaSOP_Left - Copy2';
cd(path_to_data)
% Load all files
files = dir('data*.txt')
for file_ind = 1:length(files)
    % Load and format raw data
    data_file = files(file_ind).name;
    testing_data = loadDataFromTxtFile(data_file);
    [t, roll, pitch] = preprocessData(testing_data);
    t = t / 1000;
    [pitch_for_classifier] = formatDataForClassifier(pitch, window_size);
    
    %% Label
    labels = predict(mdl, pitch_for_classifier);
    padding = zeros(window_size,1);
    labels = [0; padding; labels; padding];
    %% Post-Process in real-time
    pp = PostProcessor(window_size, 100);

    for i = 1:length(labels)
        label = labels(i);
        pp.step(label);

    end
    all_labels = pp.all_labels;
    segments = pp.segments;
    figure, plot(t, all_labels), hold on, plot(t, pitch, 'LineWidth', 1.5)

    %% Plot and save
    for i = 1:size(segments,1)

        rectangle('Position', [t(segments(i,1)),...
        min(pitch), ...
        t(segments(i,2)) - t(segments(i,1)), ...
        max(pitch) - min(pitch)], 'EdgeColor', 'green');
    end

    set(gcf,'Position',[1 1 2000 1500])

    saveLocation = strcat(data_file, 'out_.png');
    print(saveLocation,'-dpng','-r600')
    close(gcf);
    
end



