const container = document.getElementById("item-cont");
const addButton= document.querySelector("#add-item");

    addButton.addEventListener("click",() =>{
        const entry = document.createElement("div");
        entry.classList.add("item-entry");
        entry.innerHTML=`
        <div class="item-fields">
        <div class="autocomplete">
        <label for="item-id">Item ID
        <input type="text" name="ids[]"  class="item_id"   required autocomplete="off">
        </label><div class="suggestions"></div></div>
        <div class="autocomplete">
        <label for="item-id">Name
        <input type="text" required class="item_name"  autocomplete="off">
        </label><div class="suggestions"></div></div>
        <label for="item-id">Quantity
        <input type="number" name="quantity[]" min="1" autocomplete="off" required>
        </label>
        <button class="remove-item">Remove</button>
        `;
        container.appendChild(entry);
    });

    container.addEventListener("click",(event)=>{
        if(event.target.classList.contains("remove-item")){
            event.target.closest(".item-entry").remove();
        }
    })

