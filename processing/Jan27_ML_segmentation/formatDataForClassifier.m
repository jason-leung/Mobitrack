function [data] = formatDataForClassifier(pitch, window_size)
data = [];

for data_index = 1:length(pitch)
    if (data_index <= window_size || data_index >= (length(pitch) - window_size))
        continue;
    end    
    data = [data; pitch((data_index - window_size):(data_index + window_size))];
end
end

