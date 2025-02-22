document.getElementById("generateForm").addEventListener("submit", function(event) {
  event.preventDefault();
  const patientCount = document.getElementById("patientCount").value;
  document.getElementById("generationStatus").innerText = `Generating ${patientCount} patients...`;

  fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ patientCount: patientCount })
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("generationStatus").innerText = `Generated ${data.count} patients.`;
      // Optionally, refresh the visualization here
    })
    .catch(error => {
      document.getElementById("generationStatus").innerText = "Error generating data.";
      console.error("Error:", error);
    });
});
