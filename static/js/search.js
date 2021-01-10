$('#browse-all').on('click', () => {
	$.get('/books/browse-all', (response) => {
		$('#book-view').empty()
		compileBookData(response)
		// data.forEach(book => {
		// 	const title = book.title
		// 	const author = book.author
		// 	const url = book.image_url
		// 	const $newBook =  $(`<div><img src='${url}'></br><div>${title}</div><div>${author}</div></div>`)
		// 	$('#book-view').append($newBook)

		// })
	})
})

$('#search-form').on('submit', (evt) => {
	evt.preventDefault()


	const search = $('#search-input').val()
	const param = $('input[name=param]:checked', '#search-form').val()
	console.log(search)
	console.log(param)
	const formData = {'search': search, 'param': param}
	// formData.append('search', $('#search-input').val())
	// formData.append('param', $('input[name=param]:checked', '#search-form').val())
	$.post('/books/search-books', formData, (response) => {
		console.log(response)
		console.log(typeof response)
		$('#book-view').empty()
		if( typeof response === "string" ) {
			alert(response)
			document.getElementById("search-form").reset();
		} else if ( typeof response === "object") {
			compileBookData(response)
			// response.forEach(book => {
			// 	const title = book.title
			// 	const author = book.author
			// 	const url = book.image_url
			// 	const $newBook =  $(`<div><img src='${url}'></br><div>${title}</div><div>${author}</div></div>`)
			// 	$('#book-view').append($newBook)
			// 	console.log(book.title)
			// })
		}
	})			
})

function compileBookData(data) {
	const d = document;
	data.forEach(book => {
		const bookId = book.book_id
		const title = book.title
		const author = book.author
		const url = book.image_url
		const ownerName = book.owner_name
		const ownerId = book.owner_id
		const ownerPhone = book.owner_phone

		const bookCard = d.createElement("div")
		bookCard.setAttribute("class", "card")
		bookCard.setAttribute("id", `bookid${bookId}-ownerid${ownerId}`)

		const bookImg = d.createElement("img")
		bookImg.setAttribute("class", "card-img-top")
		bookImg.src = url
		bookCard.appendChild(bookImg)

		const cardBody = d.createElement("div")
		cardBody.setAttribute("class", "card-body")
		bookCard.appendChild(cardBody)

		const cardTitle = d.createElement("h5")
		cardTitle.setAttribute("class", "card-title")
		cardTitle.textContent = title
		const cardAuthor = d.createElement("div")
		cardAuthor.setAttribute("class", "card-text")
		cardAuthor.textContent = `By: ${author}`
		const cardOwner = d.createElement("div")
		cardOwner.setAttribute("class", "card-text")
		cardOwner.textContent = `Owned by: ${ownerName}`
		const borrowBtn = d.createElement("button")
		borrowBtn.textContent = "Borrow Me"
		const hiddenId = d.createElement("div")
		hiddenId.hidden = true
		hiddenId.textContent = `book id: ${bookId} owner id: ${ownerId}`
		cardBody.appendChild(cardTitle)
		cardBody.appendChild(cardAuthor)
		cardBody.appendChild(cardOwner)
		cardBody.appendChild(borrowBtn)
		cardBody.appendChild(hiddenId)

		$('#book-view').append(bookCard)

	})
}

// const cardBodyContent = `
// 	<h5 class="card-title">${title}<h5>
// 	<div class="card-text>
// 		<div>By: ${author}</div>
// 		<div>Owned by: ${owner}</div>

// 	<div>`