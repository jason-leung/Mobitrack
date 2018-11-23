close all, clear all, clc

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
secondsToCollect = 100;

%% Serial Connection with Aruino
arSerial = serial('COM17','BaudRate',115200); 
fopen(arSerial);
pause();
% Start Recording
% fprintf(arSerial, '1');
fprintf('Start Monitoring');

% Collect data
tic
while collect
    data_temp = fscanf(arSerial, '%d,%d,%d,%d,%d,%d');
    
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
    
    timeStamp = toc;
    time = [time timeStamp];
    if timeStamp >= secondsToCollect 
        collect = false;
        break           
    end
    
    processor.processStep([ax(end), ay(end), az(end), gx(end), gy(end), gz(end)]', timeStamp);
    if(processor.repDetected)
%         fprintf(arSerial, '2');
        fprintf('Repetition Detected');
    end
end

%%
% fprintf(arSerial,'0');
fclose(arSerial);


%%
processor.plotResults();

% figure, hold on
% plot(processor.pitchSinceLastSegment * 180.0 / pi), title('Real-time processing pitch')
% stairs(processor.signals * 5,'r','LineWidth',1.5);
%     for i = 1:size(processor.segmentInds,1)
%         rectangle('Position', [processor.segmentInds(i,1), min(processor.pitchSinceLastSegment), processor.segmentInds(i,2) - processor.segmentInds(i,1), max(processor.pitchSinceLastSegment) - min(processor.pitchSinceLastSegment)], 'EdgeColor', 'r');
%     end
% segments = extractSegments(data.time, processor.rollSinceLastSegment, processor.pitchSinceLastSegment, processor.segmentInds);

