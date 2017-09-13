<html>
<head>
  %#http://bottle.paws.de/docs/dev/stpl.html SimpleTemplate documentation\\
  <title></title>
  %include header description='', keywords='', author=''

  <!--
  <link rel="stylesheet" href="/css/now.css" media="screen" type="text/css" />
  -->

  <style>
    #now { 
    margin-left:auto;
    margin-right:auto;
    width: 393px;
    height: 100px;
    background: url(/images/now.svg) no-repeat;
    opacity: 0.5;
    }
  </style>

  <script language="javascript">
  $(document).ready(
    function(){


  function fit_now() {
    $('#now').css('width', $(window).height() * .95);
    $('#now').css('height', $(window).height() * .95);
  };

  $(window).resize(function() {
    //$('body').prepend('<div>Window: ' + $(window).width() + ' x ' + $(window).height() + '</div>');
    //$('body').prepend('<div>Document: ' + $(document).width() + ' x ' + $(document).height() + '</div>');
    fit_now();

  });

  var total_time = 8000; //8 seconds
  var fade_delay = total_time / 100 // 100 = number of steps involved

  var ani = {
	resizew: {
		type:	'width',
		to:	$(window).height(),
		step:	2,
		delay:	20,
	},
	resizeh: {
		type:	'height',
		to:	$(window).height(),
		step:	2,
		delay:	20,
	},
	fadein: {
		type:	'opacity',
                from:   0,
		to:	100,
		step:	1,
		delay:	fade_delay,
	},
	fadeout: {
		type:	'opacity',
                from:   100,
		to:	0,
		step:	-1,
		delay:	fade_delay,
                onfinish: function(){
                        $fx('#now').fxStop();
			$fx('#now').fxAdd(ani.fadein).fxRun(null, 1);}

	},
  }

  function fadeout(){
     $fx('#now').fxReset();
     $fx('#now').fxAdd(ani.fadeout).fxRun(fadein, 1);
  };

  function fadein(){
     $fx('#now').fxReset();
     $fx('#now').fxAdd(ani.fadein).fxRun(fadeout, 1);
  };

  function startAnimation(){
	$fx('#now').fxAdd(ani.fadein).fxRun(fadeout, 1);
  };

  //$('#now').css('width', $(window).height());
  //$('#now').css('height', $(window).height());

  fit_now();

  startAnimation();
  });
  </script>


</head>
<body>

  <div id="now"></div> 

</body>
</html>
