clc;
clear;

opts = detectImportOptions('data.xlsx', 'VariableNamingRule', 'preserve');
data = readtable('data.xlsx', opts);

headers = data.Properties.VariableNames;
x_coords = data{:, 1};
avg_depths = zeros(size(x_coords));
std_devs = zeros(size(x_coords));

figure;
hold on;

for col = 2:width(data)

    range_str = headers{col};

    range_parts = split(range_str, '-');
    start_point = str2double(range_parts{1});
    end_point = str2double(range_parts{2});

    y_coords = data{:, col};
    scatter(x_coords, y_coords, 'filled', 'DisplayName', range_str);
end

for i = 1:length(x_coords)
    depths = data{i, 2:end};
    depths = depths(~isnan(depths));
    
    % 计算平均深度和标准差
    if ~isempty(depths)
        avg_depths(i) = mean(depths);
        std_devs(i) = std(depths);
    else
        avg_depths(i) = NaN; % 如果没有有效的深度值，设置为 NaN
        std_devs(i) = NaN;
    end
end

errorbar(x_coords, avg_depths, std_devs, 'LineWidth', 2, 'Color', 'r', 'CapSize', 5);
set(findall(gca, 'Type', 'ErrorBar'), 'LineWidth', 0.8); % 误差棒


xlabel('x (m)');
ylabel('h (m)');
set(gca, 'YDir', 'reverse');

ylim([-2 12]);
legend show;
title('巴东一中折射面深度');

grid on;
grid minor;
hold off;
