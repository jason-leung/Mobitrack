function [signals,avgFilter,stdFilter] = ThresholdingAlgo(y,lag,threshold,influence)
% Initialise signal results
signals = zeros(length(y),1);

% Initialise filtered series
filteredY = y(1:lag+1);

% Initialise filters
avgFilter(lag+1,1) = mean(y(1:lag+1));
stdFilter(lag+1,1) = std(y(1:lag+1));

% Initialize signal variables
lastSignalEdgeIdx = -1;

% Loop over all datapoints y(lag+2),...,y(t)
for i=lag+2:length(y)
    % If new value is a specified number of deviations away
    if abs(y(i)-avgFilter(i-1)) > threshold*stdFilter(i-1)
        if y(i) > avgFilter(i-1)
            signals(i) = 1; % Positive signal
        else
            signals(i) = -1; % Negative signal
        end
        % Make influence lower
        filteredY(i) = influence*y(i)+(1-influence)*filteredY(i-1);
    else
        % No signal
        signals(i) = 0;
        filteredY(i) = y(i);
    end
    % Adjust the filters
    avgFilter(i) = mean(filteredY(i-lag:i));
    stdFilter(i) = std(filteredY(i-lag:i));
    
    % Fix Signal
%      0 to  1 --> rising edge --> store idx
%      1 to  0 --> falling edge --> fix signal + reset idx
%      0 to -1 --> falling edge --> store idx
%     -1 to  0 --> rising edge --> fix signal + reset idx
%     -1 to  1 --> fix signal + store idx
%      1 to -1 --> fix signal + store idx
    
    if((signals(i-1) == 0) && (signals(i) == 1))
        lastSignalEdgeIdx = i;
    elseif((signals(i-1) == 1) && (signals(i) == 0))
        if(lastSignalEdgeIdx ~= -1)
            for j = lastSignalEdgeIdx:i
                signals(j) = 0;
            end
            signals(round((lastSignalEdgeIdx+i)/2)) = 1;
        end
        lastSignalEdgeIdx = -1;
    elseif((signals(i-1) == 0) && (signals(i) == -1))
        lastSignalEdgeIdx = i;
    elseif((signals(i-1) == -1) && (signals(i) == 0))
        if(lastSignalEdgeIdx ~= -1)
            for j = lastSignalEdgeIdx:i
                signals(j) = 0;
            end
            signals(round((lastSignalEdgeIdx+i)/2)) = -1;
        end
        lastSignalEdgeIdx = -1;
    elseif((signals(i-1) == -1) && (signals(i) == 1))
        if(lastSignalEdgeIdx ~= -1)
            for j = lastSignalEdgeIdx:i
                signals(j) = 0;
            end
            signals(round((lastSignalEdgeIdx+i)/2)) = -1;
        end
        lastSignalEdgeIdx = i;
    elseif((signals(i-1) == 1) && (signals(i) == -1))
        if(lastSignalEdgeIdx ~= -1)
            for j = lastSignalEdgeIdx:i
                signals(j) = 0;
            end
            signals(round((lastSignalEdgeIdx+i)/2)) = 1;
        end
        lastSignalEdgeIdx = i;
    end
end
% Done, now return results
end