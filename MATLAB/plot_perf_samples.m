scatter3(Temp_mean(Started_indices),N(Started_indices,t-1),P(Started_indices,t-1),25,clusters,'fill');
xlabel('Temperature');
ylabel('Nutrients');
zlabel('Performance');

% Sometimes we get outliers, so don't let this ruin our visuals
nuteMax = mean(N(Started_indices,t-1)) + 2*std(N(Started_indices,t-1));
axis([0.3 0.7 0 nuteMax 0 1]);

normalizedStep = ((t/t_end) * 3 * pi) - (pi);
azimuth = 10*sin(normalizedStep) - 90;
view([azimuth 20]);

avgPerf = mean(P(Started_indices,t-1));
patch([0.3 0.7 0.7 0.3 ], [0 0 nuteMax nuteMax], [avgPerf avgPerf avgPerf avgPerf], 'b', 'FaceAlpha', 0.2, 'EdgeAlpha', 0.5);

set(gcf,'position',[100 100 1100 650]);
    
if movie
   frame = getframe(f);
   writeVideo(writer, frame);
end