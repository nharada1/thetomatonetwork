function [ p ] = calc_performance( T,N,t_start,t_early,t,mu,sig )
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
scale = 1/mvnpdf(mu,mu,sig);

% No bounds checking needed since this is only called when 
% plant has already started growing
%n_early_avg = mean(N(t_start:min(t_start+t_early,t)));
n_early_avg = 0.5;
t_avg = mean(T(t_start:t));
p = scale*mvnpdf([t_avg N(t) n_early_avg],mu,sig);
    

end

