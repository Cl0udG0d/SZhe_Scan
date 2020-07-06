$("#begin").on("click", function () {
  $("#progressFill").animate(
    {
      width: "100%",
    },
    10 * 1000
  );
  var count = 0;
  var timer = setInterval(function () {
    count++;
    var percentageValue = count + "%";
    $("#percentage").html(percentageValue);
    if (count >= 100) clearInterval(timer);
  }, 99);
});
