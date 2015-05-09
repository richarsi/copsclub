;
(function($) {
 $(document)
   .ready(
     function() {
      $('#maguire-globalnav').slicknav({
       prependTo : '#maguire-slicknav-wrapper'
      });
      // Internet Explorer 10 doesn't differentiate device width from 
      // viewport width. See notes in responsive-utilities.less
      if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
       $('<style>@-ms-viewport{width:auto!important}</style>').appendTo('head');
      }
     });
})(jQuery);
