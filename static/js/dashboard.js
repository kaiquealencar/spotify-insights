function flipCard(id) {
         const card = document.getElementById(id);
         const isFlipped = card.classList.contains("flipped");
         
         if (isFlipped) {
             const iframes = card.querySelectorAll(".card-back iframe");
             iframes.forEach(iframe => {
                 const src = iframe.src;
                 iframe.src = src;
             });
         }
         card.classList.toggle("flipped");
     }