%if alt:
  <img src="/image/{{image_path.to_relative()}}" alt="{{ alt }}">
%else:
  <img src="/image/{{image_path.to_relative()}}">
%end
