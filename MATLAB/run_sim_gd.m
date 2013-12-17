clear all;
close all;
clf;
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
n = 10;         % Number of systems
temp_range = 0.3; % Maximum deviation in temperature mean from 0.5
Temp_mean = temp_range*(rand(1,n)-0.5)+0.5; % Temperature means (0.5 +- 0.3)
temp_sig = 0.001;      % Temperature randomness (standard deviation)
sig_sig = 0.1;     % Covariance matrix randomness (standard deviation)
k = n/10;          % Max number of clusters
L = 0.01;         % Lipschitz constant for P w.r.t N. 
                  % i.e., maximum dP/dN. 
                  % Continually updated when bigger dP/dN arise
eta = L/sqrt(t_end);          % Learning rate
N = zeros(n,t_end);
T = diag(Temp_mean)*eye(n,t_end); % Fix an a constant temp of 0.5, randomly 
                      % vary it later
P = zeros(n,t_end);
Started = zeros(1,n); % Keep track of which systems have started

% Random mean and covariance matrix for calculating performance
mu = rand(1,3);
sig = rand_pos_def_mtx();

% Randomly generate starting times (0-10)
T_start = floor((rand(1,n)+1)*10); 

% Random changes in covariance (bool)
random_perf = 0;

% Enable debug output (bool)
debug = 0;

% Save as a movie
movie = 1;

if movie
    f = figure();
    a = axes('Parent',f);
    axis(a,'tight');
    set(a,'nextplot','replacechildren');
    % SICK BUG ALERT - Matlab's OpenGL rendering has issues creating
    % renderings with transparency objects in them when the host is using
    % transparent windows also (lookin at you windows 7). This means to
    % render the movie you MUST DISABLE TRANSPARENCY IN WINDOWS. You've
    % been warned.

    
    writer = VideoWriter('videos/Performance100.avi');
    set(writer, 'FrameRate', 5);
    open(writer);
end

for t=1:t_end
   % For now, will keep all early nutrient dosages constant and 
   % the same for each plant. Later we can use the same machinery
   % as used for later stages of life to learn early life dosages
   n_early_const = 0.5;
   % Cluster systems by mean temperature and current nute dosage
   Started_indices = find(Started);
   num_started = numel(Started_indices);
   if t > 1 && num_started>1
       clusters = clusterdata([Temp_mean(Started_indices)' N(Started_indices,t-1)],k);
       [C,IX] = sort(clusters);
       num_cluster = max(C);
       Gradient_approx = zeros(1,n); % approx of dP/dN based on regression
       j = 1;
       % Loop through clusters and approximate dP/dN for each via polyfit
       for i=1:num_cluster
           % First find all the systems belonging to current cluster
           cluster_begin = i;
           while j < num_started && C(j) == i
               j = j+1;
           end
           cluster_end = j-1;
           % Now fill Gradient_approx by finding best fit plane among
           % cluster points and taking dP/dN of this plane 
           %("slope w.r.t N")
           if cluster_end-cluster_begin>5 % Cannot approx grad. with <5 datapoints
               % Find system indices for current cluster
               cluster_indices = Started_indices(IX(cluster_begin:cluster_end));                                        
               % Calc grad approx. for current cluster
               coeffs = ...
                 coeffvalues(fit([Temp_mean(cluster_indices)' N(cluster_indices,t-1)],...
                        P(cluster_indices,t-1),'poly11'));
               grad = coeffs(3);%/coeffs(1);
               if debug
                   disp('Cluster:');
                   disp(i);
                   disp('Coeffs:');
                   disp(coeffs);
               end
               if isnan(grad) || isinf(grad)
                   disp('Gradient NaN or inf');
                   return;
               end
               Gradient_approx(cluster_indices) = ...
                    zeros(1,cluster_end-cluster_begin+1)+ grad;
                % Update Lipschitz constant/learning rate if needed
               if grad > L
                   L = grad;
                   eta = L/(sqrt(t_end));
               end
           end
       end
       plot_perf_samples
   end
   % Add some random temperature perturbation
   T(:,t) = Temp_mean'+temp_sig*randn(n,1);
   % Add some covariance matrix perturbation
   if random_perf
      sig = sig*(1+sig_sig*randn(1,1));
   end
   % Loop through systems to perform dosage and performance updates
   for i=1:n
       if t >= T_start(i)
           if Started(i)==0
               Started(i)=1;
           end
           if  t <= T_start(i)+t_early
               % Early stage update
               N(i,t) = rand(1,1);
           else 
               % Later stage update
               N(i,t) = max(N(i,t-1)+eta*Gradient_approx(i),0);
           end
           P(i,t) = calc_performance(T(i,:),N(i,:),T_start(i),t_early,t,mu,sig);
       end
   end
end

if movie
    close(writer);
end

disp('Sim complete');