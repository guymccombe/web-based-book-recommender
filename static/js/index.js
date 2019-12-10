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

const recElement = $("#recommended");
let recommendations, numberDisplayed;
function getRecommendations() {
  $.ajax({
    type: "GET",
    url: "recommend",
    success: function(res) {
      recommendations = res;
      numberDisplayed = 10;
      $("#recommended > tr").remove();
      for (let i = 0; i < numberDisplayed; i++) {
        console.log(i);
        recElement.append("<tr><td>" + res[i] + "</td></tr>");
      }
    },
    error: function(xhr) {
      console.log(xhr);
    }
  });
}

$("#tableWrapper").on("scroll", function() {
  if (
    $(this).scrollTop() + $(this).innerHeight() >=
    $(this)[0].scrollHeight - 25
  ) {
    for (let i = numberDisplayed; i < numberDisplayed + 5; i++) {
      recElement.append("<tr><td>" + recommendations[i] + "</td></tr>");
    }
    numberDisplayed += 5;
  }
});

$("#reviewForm").on("submit", e => {
  e.preventDefault();
  $("#recommended > tr").remove();
  $("#recommended").addClass("animate");
  const res = $.post("/rating", $("#reviewForm").serialize()).done(function() {
    //$("#reviewForm").reset();
    getRecommendations();
    $("#recommended").removeClass("animate");
    recElement.show();
  });
  // TODO post
});

$(document).ready(function() {
  getRecommendations();
});
