<html>
<head>
  <title>be present</title>
  %include header description='', keywords='', author=''

  <style type="text/css">
    body {
    background: #000000;
    color: #454456;
    font: 1em Arial, Helvetica, sans-serif;
    }

    #now { 
    margin-left:auto;
    margin-right:auto;
    width: 393px;
    height: 100px;
    background: url(/images/now-white.svg) no-repeat;
    opacity: 1;
    }
  </style>

  <script language="javascript">



  $(document).ready(
    function(){


  var total_time = 8000; //8 seconds


  function fadeout() {
    $('#now').animate({
      opacity: 0,
      //left: '+=50',
      //height: 'toggle'
    }, total_time, function() {
      // Animation complete.
      fadein();
    });
  };

  function fadein() {
    $('#now').animate({
      opacity: .5,
    }, total_time, function() {
      // Animation complete.
      fadeout();
    });
  };




  function fit_now() {
    $('#now').css('width', $(window).height() * .95);
    $('#now').css('height', $(window).height() * .95);
  };

  $(window).resize(function() {
    //$('body').prepend('<div>Window: ' + $(window).width() + ' x ' + $(window).height() + '</div>');
    //$('body').prepend('<div>Document: ' + $(document).width() + ' x ' + $(document).height() + '</div>');
    fit_now();

  });

  //$('#now').css('width', $(window).height());
  //$('#now').css('height', $(window).height());

  fit_now();
  fadeout();

  });
  </script>



</head>
<body>

  <div id="now"></div> 

</body>
</html>
