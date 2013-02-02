<html>
<head>
  <title>{{name}} - related</title>
  %include header description='', keywords='', author=''

</head>
<body>
%#http://bottle.paws.de/docs/dev/stpl.html

<h1>Tags related to {{name}}:</h1>

%for t in tags:
   <p><a href="/tagged/{{t}}">{{t}}</a> <a href="/related/{{t}}">[r]</a></p>
%end

  <hr />

</body>
</html>
