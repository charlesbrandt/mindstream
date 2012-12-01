  <!-- Meta Tags -->
  <meta http-equiv="content-type" content="application/xhtml+xml; charset=utf-8" />
  <meta name="robots" content="index, follow" />
  
  <meta name="description" content="{{description}}" />
  <meta name="keywords" content="{{keywords}}" />
  <meta name="author" content="{{author}}" />
  
  <!-- Favicon -->
  <link rel="shortcut icon" href="" />
  
  <!-- CSS -->
  <link rel="stylesheet" href="/css/style.css" media="screen" type="text/css" />
  <link rel="stylesheet" href="" media="print" type="text/css" />

  
  <!-- RSS -->
  <link rel="alternate" href="" title="RSS Feed" type="application/rss+xml" />

  <!-- JavaScript
  -->
  <link rel="stylesheet" href="/css/jquery-ui.css" media="screen" type="text/css" />

  <script src="/js/json2.js"></script>

  <script src="/js/jquery/1.6.1/jquery.min.js"></script>
  <script src="/js/jqueryui/1.8.18/jquery-ui-1.8.18.custom.min.js"></script>


  <script type="application/javascript">  
    $(document).ready(function(){
      $("input#tag").autocomplete({source: "http://localhost:8088/search/",
                                  select: function(event, ui) {
                                           window.location='/tagged/'+ui.item.value; }});
      });
  </script>
