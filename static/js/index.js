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
        $("#recommended").append("<tr><td>" + res[i] + "</td></tr>");
      }
    },
    error: function(xhr) {
      $("#recommended").append("<tr><td>" + xhr.responseJSON + "</td></tr>");
    }
  });
}

$("#tableWrapper").on("scroll", function() {
  if (
    $(this).scrollTop() + $(this).innerHeight() >=
    $(this)[0].scrollHeight - 25
  ) {
    for (let i = numberDisplayed; i < numberDisplayed + 5; i++) {
      $("#recommended").append("<tr><td>" + recommendations[i] + "</td></tr>");
    }
    numberDisplayed += 5;
  }
});

$("#reviewForm").on("submit", e => {
  e.preventDefault();

  if (
    // If exists an empty input
    $("input").filter(function() {
      return $.trim($(this).val()).length == 0;
    }).length > 0
  ) {
    $("#errorMessage").text("Please fill all text fields.");
    return;
  }

  $("#tableWrapper").scrollTop(0);
  $("#recommended > tr").remove();
  $("#recommended").addClass("animate");

  $.post("/rating", $("#reviewForm").serialize(), function() {
    $("#reviewForm").trigger("reset");
    $("#reviewForm input").removeClass("focussed");
    $("#errorMessage").text("");
  })
    .fail(function(xhr) {
      $("#errorMessage").text(xhr.responseText);
    })
    .always(function() {
      $("#recommended").removeClass("animate");
      getRecommendations();
    });
});

$("#ratingInput").keypress(e => {
  // Ignore non-numeric characters
  if (e.which < 48 || e.which > 57) {
    if (e.key !== "." && e.key !== "Enter") {
      // allow . and enter
      e.preventDefault();
    }
  }
});

$("#delete").on("click", function() {
  return confirm(
    "Are you sure you want to delete your account? This action cannot be undone."
  );
});

$(document).ready(function() {
  getRecommendations();
});
