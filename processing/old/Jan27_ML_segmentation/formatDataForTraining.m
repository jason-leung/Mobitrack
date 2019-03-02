function [data, labels] = formatDataForTraining(pitch_and_labels, window_size)
data = [];
labels = [];

for i = 1:length(pitch_and_labels)
    current_data = pitch_and_labels(i).pitch;
    current_labels = pitch_and_labels(i).labels;
    
    data = [data; formatDataForClassifier(current_data, window_size)];
    labels = [labels, current_labels(window_size+1:end-window_size-1)];
%     for data_index = 1:length(current_data)
%         if (data_index <= window_size || data_index >= (length(current_data) - window_size))
%             continue;
%         end
%         
%         data = [data; current_data((data_index - window_size):(data_index + window_size))];
%         labels = [labels;current_labels(data_index)];
%     end
end
labels = labels';
end

