classdef DataProcessor < handle
    
    properties
        allPitch = []; %This stores all the values seen by the class (this cannot be used in final implementation due to memory concerns
        allRoll = [];
        allTime = [];
        
        timeSinceLastSegment = [];
        pitchSinceLastSegment = []; % Note: this is in rad
        rollSinceLastSegment = []; % rad
        
        SVMModel;
        rawData = struct();
        smoothedData = struct(); % for debugging only for now
        smoothingWindowSize;
        
        firstStep;
        repDetected = 0;
    end
    
    methods
        function [obj] = DataProcessor(SVMModel, smoothingWindowSize) % initialize the DataProcessor object
            obj.SVMModel = SVMModel;
            obj.smoothingWindowSize = smoothingWindowSize;
            obj.firstStep = 1;
        end
        
        function [obj] = processStep(obj, data, time)
            % Estimate pitch and roll using the complimentary filter
            obj.getAngles(data, time);
            
            % Segment
            
            % If end of segment, classify
            
            
            obj.firstStep = 0;
            
        end
    end
    
    
    methods (Access = private)
        function [obj] = getAngles(obj, data, time)
            % Change to appropriate units and add data to local rawData struct
            obj.addDataToStruct(data);
            
            % Estimate from accelerometer
            ax = obj.smoothedData.ax(end);
            ay = obj.smoothedData.ay(end);
            az = obj.smoothedData.az(end);
            
            roll_est_acc  = atan2(ay, sqrt(ax .^ 2 + az .^ 2)); % range [-90, 90]
            pitch_est_acc = atan2(ax, sqrt(ay .^ 2 + az .^ 2)); % range [-90, 90]
            
            % Complimentary filter (gyro estimate is computed inside this
            % loop because it relies on the previous angle)
            alpha = 0.1;
            compRollEst = 0; compPitchEst = 0;            
            % Only use acceleration if we are at the first time stamp
            if(obj.firstStep)
                compRollEst = roll_est_acc;
                compPitchEst = pitch_est_acc;
            else
                dt = obj.timeSinceLastSegment(end) - time;
                roll_est_gyr = obj.rollSinceLastSegment(end) + dt * obj.smoothedData.gx(end);
                pitch_est_gyr = obj.pitchSinceLastSegment(end) + dt * obj.smoothedData.gy(end);
                
                compRollEst = (1 - alpha) * roll_est_gyr  + alpha * roll_est_acc;
                compPitchEst = (1 - alpha) * pitch_est_gyr  + alpha * pitch_est_acc;
            end

            obj.rollSinceLastSegment = [obj.rollSinceLastSegment, compRollEst];
            obj.pitchSinceLastSegment = [obj.pitchSinceLastSegment, compPitchEst];
            obj.timeSinceLastSegment = [obj.timeSinceLastSegment, time];
        end
        
        
        
        function [obj] = addDataToStruct(obj, data, time)
            % Convert units and add to the sliding window struct
            g = 9.81; % gravitational constant (m/s^2)
            A_sens = 16384; % for acceleration limit of 2g
            G_sens = 131; % for angular velocity limit of 250 degrees / second
            Ax = data(1) / A_sens * g; Ay = data(2) / A_sens * g; Az = data(3) / A_sens * g; % m/s^2
            Gx = data(4) / G_sens; Gy = data(5) / G_sens; Gz = data(6) / G_sens; % degrees/s
            Gx_rad = Gx * pi / 180.0; Gy_rad = Gy * pi / 180.0; Gz_rad = Gz * pi / 180.0; % rad/s
            
            if(obj.firstStep)
                
                obj.rawData = struct();
                obj.rawData.ax = Ax * ones(1, obj.smoothingWindowSize + 1);
                obj.rawData.ay = Ay * ones(1, obj.smoothingWindowSize + 1);
                obj.rawData.az = Az * ones(1, obj.smoothingWindowSize + 1);
                
                obj.rawData.gx = Gx_rad * ones(1, obj.smoothingWindowSize + 1);
                obj.rawData.gy = Gy_rad * ones(1, obj.smoothingWindowSize + 1);
                obj.rawData.gz = Gz_rad * ones(1, obj.smoothingWindowSize + 1);
                
                obj.smoothedData.ax = [];
                obj.smoothedData.ay = [];
                obj.smoothedData.az = [];
                obj.smoothedData.gx = [];
                obj.smoothedData.gy = [];
                obj.smoothedData.gz = [];
                
            else
                obj.rawData.ax = [obj.rawData.ax(2:end), Ax];
                obj.rawData.ay = [obj.rawData.ay(2:end), Ay];
                obj.rawData.az = [obj.rawData.az(2:end), Az];
                
                obj.rawData.gx = [obj.rawData.gx(2:end), Gx_rad];
                obj.rawData.gy = [obj.rawData.gy(2:end), Gy_rad];
                obj.rawData.gz = [obj.rawData.gz(2:end), Gz_rad];
            end
            
            obj.smoothedData.ax = [obj.smoothedData.ax, mean(obj.rawData.ax(2:end))];
            obj.smoothedData.ay = [obj.smoothedData.ay, mean(obj.rawData.ay(2:end))];
            obj.smoothedData.az = [obj.smoothedData.az, mean(obj.rawData.az(2:end))];
            obj.smoothedData.gx = [obj.smoothedData.gx, mean(obj.rawData.gx(2:end))];
            obj.smoothedData.gy = [obj.smoothedData.gy, mean(obj.rawData.gy(2:end))];
            obj.smoothedData.gz = [obj.smoothedData.gz, mean(obj.rawData.gz(2:end))];
        end
        
    end
    
end
