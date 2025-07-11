function preview() {
    const desc = document.getElementById("description").value;
    fetch("/api/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: desc })
    })
    .then(res => res.json())
    .then(data => {
        if (data.preview) {
            document.getElementById("output").innerText = "Предпросмотр:\n" + data.preview.join("\n");
        }
    });
}

function generate() {
    const intent = document.getElementById("intent").value;
    const desc = document.getElementById("description").value;
    fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ intent: intent, description: desc })
    })
    .then(res => res.json())
    .then(data => {
        if (data.examples) {
            document.getElementById("output").innerText = "Сохранено:\n" + data.examples.join("\n");
        } else {
            document.getElementById("output").innerText = "Ошибка: " + data.error;
        }
    });
}

function rollback() {
    fetch("/api/rollback", { method: "POST" })
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText = data.status || ("Ошибка: " + data.error);
    });
}
