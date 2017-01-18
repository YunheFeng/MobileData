% figure(1); % number of records
% hist_records = hist(num_records, max(num_records));
% x = [1:max(num_records)];
% scatter(x, hist_records, 'filled');
% 
% set(gca, 'XScale', 'log');
% set(gca, 'YScale', 'log');
% 
% %use large font size because three figures in a row
% set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
% ylabel_hand=ylabel('Number of users');
% xlabel_hand=xlabel('Number of records');
% 
% figure(2); % time interval
% hist_time_interval = hist(time_interval, max(time_interval));
% x = [1:max(time_interval)];
% scatter(x, hist_time_interval, 'filled');
% 
% set(gca, 'XScale', 'log');
% set(gca, 'YScale', 'log');
% 
% % use large font size because three figures in a row
% set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
% ylabel_hand=ylabel('Number of users');
% xlabel_hand=xlabel('Time interval (s)');

figure(3); % visited towers
hist_visited_tower = hist(visited_tower, max(visited_tower));
x = [1:max(visited_tower)];
scatter(x, hist_visited_tower, 'filled');

set(gca, 'XScale', 'log');
set(gca, 'YScale', 'log');

% use large font size because three figures in a row
set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
ylabel_hand=ylabel('Number of users');
xlabel_hand=xlabel('Number of visited towers');