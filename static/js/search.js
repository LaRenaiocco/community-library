$('#browse-all').on('click', () => {
    $.get('/books/browse-all', (data) => {
        data.forEach(book => {
            const title = book.title
            const author = book.author
            const url = book.image_url
            const $newBook =  $(`<div><img src='${url}'></br><div>${title}</div><div>${author}</div></div>`)
            $('#book-view').append($newBook)
            console.log(book.title)
        })
    })
})