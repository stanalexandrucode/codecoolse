const divContainer = document.querySelector(".card")
console.log(divContainer)


async function getData(callback) {
    let rawData = await fetch('/all_actors', {
        headers: {"Content-Type": "application/json"}
    })
    let data = await rawData.json()
    callback(data)

}

function showActors(data) {
    console.log(data)
    for (let foo of data) {
        let ulContainer = document.createElement('ul')
        ulContainer.innerHTML = `<li><a href="actorsDetails/${foo.id}">${foo.name}</a></li>`
        divContainer.appendChild(ulContainer)
    }
}

async function main() {
    await getData(showActors)
}

main()