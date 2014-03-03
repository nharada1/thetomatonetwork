function [ p ] = calc_performance_1d( N,t,mu,sig )
% Return a performance value by "simulating nature"
% N: nutrient concentration vector
% T: temperature vector
% t_start: vector of times where system starts
% t_early: number of rounds constituting early growth phase
% t: current time
% mu: means of Gaussian
% sig: covariance matrix of Gaussians

% A natural way to simulate performance is assume there is an 
% optimal combination of temperature, current nutrient dosage,
% and average early life nutrient dosage, and have performance fall off
% continuously in every direction. We choose a tri-variate gaussian
% distribution with randomized covariance matrix and arbitary mean.

    % Make the optimal performance 1
    scale = 1/normpdf(mu,mu,sig);

    % No bounds checking needed since this is only called when 
    % plant has already started growing
    p = scale*normpdf(N(t),mu,sig);
   
end

