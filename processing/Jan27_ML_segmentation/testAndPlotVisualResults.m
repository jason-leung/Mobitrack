function [  ] = testAndPlotVisualResults( fullFilePath, saveName, mdl, dataForVisualization, dataForVisualization_formatted, window_size )

testPredict = predict(mdl, dataForVisualization_formatted);
padding = zeros(window_size,1);
testPredict = [padding; testPredict; padding];
testPredict = testPredict';
x_labels = 1:length(dataForVisualization);


min_pitch = min(dataForVisualization);
max_pitch = max(dataForVisualization);
labels_to_plot = ones(length(x_labels), 1);
labels_to_plot(testPredict == 1) = max_pitch;
labels_to_plot(testPredict == 0) = min_pitch;


figure, plot(x_labels, dataForVisualization, 'LineWidth', 1.5), title('Off-line processing pitch'), hold on,
plot(x_labels, labels_to_plot)
set(gcf,'Position',[1 1 2500 1500])

saveLocation = strcat(fullFilePath, filesep, saveName, '.png');
print(saveLocation,'-dpng','-r600')
close(gcf);
end

