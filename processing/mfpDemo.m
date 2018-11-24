close all, clear all, clc
ports = instrfind;
if(length(ports) > 0)
    fclose(ports);
end

%% Variables
comPort = 'COM14';
secondsToCollect = 100;

%%
warning('off','all')
dotCount = 0;

%% Initialize Data Processing Variables
% Load Classifier
classifier = load('C:\Users\Jason\Desktop\Mobitrack\processing\classifiers\classifier_nov21.mat');
SVMModel = classifier.SVMModel;
% Set Segmentation Parameters
windowSize = 10;
lag = 1000; % samples
threshold = 0.8; % standard deviations
influence = 1;  
% Initialize Data Processor
processor = DataProcessor(SVMModel, windowSize, lag, threshold, influence);

%% Initialize Data Variables
time = [];
data = [];
ax = [];
ay = [];
az = [];
gx = [];
gy = [];
gz = [];
timeStamp = 0;
collect = true;

%% Serial Connection with Aruino
arSerial = serial(comPort,'BaudRate',115200); 
fopen(arSerial);
pause();

% Start Recording
disp('Start Monitoring');

% Collect data
tic
while collect
    data_temp = fscanf(arSerial, '%d,%d,%d,%d,%d,%d');
    
    if (numel(data_temp) ~= 6)
%         disp('fail to match format')
        continue
    end
    
    ax = [ax, data_temp(1)];
    ay = [ay, data_temp(2)];
    az = [az, data_temp(3)];
    gx = [gx, data_temp(4)];
    gy = [gy, data_temp(5)];
    gz = [gz, data_temp(6)];
    
    timeStamp = toc;
    time = [time timeStamp];
    if timeStamp >= secondsToCollect 
        collect = false;
        break           
    end
    
    processor.processStep([ax(end), ay(end), az(end), gx(end), gy(end), gz(end)]', timeStamp);
    if(processor.repDetected(end))
        fprintf(' ');
        disp('Repetition Detected');
        dotCount = 0;
    else
        if timeStamp > 10
            if(dotCount > 30)
                disp('.');
                dotCount = 0;
            else
                fprintf('.');
            end
            dotCount = dotCount + 1;
        end
    end
end

%%
fclose(arSerial);

% processor.plotResult();


