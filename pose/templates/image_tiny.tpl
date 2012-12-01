%image = path.load()
%image_path = image.size_path("tiny")
%if not image_path.exists(): image.make_thumbs()
%if alt:
%include image image_path=image_path, alt=alt
%else:
%include image image_path=image_path
%end