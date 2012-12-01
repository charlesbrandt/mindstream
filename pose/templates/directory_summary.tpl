<div class="directory">
%d = path.load()
%default = d.default_image()
%if default:
  <span class="slideshow" style="float: left">
  <a href="/path/{{path.to_relative()}}">
  %include image_tiny path=default, alt="image"
  </a>
  </span>
  <span style="float: left">
  {{len(d.images)}} images<br>
  %if admin:
    <a href="/path/launch/{{path.to_relative()}}">launch</a> | <a href="/path/dupe/{{path.to_relative()}}">dupe</a>
    <form action="/path/edit/{{path.to_relative()}}" method="post">
    <input size="14" class="update_tags" id="{{path.filename}}" name="tags" type="text" value="{{path.to_tags(include_parent=False)}}"  />
    <br>
    <input id="hi" name="submit" type="submit" value="Save" />
    </form>
  %end
  </span>
%else:
  <div style="clear: both">
  <a href="/path/{{path.to_relative()}}">
  [{{path.filename}}]</a>
  </div><br>
%end
</div>
