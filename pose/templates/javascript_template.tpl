<html>
<head>
  <title></title>
  %include header description='', keywords='', author=''

  <link rel="stylesheet" href="/css/jquery-ui.css" media="screen" type="text/css" />
  <!--
   from:
   http://code.google.com/apis/libraries/devguide.html#jqueryUI
      
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
  <script src="/js/jquery/1.6.1/jquery.min.js"></script>
  <script src="file:///c/technical/web/template/js/jquery/1.6.1/jquery.js"></script>


   <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
  <script src="/js/jquery-1.4.4.min.js"></script>
  <script src="file:///c/technical/web/template/js/jquery/1.4.4/jquery.js"></script>

   <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/jquery-ui.min.js"></script>
  -->
  <script src="/js/jquery-ui.min.js"></script>
  <!--
  <script src="file:///c/technical/web/template/js/jqueryui/1.8.13/jquery-ui.js"></script>

  <script src="/js/jquery.mobile-1.0a2.min.js"></script>  
  <script src="/js/processing-1.0.0.min.js"></script>  
  <script src="/js/raphael-min.js"></script>  

  <script src="file:///c/moments2/moments2/journal.js"></script>
  -->
  <script src="/js/journal.js"></script>


  <script language="javascript">
$(document).ready(function(){
   /* Description:

   */
   // Your code here
   var j = new Journal("http://localhost:8088/tags/");

 });
$(function() {
   /* // this works!!:
   var availableTags = [
      "Java",
      "Javascript",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
   ];
   $("input#tags").autocomplete({source: availableTags});
   */
   $("input#tags").autocomplete({source: "http://localhost:8088/search/",
                                 select: function(event, ui) {
                                         window.location='/tagged/'+ui.item.value; }
                                  });
});


  </script>

</head>
<body>
  %include navigation 

<div id="result"> </div>

search for entries based on tags<br>
tag search field<br>
should autocomplete with available options<br>

<label for="tags">Tags: </label>
<input id="tags" value=''>
<input type=button name="submit" value="Go" onClick="window.location='/tagged/test'+$('input#tags').value;">

  
  {{! body }}

  %include footer 

</body>
</html>

<html>
<head>
  <title></title>


   

  </script>

</head>
<body>

</body>
</html>
