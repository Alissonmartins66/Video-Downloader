document.addEventListener("DOMContentLoaded", function () {
    const videoUrlInput = document.getElementById("video_url");
    const thumbnail = document.getElementById("thumbnail");
    const thumbnailLink = document.querySelector(".thumblink");
    const thumbnailContainer = document.getElementById("thumbnail-container");
    const buttonsContainer = document.getElementById("buttons-container"); // Adicionado

    videoUrlInput.addEventListener("input", function () {
        const url = videoUrlInput.value;
        thumbnailLink.href = url;

        fetch(`/get_thumbnail?video_url=${url}`)
            .then(response => response.json())
            .then(data => {
                if (data.thumbnail_url) {
                    thumbnail.src = data.thumbnail_url;
                    thumbnailContainer.style.display = "flex";
                    thumbnail.style.boxShadow = "0 0 10px #000";
                    buttonsContainer.style.display = "block"; // Mostra os botões
                } else {
                    thumbnail.src = "";
                    thumbnailContainer.style.display = "none";
                    buttonsContainer.style.display = "none"; // Oculta os botões se a thumbnail não for carregada
                }
            })
            .catch(error => {
                console.error("Erro ao obter a miniatura:", error);
            });
    });
});
