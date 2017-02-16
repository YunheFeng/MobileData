clear;
clc;
close;

addpath('C:/export_fig/');
M = dlmread('app_overlap.csv');
app = M(:, 1:5).'
figure('position', [100, 100, 800, 600])
i = 4
plot(app(:, i + 4), '-d', ...
    'LineWidth',2,...
    'MarkerSize',10)
hold on;
plot(app(:,i + 1), '-o', ...
    'LineWidth',2,...
    'MarkerSize',10)
plot(app(:,i + 2), '-*', ...
    'LineWidth',2,...
    'MarkerSize',10)
plot(app(:,i + 3), '-+', ...
    'LineWidth',2,...
    'MarkerSize',10)
hold off;
ylabel('Avg. number of concurrent apps');
xlabel('Speed range (km/h)');
speed = {'0-20', '20-40', '40-60', '60-80', '80-100'};
set(gca, 'XTick', 1:5, 'XTickLabel', speed, 'FontSize',22)
legend('All Cities', 'City A','City B','City C')

set(gcf, 'Color', 'w');
export_fig app_overlap_8_6.pdf





