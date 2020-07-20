const addCommentBtn = document.querySelector('.addCommentBtn')
const divContainer = document.querySelector('.hiden')
const textarea = document.querySelector('.textarea')
const saveBtn = document.querySelector('.saveBtn')
let id = textarea.getAttribute('id')
const commentContainer = document.querySelector('.showComment')

function visibleHandler() {
    divContainer.classList.toggle('visible')
}

//POST
async function addData(data = {}, url = '') {
    let response = await fetch(`${url}`, {
        method: "POST",
        mode: "cors",
        cache: "default",
        credentials: "include",
        headers: {"Content-Type": "application/json"},
        redirect: "follow",
        body: JSON.stringify(data)
    })
    // let result = await response.json()
}


addCommentBtn.addEventListener('click', visibleHandler)

saveBtn.addEventListener('click', () => {
    data = {"id": id, "message": textarea.value}
    addData(data, '/add_comment')
    visibleHandler()
})


async function getData(callback, id) {
    let rawData = await fetch(`/get_comment/${id}`)
    let data = await rawData.json()
    callback(data)
}

function showComment(data) {
    console.log(data)
    for (let foo of data) {
        let ulContainer = document.createElement('ul')
        ulContainer.innerHTML = `<li>${foo.message}</li><button type="button" id="editBtn" class="btn" onclick="window.location.href='/logout'">Edit</button>`
        commentContainer.appendChild(ulContainer)
    }
}

async function main() {
    await getData(showComment, id)
}

main()