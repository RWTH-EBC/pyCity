function result = create_time(date)
%This function receives the time stamps in cell format and transforms it to
%seconds
%   Input: cell array with this format: "dd.mm.yyyy hh:mm:ss"
%   Output: vector in which the first entry is zero, all subsequent values
%   represent the seconds passed by

    % Break down "date" into a matrix:
    % Columns: day, month, year, hour, minute, second (6 in total)
    
    time_now = zeros(6, 1);
    time_total = zeros(length(date), 1);
    time_relative = zeros(length(date), 1);
    
    
    i = 1;
    
    
    while i <= length(date)
        day_time = strsplit(date{i}, ' ');
        day = strsplit(day_time{1}, '.');
        time = strsplit(day_time{2}, ':');
        
        time_now(1:3) = str2double(day);
        time_now(4:6) = str2double(time);
        
        time_total(i) = time_now(6) + 60*time_now(5) + 3600 * time_now(4) + 24*3600 * time_now(3);
        
        time_relative(i) = time_total(i) - time_total(1);
        
        i = i + 1;
    end

    result = time_relative;

end

