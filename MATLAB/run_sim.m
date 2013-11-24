% Variables and parameters: 

% Matrices: normalized between 0 and 1 for simplicity
% N: matrix of nutrient concentrations (rows: system, cols: time)
% T: temperature matrix (rows: system, cols: time)
% P: performance matrix (rows: system, cols: time)
% W: weighting vectors for current round (rows: systems, cols: systems)

% Other parameters:
% n: number of systems
% t: current "round" (time period). Each system shares the same clock
% t_early: number of rounds constituting early growth phase
% t_end: last round of simulation
% T_start: vector of starting times for the systems
% lambda: temperature weighting factor

% Note: all vectors are row vectors

% Functions:
% vector suggest(matrix N, matrix P, vector T_start, scalar t_early)
% matrix similarity(matrix N, matrix T,...
%                       vector T_start, scalar t_early, scalar t) 
% scalar cosine_simil(vector v, vector w)
% vector calc_performance(matrix T, matrix N, vector T_start, ...
%                            scalar t_early, scalar t)

% Initialize 
t_early = 9; % Really 10 units, but calculations are easier if
            % this parameter is set to 1 less than the number of
            % time periods constituting early growth
t_end = 100;
n = 50;         % Number of systems
lambda = .1;   % Similarity dependence on temperature
Temp_mean = 0.3/0.5*(rand(1,n)-0.5)+0.5; % Temperature means (0.5 +- 0.3)
tau = 0.005;      % Temperature randomness (standard deviation)
alpha = 8/n;    % Performance factor
N = zeros(n,t_end);
T = diag(Temp_mean)*eye(n,t_end); % Fix all temps according to Temp_mean, 
                                 % randomly vary it later
P = zeros(n,t_end);
W = zeros(n);

% Randomly generate starting times (0-10)
T_start = floor((rand(1,n)+1)*10); 

for t=1:t_end
    % For now, will keep all early nutrient dosages constant and 
    % the same for each plant. Later we can use the same machinery
    % as used for later stages of life to learn early life dosages
    n_early_const = 0.5;
    % Get suggestions and similarities
    E = suggest(N,P,T_start,t_early,0,t);
    %S = similarity(N,T,T_start,t_early,t,lambda);
    S = zeros(n)+1; % Similarity measure not working well, ignore for now
    % Calc average performance vector
    % (should change this to incremental update for speed)
    P_avg = zeros(1,n);
    for i=1:n
       if t > T_start(i)
           P_avg(i) = mean(P(i,T_start(i):t-1));
       end
    end
    % Set weight vector
    W = S*diag(P_avg.^alpha);
    % Add some random temperature perturbation
    T(:,t) = Temp_mean'+tau*randn(n,1);
    % Loop through systems to perform dosage and performance updates
    for i=1:n
       if t >= T_start(i)
           if  t <= T_start(i)+t_early
               % Early stage update
               N(i,t) = n_early_const;
           else 
               % Later stage update
               % Set next nutrient dosage using experts update
               N(i,t) = E*W(i,:)';
           end
           P(i,t) = calc_performance(T(i,:),N(i,:),T_start(i),t_early,t,random_perf);
       end
    end
end

%% Plot our results
% Plot scale from 0..1
logScale = histeq(P);
subplot(2,1,1); imagesc(P); xlabel('Performance'); ylabel('Instance Number'); title('Normalized Performance');
colormap(Jet);
colorbar;
% Plot the same graph using histogram equalization
% This expands our dynamic range and will better visualize performance for
% higher values
subplot(2,1,2); imagesc(logScale); xlabel('Performance'); ylabel('Instance Number'); title('Histogram Equalized Performace');
colormap(Jet);
colorbar;
