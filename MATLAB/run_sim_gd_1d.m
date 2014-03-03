% Variables and parameters: 

% Matrices: normalized between 0 and 1 for simplicity
% N: matrix of nutrient concentrations (rows: system, cols: time)
% P: performance matrix (rows: system, cols: time)

% Other parameters:
% n: number of systems
% t: current "round" (time period). Each system shares the same clock
% t_end: last round of simulation

% Note: all vectors are row vectors

% Functions:
% vector suggest(matrix N, matrix P, vector T_start, scalar t_early)
% matrix similarity(matrix N, matrix T,...
%                       vector T_start, scalar t_early, scalar t) 
% scalar cosine_simil(vector v, vector w)
% vector calc_performance(matrix T, matrix N, vector T_start, ...
%                            scalar t_early, scalar t)

% Initialize 
t_end = 100;
n = 100;         % Number of systems
k = 15;          % Max number of clusters
L = 0.01;         % Lipschitz constant for P w.r.t N. 
                  % i.e., maximum dP/dN. 
                  % Continually updated when bigger dP/dN arise
eta = L/sqrt(t_end);          % Learning rate
N = zeros(n,t_end);
P = zeros(n,t_end);
N_start_mean = .5;
N_start_sig = .5;
debug = 0;
random_perf = 0;
colors_raw = linspace(0,1,floor(k/2))';
colors = zeros(k,3);
colors(1:size(colors_raw),1) = colors_raw;
colors(size(colors_raw)-floor(k/4):2*size(colors_raw)-floor(k/4)-1,2) = colors_raw;
colors(k-size(colors_raw)+1:k,3) = colors_raw;
% Random mean and s.d. for calculating performance
mu = rand();
sig = rand();

for i=1:n
     N(i,1) = N_start_mean+N_start_sig*randn();
     P(i,1) = calc_performance_1d(N(i,:),1,mu,sig);
end

for t=2:t_end
   % Cluster systems by mean temperature and current nute dosage
       [C,IX] = sort(clusterdata(N(:,t-1),'maxclust',k,'linkage','median'));
       num_cluster = max(C);
       Gradient_approx = zeros(1,n); % approx of dP/dN based on regression
       Y_intercepts = zeros(1,n);
       j = 1;
       % Loop through clusters and approximate dP/dN for each via polyfit
       for i=1:num_cluster
           % First find all the systems belonging to current cluster
           cluster_begin = j;
           while j <= n && C(j) == i
               j = j+1;
           end
           cluster_end = j-1;
           % Now fill Gradient_approx by finding best fit line among
           % cluster points and taking dP/dN of this plane 
           %("slope w.r.t N")
           if cluster_end-cluster_begin>1 % Cannot approx grad. with <2 datapoints
               % Find system indices for current cluster
               cluster_indices = IX(cluster_begin:cluster_end);
               % Calc grad approx. for current cluster
               coeffs = polyfit(N(cluster_indices,t-1),...
                        P(cluster_indices,t-1),1);
               grad = coeffs(1);
               y_intercept = coeffs(2);
               % Plot this cluster
               scatter(N(cluster_indices,t-1), P(cluster_indices,t-1),10,colors(i,:))
               xlim([0 1]);
               ylim([0 1]);
               xlabel('Nutrient Dosage');
               ylabel('Performance');
                % SHOULD USE REPMAT HERE BUT FUCK ITx
               hold on;
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
                Y_intercepts(cluster_indices) = ...
                    zeros(1,cluster_end-cluster_begin+1)+ y_intercept;
                % Update Lipschitz constant/learning rate if needed
               if grad > L
                   L = grad;
                   eta = L/(sqrt(t_end));
               end
           end
       end
       drawnow
       hold off
   % Add some covariance matrix perturbation
   if random_perf
      sig = sig*(1+sig_sig*randn(1,1));
   end
   % Loop through systems to perform dosage and performance updates
   for i=1:n
       N(i,t) = N(i,t-1)+eta*Gradient_approx(i);
       P(i,t) = calc_performance_1d(N(i,:),t,mu,sig);
   end
end
