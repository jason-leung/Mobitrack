path_to_test_data = 'D:\OneDrive\School\4A\BME 461\Mobitrack\data\MetaMotion\Jan25_AndreaSOP_Left_clean\data_ankle_full.txt'
testing_data = loadDataFromTxtFile(path_to_test_data);
[t, roll, dataForVisualization] = preprocessData(testing_data);

figure, plot(dataForVisualization, 'LineWidth', 1.5)