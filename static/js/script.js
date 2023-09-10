async function postData(url = "", data = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

document.getElementById("sendButton").addEventListener("click", async () => {
  questionInput = document.getElementById("questionInput").value;
  document.getElementById("questionInput").value = "";
  document.querySelector(".right").style.display = "none";
  document.querySelector(".right2").style.display = "block";

  question1.innerHTML = questionInput;
  question2.innerHTML = questionInput;

  const result = await postData("/api", { question: questionInput });
  solution.innerHTML = result.answer; // Update "solution" div with the server's response
});
