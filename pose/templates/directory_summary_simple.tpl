<div class="directory" style="float:left">
%d = path.load()
%default = d.default_image()
%if default:
  <span class="slideshow">
  <a href="/path/{{path.to_relative()}}">
  %include image_tiny path=default, alt="image"
  </a><br>
  </span>
  <span>
  {{path.filename}} ({{len(d.images)}})<br>
  </span>
%else:
  <span class="directory">
  <a href="/path/{{path.to_relative()}}">
  [{{path.filename}}]</a>
  </span>
%end
</div>
