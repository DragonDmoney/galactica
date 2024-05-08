const url = "http://localhost:3000";

$(document).ready(function () {
  let userToken = ""; // Variable to store user token

  $("#startButton").click(function () {
    userToken = $("#tokenInput").val();
    if (userToken) {
      console.log("User token: " + userToken);
      switchToGameScreen();
    } else {
      alert("Please enter a token.");
    }
  });

  function guess() {
    $("#guessOutput").text($("#guessInput").val());
    let v = $("#guessInput").val();
    $("#guessInput").val("");

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token: userToken, guess: v }),
    })
      .then((response) => response.json())

      .then((data) => {
        console.log(data);
        update(data);
      });
  }

  $("#guessInput").keypress(function (event) {
    if (event.which === 13) {
      // Enter key pressed
      guess();
    }
  });

  $("#guessButton").click(function () {
    guess();
  });

  $("#testButton").click(function () {
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token: userToken, next: true }),
    })
      .then((response) => response.json())

      .then((data) => {
        console.log(data);
        update(data);
      });
  });

  function switchToGameScreen() {
    $("#welcomeScreen").hide();
    $("#gameScreen").show();
    main();
  }

  function main() {
    request = fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token: userToken }),
    }).then((response) => response.json());

    request.then((data) => {
      console.log("Current image: " + data.current_image);
      console.log(data.images[data.current_image]);
      console.log(data);
      update(data);
    });
  }

  function timer(data) {
    console.log("timer");
    $("#timer").text("7");

    $("#guessInput").prop("disabled", true);
    $("#guessButton").prop("disabled", true);

    var x = setInterval(function () {
      $("#timer").text(parseInt($("#timer").text()) - 1);

      if ($("#timer").text() == "0") {
        $("#guessInput").prop("disabled", false);
        $("#guessButton").prop("disabled", false);

        $("#guessInput").val(data.labels[data.current_image]);
        $("#guessButton").click();
        $("#timer").text("");

        window.clearInterval(x);

        return;
      }
    }, 1000);
  }

  function update(data) {
    if (data.done) {
      $("#gameScreen").hide();
      $("#testScreen").show();

      if (data.final_test == true) {
        $("#testButton").hide();
        $("#testOutput").text(
          "You finished the final test in " +
            data.attempts +
            " attempts. You're done and thank you for participating!!"
        );
      } else {
        $("#testOutput").text(
          "You finished the test in " +
            data.attempts +
            " attempts. Get ready for the next one"
        );
      }
    } else {
      $("#testScreen").hide();
      $("#gameScreen").show();
    }

    $("#gameImage").attr(
      "src",
      url + "/image/" + userToken + `?v=${new Date().getTime()}`
    );
    $("#wordBank").text(data.labels.join(" "));

    if (data.text.includes("Correct")) {
      $("#guessOutput").css("color", "green");
    } else if (data.text.includes("Incorrect")) {
      console.log("incorrect");
      $("#guessOutput").css("color", "red");
      timer(data);
    } else {
      $("#guessOutput").css("color", "black");
    }

    $("#guessOutput").text(data.text);
    $("#attemptCount").text(data.attempts);
  }
});
