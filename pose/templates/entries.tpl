<html>
<head>
  <title>{{name}} - entries</title>
  %include header description='', keywords='', author=''
  
  <script language="javascript">
  </script>

</head>
<body>
  %include navigation 
%#http://bottle.paws.de/docs/dev/stpl.html

<h1>{{len(entries)}} entries tagged {{name}}:</h1>
<p>
<p><b>All tags related to '{{name}}':</b></p>
<p>
%for t in tags:
   <a href="/tagged/{{t}}">{{t}}</a> &nbsp;
   %#<a href="/related/{{t}}">[r]</a>
%end
</p>

%#(Tags related to <a href="/related/{{name}}">{{name}}</a>)</p>
<hr />

%for e in entries:
   %include entry entry=e
%end

  <hr />

</body>
</html>
