h1 = cdfplot(rawspeed); hold on; 
h2 = cdfplot(filteredspeed);

set(h1, 'LineWidth', 2);
set(h2, 'LineWidth', 2);
set(gca, 'XScale', 'log');

legend('raw speed estimation', 'filtered speed estimation');
set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
ylabel_hand=ylabel('Cumulative distribution');
xlabel_hand=xlabel('Speed (km/h)');