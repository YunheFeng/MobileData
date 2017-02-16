clear;
clc;
close;

addpath('C:/export_fig/');
M = dlmread('switch_frequency_app_category.csv');
app_cate_switch = M(:, 1:5);
figure('position', [100, 100, 800, 600]) 
bar(app_cate_switch)
ylabel('APP category switch frequency');
city_name = {'City A','City B','City C','All Cities'};
set(gca, 'XTick', 1:4, 'XTickLabel', city_name, 'FontSize',14)    
legend('0-20km/h', '20-40km/h', '40-60km/h', '60-80km/h', '80-100km/h')

set(gcf, 'Color', 'w');
export_fig app_category_switch_frequency_8_6.pdf




clear;
clc;
close;

addpath('C:/export_fig/');
M = dlmread('switch_frequency_app_category.csv');
app_cate_switch = M(:, 1:5);
figure('position', [100, 100, 1700*0.7, 600*0.7]) 
bar(app_cate_switch)
ylabel('APP category switch frequency');
city_name = {'City A','City B','City C','All Cities'};
set(gca, 'XTick', 1:4, 'XTickLabel', city_name, 'FontSize',14)   
legend('0-20km/h', '20-40km/h', '40-60km/h', '60-80km/h', '80-100km/h')

set(gcf, 'Color', 'w');
export_fig app_category_switch_frequency_17_6.pdf

