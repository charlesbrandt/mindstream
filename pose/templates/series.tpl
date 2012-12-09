<html>
<head>
  <title>{{ path.name }}</title>
  %include header description='', keywords='', author=''

  %#<h1> <a href="/path/{{ parent }}">{{parent.name}}</a> </h1>
</head>
<body>

<div style="float:left">

    <span class="description">
      %for i in range(4):
      <a href="/path/{{ parent }}">^</a> <br>
      %end
    </span>

    <span class="image">
      <a href="/series/{{ previous }}" accesskey="a">
	%include image_tiny path=previous, alt='<---'
      </a><br>
    </span>
							  
    <span class="selected">
      %include image_tiny path=path, alt=path.load().date()
      <br>
    </span>

    %if len(nexts):
    <span class="image">
      <a href="/series/{{ nexts[0] }}" accesskey="d">
	%include image_tiny path=nexts[0], alt=nexts[0].load().date()
      </a><br>
    </span>
    %nexts.pop(0)
    %end

    %for i in nexts:
    <span class="image">
      <a href="/series/{{ i }}">
	%include image_tiny path=i, alt=i.load().date()
      </a><br>
    </span>
    %end

</div>

<span class="image" style="float:left"> 
      <a href="/path/{{ path.to_relative() }}">
	%image = path.load()
	%image_path = image.size_path("medium")
	<img src="/image/{{image_path.to_relative()}}" width=500>
      </a><br>
</span>




  <hr />

  %include footer
</body>
</html>
