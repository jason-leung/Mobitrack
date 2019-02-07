close all, clear all, clc

%% Read txt files
prefix = 'C:\Users\Jason\Desktop\Mobitrack\data\Jan25\';
% filename = 'data_jan25_la_flexion'
% filename = 'data_jan25_la_flexion_02'
filename = 'data_ll_exercise_01'
ext = '.txt';
file = strcat(prefix,filename,ext);
data = csvread(file, 1, 0);

%%
ax = data(:,2)';
ay = data(:,3)';
az = data(:,4)';
gx = data(:,5)';
gy = data(:,6)';
gz = data(:,7)';
time = (data(:,1)' - data(1,1)') / 1000;

%%
save(filename,'ax','ay','az','gx','gy','gz','time');