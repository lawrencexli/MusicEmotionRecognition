$(function(){

    $(".dropdown-menu").click(function(){

      $(".dropdown-menu:first-child").text($(this).text());
      $(".dropdown-menu:first-child").val($(this).text());

   });

});