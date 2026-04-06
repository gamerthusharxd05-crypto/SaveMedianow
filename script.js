let dark = false;

function toggleTheme() {
  dark = !dark;
  document.body.className = dark ? "dark" : "light";
}

async function fetchVideo() {
  const url = document.getElementById("url").value;
  const results = document.getElementById("results");

  results.innerHTML = "Loading...";

  try {
    const res = await fetch(`http://127.0.0.1:8000/fetch?url=${encodeURIComponent(url)}`);
    const data = await res.json();

    if (data.error) {
      results.innerHTML = "Error: " + data.error;
      return;
    }

    results.innerHTML = `<h3>${data.title}</h3>`;

    data.formats.forEach(f => {
      const a = document.createElement("a");
      a.href = f.url;
      a.innerText = `Download ${f.quality}`;
      a.target = "_blank";
      results.appendChild(a);
    });

  } catch {
    results.innerHTML = "Server error";
  }
}