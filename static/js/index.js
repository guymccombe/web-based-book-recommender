$(".inputWrapper input").focus(function() {
  $(this).addClass("focussed");
});

$(".inputWrapper input").blur(function() {
  if ($(this).val().length == 0) {
    $(this).removeClass("focussed");
  }
});

$("#refreshRecommendations").click(e => {
  e.preventDefault();
  getRecommendations();
});

$(document).ready(function() {
  getRecommendations();
});

function getRecommendations() {
  $.ajax({
    type: "GET",
    url: "recommend",
    success: function(res) {
      const recommended = $("#recommended");
      recommended.html("");
      for (index in res) {
        recommended.append("<tr><td>" + res[index] + "</td></tr>");
      }
    },
    error: function(xhr) {
      console.log(xhr.responseText);
    }
  });
}
