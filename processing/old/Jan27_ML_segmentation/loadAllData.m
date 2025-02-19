function [pitch_and_labels] = loadAllData(path_to_data)
cd(path_to_data)
% Load all files
files = dir('data*.txt')
pitch_and_labels = struct();
for i = 1:length(files)
    % Load and format raw data
    data_file = files(i).name;
    data = loadDataFromTxtFile(data_file);
    
    % Load labels
    segment_file = strcat('segs_', data_file);
    segs = csvread(segment_file, 1,0);
    labels = zeros(1, length(data.ax));
    
    for j = 1:size(segs, 1)
        labels(segs(j,1):segs(j,2)) = 1;
    end 
    
    [t, roll, pitch] = preprocessData(data);
    
    pitch_and_labels(i).pitch = pitch;
    pitch_and_labels(i).labels = labels;
    
    
%     figure, plot(t, pitch), title('Off-line processing pitch'), hold on,
%     plot(t(labels == 1), pitch(labels == 1), 'k*')
    
end
end

