  %if path.type() == "Image":
    <span><a href="/path/{{path.to_relative()}}">
    %img = path.load()
    %tiny = img.size_path("tiny")
    %small = img.size_path("small")
    <img src="/image/{{small.to_relative()}}" width=147>
    %#<img src="/image/{{tiny.to_relative()}}">
    %# //include image_tiny image_path = path
    %#{{path.filename}}
    </a></span>
  %else:
    <div class="file"><a href="/path/{{path.to_relative()}}">{{path.filename}}</a></div>
  %end
