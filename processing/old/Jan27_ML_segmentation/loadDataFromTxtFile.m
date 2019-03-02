function [data] = loadDataFromTxtFile(data_file)
    data_raw = csvread(data_file, 1, 0);
    data = struct();
    data.time = data_raw(:,1);
    data.ax = data_raw(:,2);
    data.ay = data_raw(:,3);
    data.az = data_raw(:,4);
    data.gx = data_raw(:,5);
    data.gy = data_raw(:,6);
    data.gz = data_raw(:,7);
end

