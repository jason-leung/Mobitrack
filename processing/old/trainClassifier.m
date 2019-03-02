function [ Mdl ] = trainClassifier(currentSVMOptions, trainingData, trainingDataLabels)
% A function that interprets the selected classifier options and trains a
% classifier using the provided input data. This function is used by the 2
% class and 3 class hierarchical workflow. 
%
% Parameters: 
%   currentSVMOptions: a struct containing the parameters the SVM
%                      classifier Mdl is to have.
%   trainingData: an n by m matrix where each row is one observation to be
%                 used to train the classifier. There should be no class
%                 labels in this matrix.
%   trainingDataLabels: an n by 1 vector containing the class labels that
%                       correspond to each row of the trainingData matrix.
%
% Returns:
%   Mdl: the trained SVM classifier 
%


    rng(1) % Set the seed to 1 to get the same results each time a particular set of parameters is selected
    
    % Need to check if the kernel type is polynomial because attempting to
    % set a PolynomialOrder for a non-polynomial kernel will cause an error.
    if(strcmp(char(currentSVMOptions.kernel), 'polynomial'))
        Mdl = fitcsvm(trainingData, trainingDataLabels, 'KernelScale', currentSVMOptions.kernelScale, 'Standardize', currentSVMOptions.standardize,...
                        'BoxConstraint', currentSVMOptions.boxConstraint, 'Solver', currentSVMOptions.solver, ...
                        'KernelFunction', currentSVMOptions.kernel, 'PolynomialOrder', currentSVMOptions.polynomialOrder);

    else
         Mdl = fitcsvm(trainingData, trainingDataLabels, 'KernelScale', currentSVMOptions.kernelScale, 'Standardize', currentSVMOptions.standardize,...
                        'BoxConstraint', currentSVMOptions.boxConstraint, 'Solver', currentSVMOptions.solver, ...
                        'KernelFunction', currentSVMOptions.kernel);

    end
end

