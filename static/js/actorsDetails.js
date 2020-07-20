const divContainer = document.querySelector('.card')
let id = divContainer.getAttribute('id')
console.log(id)

async function getData(callback, id) {
    let rawData = await fetch(`/actorsDetails/${id}`, {
        headers: {"Content-Type": "application/json"}
    })
    let data = await rawData.json()
    callback(data)
}


function showActorsDetails(data) {
    console.log(data)
    for (let foo of data) {
        let ulContainer = document.createElement('ul')
        ulContainer.innerHTML = `<li>Character <b>${foo.character}</b> in show <i>${foo.title}</i></li>`
        divContainer.appendChild(ulContainer)
    }
}


async function main() {
    getData(showActorsDetails, id)
}

main()