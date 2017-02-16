clear;
clc;
close;

addpath('C:/export_fig/');
M = dlmread('average_app_category_per_min.csv');
app_category = M(:, 1:5).'
app_category = app_category.*60
figure('position', [100, 100, 800, 600])
plot(app_category(:,4), '-d', ...
    'LineWidth',2,...
    'MarkerSize',10)
hold on;
plot(app_category(:,1), '-o', ...
    'LineWidth',2,...
    'MarkerSize',10)
plot(app_category(:,2), '-*', ...
    'LineWidth',2,...
    'MarkerSize',10)
plot(app_category(:,3), '-+', ...
    'LineWidth',2,...
    'MarkerSize',10)
hold off;
ylabel('Avg. no. of unique app cat. per min');
xlabel('Speed range (km/h)');
speed = {'0-20', '20-40', '40-60', '60-80', '80-100'};
set(gca, 'XTick', 1:5, 'XTickLabel', speed, 'FontSize',22)
legend('All Cities', 'City A','City B','City C')

set(gcf, 'Color', 'w');
export_fig app_category_per_min_8_6.pdf




% clear;
% clc;
% close;

% addpath('C:/export_fig/');
% M = dlmread('average_app_category_per_min.csv');
% app_category = M(:, 1:5).'
% app_category = app_category.*60
% figure('position', [100, 100, 1700*0.7, 600*0.7])
% plot(app_category(:,4), '-d', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% hold on;
% plot(app_category(:,1), '-o', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% plot(app_category(:,2), '-*', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% plot(app_category(:,3), '-+', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% hold off;
% ylabel('Average no. of unique app categories (app/min)');
% xlabel('Speed range (km/h)');
% speed = {'0-20', '20-40', '40-60', '60-80', '80-100'};
% set(gca, 'XTick', 1:5, 'XTickLabel', speed, 'FontSize',22)
% legend('All Cities', 'City A','City B','City C')

% set(gcf, 'Color', 'w');
% export_fig export_fig app_category_per_min_17_6.pdf






