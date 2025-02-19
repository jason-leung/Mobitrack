%%
close all, clear all, clc

%% Load data
cd ('C:\Users\Jason\Desktop\Mobitrack\data\Nov16');
filename = 'RA_continuous_comp';

data = load(strcat(filename, '.mat'));
t = data.t;
roll = data.roll_est_comp;
pitch = data.pitch_est_comp;

% Differentiate
roll_dot = diff(roll) ./ diff(t);
pitch_dot = diff(pitch) ./ diff(t);

dt = diff(t);
fc = 0.5; % cutoff frequency [Hz]
fs = 1/mean(dt); % sampling frequency [Hz]

% Butterworth filter
[b,a] = butter(1, fc/(fs/2));
pitch_dot = filter(b,a,pitch_dot);

%% Plot data
figure,
subplot(2,1,1)
plot(t, [roll; pitch])
title('Angles')
legend('Roll','Pitch')
xlabel('Time (s)')
ylabel('Angle (Degrees)')

subplot(2,1,2),
plot(t(2:end), [roll_dot; pitch_dot])
title('Velocity')
legend('Roll','Pitch')
xlabel('Time (s)')
ylabel('Angular Velocity (Degrees / sec)')

%% ZVC approach
window_width = 15;
window_size = 2*window_width + 1;
center_buffer_width = 7;
last_ZVC = 1;
last_ZVC_thresh = 15;
epsilon = 3;
data = pitch_dot;
ZVC = zeros(1,length(t));

for i = window_size:(length(t) - window_width)
    % Check if sufficiently far away from the previous ZVC
    center_idx = i-window_width;
    if (center_idx - last_ZVC < last_ZVC_thresh)
        continue;
    end
    
    % Continue if center is not ZVC
    if( ((data(center_idx-1) > 0) && (data(center_idx+1) > 0)) || ...
            ((data(center_idx-1) < 0) && (data(center_idx+1) < 0)) )
        continue;
    end
    
    % found ZVC, compute mean
    before = data(i-window_size:i-window_width-1-center_buffer_width);
    after  = data(i-window_width+1+center_buffer_width:i);
    before_mean = mean(before);
    after_mean = mean(after);
    if( (before_mean > epsilon) && (after_mean < -epsilon) )
        % falling edge
        ZVC(center_idx) = -1;
        last_ZVC = center_idx;
    elseif ( (before_mean < -epsilon) && (after_mean > epsilon) )
        % rising edge
        ZVC(center_idx) = 1;
        last_ZVC = center_idx;
    end
end

% Plot ZVC
figure, hold on,
plot(t(2:end), pitch(2:end)), plot(t, ZVC .*epsilon)

%% Identify Segments

% "down-up-whatever" pattern

last_event_ind = 1;
last2_event_ind = 1;

segment_inds = [];

for i =1:length(ZVC)
     
   
   if (ZVC(i) == 0)
       continue;
   end
   
   % Check if we match the pattern
   if(ZVC(last2_event_ind) == -1 && ZVC(last_event_ind) == 1)
       segment_inds = [segment_inds; last2_event_ind, i];
   end
   
   last2_event_ind = last_event_ind;
   last_event_ind = i;
   
end

figure, hold on
plot(pitch), plot(ZVC .*epsilon)

for i = 1:length(segment_inds)
    rectangle('Position', [segment_inds(i,1), min(pitch), segment_inds(i,2) - segment_inds(i,1), max(pitch) - min(pitch)], 'EdgeColor', 'r');
end








