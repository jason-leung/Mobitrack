close all

% Plot acceleration
figure, hold on, plot(time - time(1), ax),  plot(time - time(1),ay),  plot(time - time(1),az)
legend('ax', 'ay', 'az')
title('Acceleration vs. Time')
xlabel('Time (s)')
ylabel('Acceleration')

% Plot gyro
figure, hold on, plot(time - time(1), gx),  plot(time - time(1), gy),  plot(time - time(1), gz)
legend('gx', 'gy', 'gz')
title('Gyro vs. Time')
xlabel('Time (s)')
ylabel('Gyro')
