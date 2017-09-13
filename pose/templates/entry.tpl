<div class="entry">
<div class="entry_header">
<span class="asterisk"><a href="/path/launch/{{entry.path}}">*</a></span>
%#<span class="asterisk"><a href="/path/launch/{{entry.path.to_relative()}}">*</a></span>
%#<span class="asterisk"><a href="/path/launch/{{entry.created.compact()}}">*</a></span>
<span class="date">{{str(entry.created)}} </span>
<span class="tags">
%for tag in entry.tags:
   <a href="/tagged/{{tag}}">{{tag}}</a>
%end
</span></div>
<div class="entry_data">
%for line in entry.data.splitlines():
  %if line.startswith('http'):
     <a href="{{line}}">{{line}}</a><br>
  %else:
     {{line}}<br>
  %end
%end

</div>
</div>