clear;
clc;
close;

addpath('C:/export_fig/');
M = dlmread('speed_appcat_all_city.csv');
volume = M(:, 3:4);
time = M(:, 5:6);
volume_per_min = volume./time.*60
figure('position', [100, 100, 800, 600]) 
bar(volume_per_min)
ylabel('Volume (Byte) per minute');
app_name = {'IM','Reading','Microblog','Navigation','Video','Music','App Market','Game','Online Payment','Comic','Email','P2P','VOIP','MM','B&D','Finance','Security','Others'};
set(gca, 'XTick', 1:18, 'XTickLabel', app_name, 'FontSize',14)   
set(gca,'XTickLabelRotation',90) 
legend('low speed (\leq50km/h)', 'high speed (>50km/h)')

set(gcf, 'Color', 'w');
export_fig volume_high_low_speed_per_minute_8_6.pdf





clear;
clc;
close;

addpath('C:/export_fig/');
M = dlmread('speed_appcat_all_city.csv');
volume = M(:, 3:4);
time = M(:, 5:6);
volume_per_min = volume./time.*60
figure('position', [100, 100, 1700*0.7, 600*0.7]) 
bar(volume_per_min)
ylabel('Volume (Byte) per minute');
app_name = {'IM','Reading','Microblog','Navigation','Video','Music','App Market','Game','Online Payment','Comic','Email','P2P','VOIP','MM','B&D','Finance','Security','Others'};
set(gca, 'XTick', 1:18, 'XTickLabel', app_name, 'FontSize',14)   
set(gca,'XTickLabelRotation',90) 
legend('low speed (\leq50km/h)', 'high speed (>50km/h)')

set(gcf, 'Color', 'w');
export_fig volume_high_low_speed_per_minute_17_6.pdf