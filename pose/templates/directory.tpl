<html>
<head>
  <title>{{ path.name }}</title>
  %include header description='', keywords='', author=''
  
<script src="/js/jquery.cycle.lite.1.0.min.js"></script> 

<script type="text/javascript">      
$(document).ready(function(){
   /* TODO:
   add a function to all img tags
   on mouse over
   get next image in directory
   update dom to use the new image

   on tag update form save
   get response of if submit was successful
   either way, add an alert indicating status that fades

   on dupe link clicked
   get the new html block for the new directory
   and insert it to the right location in the listing/DOM
   */

   /*
   add a function to all img tags
   on mouse over
   get next image in directory
   update dom to use the new image
   */
   
   /*
   // this attempt uses the jquery.cycle plugin.  all run at the same time though.
   $('.slideshow').attr("loaded", false)
   $('.slideshow')
        .mouseover(function() { 
            var src = $(this).attr("loaded")
	    //$('body').prepend('<div>Mouseover: ' + src + '</div>');
            if ($(this).attr("loaded") == false) {
               $('body').prepend('<div>Loading: </div>');
               // append other images here
	       $(this).cycle({
	   	        fx: 'fade', // choose your transition type, ex: fade, scrollUp, shuffle, etc...
               }); 	
               $(this).attr("loaded", true);
            }
            else {
               //$('body').prepend('<div>Resuming: </div>');
               $(this).cycle('resume');
            }

        })
        .mouseout(function() {
            $('.slideshow').cycle('pause')
            //var src = $(this).attr("src").replace("over", "");
	    //$('body').prepend('<div>Mouseout: ' + src + '</div>');
            //$(this).attr("src", src);
        });

   var slidesAdded = false; 
     
   function onBefore(curr, next, opts) { 
       // make sure we don't call addSlide before it is defined 
       $('body').prepend('<div>onBefore called</div>');
       if (!opts.addSlide || slidesAdded) 
           return; 
         
       // add slides for images 3 - 8 
       // slides can be a DOM element, a jQuery object, or a string 
       for (var i=3; i < 9; i++) 
           opts.addSlide('<img src="images/beach'+i+'.jpg" width="200" height="200" />'); 
       slidesAdded = true; 
   }; 

   */

 });
</script>

</head>
<body>
  <h1>
<a href="/">*</a>/
  %parts = path.relative_path_parts()
  %if len(parts):
  %for part in parts[:-1]:
<a href="/path/{{part[1]}}">{{part[0]}}</a>/
  %end
{{parts[-1][0]}}
  %end
  </h1>

  <a href="/sort/{{ path }}/sort.json">Sort it</a><br>
  <p></p>

  %for p in contents:
  %if p.type() == "Directory":
    %try:
    %include directory_summary_simple path=p, admin=True
    %except:
    % pass
    %end
  %else:
    %include series_summary path=p
  %end
  %end

<p style="clear:both">&nbsp;</p>
<p>&nbsp;</p>

  <hr />

  %include footer
</body>
</html>
