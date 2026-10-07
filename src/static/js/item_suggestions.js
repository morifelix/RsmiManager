
async function showSuggestions(input) {
        const container =input.closest(".autocomplete");
        const suggestions = container.querySelector(".suggestions");
        const search =input.value.trim();

        if (search.length <2) {
            suggestions.innerHTML="";
            suggestions.style.display = "none";
            return
        }
        const response = await fetch(`api/items?q=${encodeURIComponent(search)}`);
        const items= await response.json();
        suggestions.innerHTML="";

        if(suggestions.length ==0){
            suggestions.style.display = "none";
            return;
        }

        items.forEach(item => {
            const option= document.createElement("div");
            option.classList.add("suggestion");
            option.textContent=`${item.id} - ${item.item_name}`;
            suggestions.appendChild(option);
            suggestions.style.display= "block";
            option.addEventListener("click",()=>{
               selectItem(input,item)
            });
        });
        
    }

    function selectItem(input,item){
        const entry = input.closest(".item-entry");
        const idInput=entry.querySelector(".item_id");
        const nameInput= entry.querySelector(".item_name");

        idInput.value= item.id;
        nameInput.value=item.item_name

        const suggestions =input.closest(".autocomplete").querySelector(".suggestions");

        suggestions.innerHTML="";
        suggestions.style.display = "none";

    }

 document.addEventListener("input",event =>{
    if(event.target.classList.contains("item_id") || event.target.classList.contains("item_name")){
        showSuggestions(event.target);
    }

 })