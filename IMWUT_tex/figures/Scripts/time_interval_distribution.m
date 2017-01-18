h1 = cdfplot(C020); hold on; 
h2 = cdfplot(C040); hold on; 
h3 = cdfplot(C060); hold on; 
h4 = cdfplot(C080); hold on; 
h5 = cdfplot(C100);

set(h1, 'LineWidth', 2);
set(h2, 'LineWidth', 2);
set(h3, 'LineWidth', 2);
set(h4, 'LineWidth', 2);
set(h5, 'LineWidth', 2);
set(gca, 'XScale', 'log');

legend('0-20 km/h', '20-40 km/h', '40-60 km/h', '60-80 km/h', 'above 80 km/h');
set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
ylabel_hand=ylabel('Cumulative distribution');
xlabel_hand=xlabel('Time interval(s)');
