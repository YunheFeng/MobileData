clear;
clc;
close;

addpath('C:/export_fig/');
M = dlmread('switch_frequency_app_category.csv');
app_switch = M(:, 1:5).'
figure('position', [100, 100, 800, 600])
plot(app_switch(:,4), '-d', ...
    'LineWidth',2,...
    'MarkerSize',10)
hold on;
plot(app_switch(:,1), '-o', ...
    'LineWidth',2,...
    'MarkerSize',10)
plot(app_switch(:,2), '-*', ...
    'LineWidth',2,...
    'MarkerSize',10)
plot(app_switch(:,3), '-+', ...
    'LineWidth',2,...
    'MarkerSize',10)
hold off;
ylabel('App category switch frequency');
xlabel('Speed range (km/h)');
speed = {'0-20', '20-40', '40-60', '60-80', '80-100'};
set(gca, 'XTick', 1:5, 'XTickLabel', speed, 'FontSize',22)
legend('All Cities', 'City A','City B','City C')

set(gcf, 'Color', 'w');
export_fig app_category_switch_frequency_line_8_6.pdf




% clear;
% clc;
% close;

% addpath('C:/export_fig/');
% M = dlmread('switch_frequency_app_category.csv');
% app_switch = M(:, 1:5).'
% figure('position', [100, 100, 1700*0.7, 600*0.7])
% plot(app_switch(:,4), '-d', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% hold on;
% plot(app_switch(:,1), '-o', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% plot(app_switch(:,2), '-*', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% plot(app_switch(:,3), '-+', ...
    % 'LineWidth',2,...
    % 'MarkerSize',10)
% hold off;
% ylabel('App category switch frequency');
% xlabel('Speed range (km/h)');
% speed = {'0-20', '20-40', '40-60', '60-80', '80-100'};
% set(gca, 'XTick', 1:5, 'XTickLabel', speed, 'FontSize',22)
% legend('All Cities', 'City A','City B','City C')

% set(gcf, 'Color', 'w');
% export_fig app_category_switch_frequency_line_17_6.pdf






