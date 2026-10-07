genSearch()

function genSearch(){
const searchInput=document.querySelector("#search-items");

const tableRows=document.querySelectorAll(".scroll-table table tbody tr");

searchInput.addEventListener("input",()=>{
    const search= searchInput.value.toLowerCase();

        tableRows.forEach(row=>{
            const text=row.textContent.toLowerCase();

            row.style.display=text.includes(search) ? "":"none";
        });
});
};

function filteredSearch(){
const searchInput=document.querySelector("#search-items");

const tableRows=document.querySelectorAll(".scroll-table table tbody tr");

searchInput.addEventListener("input",()=>{
    const search= searchInput.value.toLowerCase();

        tableRows.forEach(row=>{
            const id=row.cells[0].textContent.toLowerCase();
            const name=row.cells[1].textContent.toLowerCase();
            const type=row.cells[3].textContent.toLowerCase();

            const match=
                id.includes(search) ||
                name.includes(search)||
                type.includes(search);

            row.style.display=match ? "":"none";
        });
});
};
