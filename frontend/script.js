async function feedTamagotchi() {
  const inputBox = document.getElementById("studentInput");
  const input = inputBox.value.trim();

  const responseBox = document.getElementById("response");
  const tama = document.getElementById("tamagotchi");
  const moodText = document.getElementById("moodText");

  if (!input) return;

  // Clear the active prompt box immediately
  inputBox.value = "";

  // Show only the current submitted prompt
  responseBox.innerHTML = `
    <div class="submitted-prompt">${input}</div>
    <br>
    Tamagotchi is thinking...
  `;

  const response = await fetch(  "https://feynman-tamagotchi-api.onrender.com/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: input
    })
  });

  const data = await res.json();

  tama.src = data.mood + ".png";
  moodText.innerText = "Mood: " + data.mood;

  let feedback = data.feedback;

  feedback = feedback.replace(/TAMAGOTCHI_MOOD:\s*\w+/g, "");

feedback = feedback.replace(
  /TAMAGOTCHI_REACTION:/g,
  `<div class="pixel-title reaction-title">Reaction</div>`
);

feedback = feedback.replace(
  /MINI_HINT:/g,
  `<div class="pixel-title hint-title">Mini Hint</div>`
);

feedback = feedback.replace(
  /YOUR_TURN:/g,
  `<div class="pixel-title turn-title">Your Turn</div>`
);

feedback = feedback.replace(
  /FEEDBACK:/g,
  `<div class="pixel-title feedback-title">Feedback</div>`
);

feedback = feedback.replace(
  /FOOD_SCORE:/g,
  `<div class="pixel-title score-title">Food Score</div>`
);

feedback = feedback.replace(
  /NEXT_CHALLENGE:/g,
  `<div class="pixel-title challenge-title">Next Challenge</div>`
);
  responseBox.innerHTML = `
    <div class="submitted-prompt">${input}</div>
    ${feedback.replace(/\n/g, "<br>")}
  `;
}
