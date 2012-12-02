%image = path.load()
%image_path = image.size_path("tiny")
%if not image_path.exists(): image.make_thumbs()
%tiny = image_path.load()
%dimensions = tiny.dimensions()
%width = dimensions[0] / 2

  <img src="/image/{{image_path.to_relative()}}" width="{{ width }}">
