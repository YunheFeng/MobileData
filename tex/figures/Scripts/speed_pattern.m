n = 8;
c = 4;
r = ceil(n/c);
column = 5;
title_string = {'Instant message' ...
    'Reading' ...
    'Microblog' ...
    'Navigation' ...
    'Video' ...        
    'Music' ...
    'App market' ...
    'Browser & Download'};

figure(1); % speed appcat correlation
for i = 1:n
    subplot(r, c, i);
%     marketshare = bsxfun(@rdivide, speedappcatallcity(i,1:column), sum(speedappcatallcity(:,1:column), 1));
    marketshare = 100 * bsxfun(@rdivide, speedappcatallcity(i,1:column), speedrecord(1, 1:column));
%     marketsharexuzhou = 100 * bsxfun(@rdivide, speedappcatxuzhou(i,1:column), speedrecord(2, 1:column));
%     marketshareyancheng = 100 * bsxfun(@rdivide, speedappcatyancheng(i,1:column), speedrecord(3, 1:column));
%     marketsharetaizhou = 100 * bsxfun(@rdivide, speedappcattaizhou(i,1:column), speedrecord(4, 1:column));
    plot(marketshare, '-d', 'LineWidth', 2); hold on;
%     plot(marketsharexuzhou, '-o'); hold on;
%     plot(marketshareyancheng, '-*'); hold on;
%     plot(marketsharetaizhou, '-+');
    grid on;
    
    set(gca, 'XTick', [1:column]);
    set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});
    Ymean = mean(marketshare);
    set(gca, 'Ylim', [0.5*Ymean 1.5*Ymean]);
    
%     legend('all city', 'xuzhou', 'yancheng', 'taizhou');
    set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 16);
    ylabel_hand=ylabel('Impact (%)');
    set(ylabel_hand,'Fontname', 'Times New Roman', 'Fontsize', 14);
    xlabel_hand=xlabel('Speed range (km/h)');
    set(xlabel_hand,'Fontname', 'Times New Roman', 'Fontsize', 14);
    title(title_string(i))
    
end

figure(2) % speed volume correlation
plot(speedvol(1, 1:column), '-d', 'LineWidth', 2); hold on;
plot(speedvol(2, 1:column), '-o', 'LineWidth', 2); hold on;
plot(speedvol(3, 1:column), '-*', 'LineWidth', 2); hold on;
plot(speedvol(4, 1:column), '-+', 'LineWidth', 2); 

set(gca, 'XTick', [1:column]);
set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});

legend('all city', 'xuzhou', 'yancheng', 'taizhou');
set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 16);
ylabel_hand=ylabel('Volume (Byte)');
set(ylabel_hand,'Fontname', 'Times New Roman', 'Fontsize', 14);
xlabel_hand=xlabel('Speed range (km/h)');
set(xlabel_hand,'Fontname', 'Times New Roman', 'Fontsize', 14);


figure(3) % speed gap correlation
plot(speedgap(1, 1:column), '-d', 'LineWidth', 2); hold on;
plot(speedgap(2, 1:column), '-o', 'LineWidth', 2); hold on;
plot(speedgap(3, 1:column), '-*', 'LineWidth', 2); hold on;
plot(speedgap(4, 1:column), '-+', 'LineWidth', 2); 

set(gca, 'XTick', [1:column]);
set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});

legend('all city', 'xuzhou', 'yancheng', 'taizhou');
set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 16);
ylabel_hand=ylabel('Average gap (Byte)');
set(ylabel_hand,'Fontname', 'Times New Roman', 'Fontsize', 14);
xlabel_hand=xlabel('Speed range (km/h)');
set(xlabel_hand,'Fontname', 'Times New Roman', 'Fontsize', 14);

