function sendMessage() {
  const input = document.getElementById("studentInput").value;
  const responseBox = document.getElementById("response");
  const tama = document.getElementById("tamagotchi");
  const mood = document.getElementById("mood");

  responseBox.innerText =
    "Tamagotchi is thinking...\n\nYou said: " + input;

  tama.src = "excited.gif";
  mood.innerText = "Mood: excited";
}