<a href="/"><img src="/images/home.png" height="20" width="21"></a> 

% from moments.timestamp import Timerange
% import datetime; now = datetime.datetime.now()
% for month in range(1, 13):
            %#print each month link to range
            % compact = "%s%02d" % (now.year, month)
            % month_range = Timerange(compact)
            <a href="/range/{{compact}}/{{month_range.end.compact()}}">{{month}}</a> - 
%end


<a href="/clouds">clouds</a> 
<a href="/timeline">full timeline</a> 

<form method="post" action="/tagged/">
<label for="tag">Search: </label>
<input type="text" id="tag" name="tag">  
<input type=submit name="submit" value="Go">
</form>
 
