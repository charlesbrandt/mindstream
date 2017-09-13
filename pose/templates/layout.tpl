<html>
<head>
  %if title:
  <title>{{ title }} - pose</title>
  %else:
  <title>pose</title>
  %end

  %include header description='', keywords='', author=''

  <script type="application/javascript">  
  </script>

</head>
<body>
  %include navigation 

  %#this is utilized by rebase calls
  %#easier than passing in body from application.py
  %include

  %include footer 

</body>
</html>
