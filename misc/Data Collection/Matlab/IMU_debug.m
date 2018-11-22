close all

% Plot acceleration
figure, hold on, plot(time - time(1), [ax; ay; az])
legend('ax', 'ay', 'az')
title('Acceleration vs. Time')
xlabel('Time (s)')
ylabel('Acceleration')

% Plot gyro
figure, hold on, plot(time - time(1), [gx; gy; gz])
legend('gx', 'gy', 'gz')
title('Gyro vs. Time')
xlabel('Time (s)')
ylabel('Gyro')
