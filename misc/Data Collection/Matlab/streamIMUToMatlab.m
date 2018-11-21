close all, clear all, clc

%% Data Collection
secondsToCollect = 10;

if ~isempty(instrfind) fclose(instrfind); delete(instrfind); end
arduino = serial('COM9','BaudRate',115200); 
fopen(arduino);
time = [];
data = [];
collect = true;
timeStamp = 0;

ax = [];
ay = [];
az = [];
gx = [];
gy = [];
gz = [];

% Read in loop values
disp('Data capture Start.')
tic
while collect
    data_temp = fscanf(arduino, '%d,%d,%d,%d,%d,%d');

    if (numel(data_temp) ~= 6)
        disp('fail to match format')

        continue
    end
    
    ax = [ax, data_temp(1)];
    ay = [ay, data_temp(2)];
    az = [az, data_temp(3)];
    gx = [gx, data_temp(4)];
    gy = [gy, data_temp(5)];
    gz = [gz, data_temp(6)];
    
    timeStamp = toc
        time = [time timeStamp];
        if timeStamp >= secondsToCollect 
            collect = false;
            break           
        end
end
   
% Close comport
fclose(arduino);    
disp('Data capture complete.')
