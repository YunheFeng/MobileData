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

% figure(1); % speed appcat correlation
% for i = 1:n
%     subplot(r, c, i);
% %     marketshare = bsxfun(@rdivide, speedappcatallcity(i,1:column), sum(speedappcatallcity(:,1:column), 1));
%     marketshare = 100 * bsxfun(@rdivide, speedappcatallcity(i,1:column), speedrecord(1, 1:column));
% %     marketsharexuzhou = 100 * bsxfun(@rdivide, speedappcatxuzhou(i,1:column), speedrecord(2, 1:column));
% %     marketshareyancheng = 100 * bsxfun(@rdivide, speedappcatyancheng(i,1:column), speedrecord(3, 1:column));
% %     marketsharetaizhou = 100 * bsxfun(@rdivide, speedappcattaizhou(i,1:column), speedrecord(4, 1:column));
%     plot(marketshare, '-d', 'LineWidth', 2); hold on;
% %     plot(marketsharexuzhou, '-o'); hold on;
% %     plot(marketshareyancheng, '-*'); hold on;
% %     plot(marketsharetaizhou, '-+');
%     grid on;
%     
% %     a=[cellstr(num2str(get(gca,'ytick')'))]; 
% %     pct = char(ones(size(a,1),1)*'%');
% %     new_yticks = [char(a),pct];
% %     set(gca,'yticklabel',new_yticks);
%     set(gca, 'Xlim', [1 column]);
%     set(gca, 'XTick', [1:column]);
%     set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});
%     Ymean = mean(marketshare);
%     Ymin = min(marketshare);
%     Ymax = max(marketshare);
%     set(gca, 'Ylim', [min(Ymin, 0.75*Ymean) max(Ymax, 1.25*Ymean)]);
%     
% %     legend('All cities', 'City A', 'City B', 'City C');
%     set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 16);
%     ylabel_hand=ylabel('Contribution (%)');
%     xlabel_hand=xlabel('Speed range (km/h)');
%     title(title_string(i))
% end
% 
% figure(2) % speed volume correlation
% plot(speedvol(1, 1:column), '-d', 'LineWidth', 2); hold on;
% plot(speedvol(2, 1:column), '-o', 'LineWidth', 2); hold on;
% plot(speedvol(3, 1:column), '-*', 'LineWidth', 2); hold on;
% plot(speedvol(4, 1:column), '-+', 'LineWidth', 2); 
% 
% set(gca, 'XTick', [1:column]);
% set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});
% 
% legend('All cities', 'City A', 'City B', 'City C', 'Location', 'Northwest');
% set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
% ylabel_hand=ylabel('Volume (Byte)');
% xlabel_hand=xlabel('Speed range (km/h)');


% figure(3) % speed gap correlation
% plot(speedgap(1, 1:column), '-d', 'LineWidth', 2); hold on;
% plot(speedgap(2, 1:column), '-o', 'LineWidth', 2); hold on;
% plot(speedgap(3, 1:column), '-*', 'LineWidth', 2); hold on;
% plot(speedgap(4, 1:column), '-+', 'LineWidth', 2); 
% 
% set(gca, 'XTick', [1:column]);
% set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});
% 
% legend('All cities', 'City A', 'City B', 'City C');
% set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
% ylabel_hand=ylabel('Average time interval (s)');
% xlabel_hand=xlabel('Speed range (km/h)');

% figure(4) % volume per connection
% plot(speedpervol(1, 1:column), '-d', 'LineWidth', 2); hold on;
% plot(speedpervol(2, 1:column), '-o', 'LineWidth', 2); hold on;
% plot(speedpervol(3, 1:column), '-*', 'LineWidth', 2); hold on;
% plot(speedpervol(4, 1:column), '-+', 'LineWidth', 2); 
% 
% set(gca, 'Ylim', [5000 15000]);
% set(gca, 'XTick', [1:column]);
% set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});
% 
% legend('All cities', 'City A', 'City B', 'City C');
% set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
% ylabel_hand=ylabel('Average volume per access (Byte)');
% xlabel_hand=xlabel('Speed range (km/h)');

figure(5) % speed diversity
speeddiversity = speeddiversity * 60;
plot(speeddiversity(1, 1:column), '-d', 'LineWidth', 2); hold on;
plot(speeddiversity(2, 1:column), '-o', 'LineWidth', 2); hold on;
plot(speeddiversity(3, 1:column), '-*', 'LineWidth', 2); hold on;
plot(speeddiversity(4, 1:column), '-+', 'LineWidth', 2); 
speeddiversity = speeddiversity / 60

set(gca, 'XTick', [1:column]);
set(gca, 'XTickLabel', {'0-20'; '20-40'; '40-60'; '60-80'; '80-100'});

legend('All cities', 'City A', 'City B', 'City C', 'Location', 'Northwest');
set(gca, 'Fontname', 'Times New Roman', 'Fontsize', 20);
ylabel_hand=ylabel('Average no. of used apps (app/min)');
xlabel_hand=xlabel('Speed range (km/h)');
