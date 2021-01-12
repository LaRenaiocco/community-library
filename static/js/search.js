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
	data.forEach(book => {
		const bookId = book.book_id
		const title = book.title
		const author = book.author
		const url = book.image_url
		const ownerName = book.owner_name
		console.log(ownerName)
		const ownerId = book.owner_id
		const ownerPhone = book.owner_phone

		const bookCard = createBookCard(bookId, title, author, url, ownerName, ownerId)

	})
}

// function compileBookData(data) {
// 	const container = document.createElement('div')
// 	container.setAttribute('class', 'container')

// 	data.forEach((book,i) => {
// 		const bookId = book.book_id
// 		const title = book.title
// 		const author = book.author
// 		const url = book.image_url
// 		const ownerName = book.owner_name
// 		console.log(ownerName)
// 		const ownerId = book.owner_id
// 		const ownerPhone = book.owner_phone

// 		const bookCard = createBookCard(bookId, title, author, url, ownerName, ownerId)
// 		if (i === 0 || i % 3 === 0) {
// 			const row = document.createElement('div')
// 			row.setAttribute('class', 'row')
// 		}
// 	})
// }

// $.get('/profile/json', (data) => {
// 	// const books = data.books
// 	console.log(typeof data)
// 	if ( typeof data === "object") {
// 		  const container = document.createElement('div')
// 		  container.setAttribute('class', 'container')
// 		  data.forEach(book, i => {
// 			  if (i === 0 || i % 3 === 0) {
// 				  const row = document.createElement('div')
// 				  row.setAttribute('class', 'row')
// 				  container.appendChild(row)
// 				  const bookDiv = createBookDiv(book)
// 				  row.appendChild(bookDiv)
// 			  } else {
// 				  const bookDiv = createBookDiv(book)
// 				  row.appendChild(bookDiv)
// 			  }
// 		  })
// 		  $('#user-library-view').append(container)
// 	}
//   })

function createBookCard(bookId, title, author, url, ownerName, ownerId) {
	const d = document;
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
  borrowBtn.setAttribute('style', 'display: block')
  borrowBtn.setAttribute('id', `borrow-btn-${bookId}`)
  borrowBtn.addEventListener('click', () => {
    $(`#borrow${bookId}`).toggle()
    $(`#borrow-btn-${bookId}`).toggle()
    
	})
	const hiddenId = d.createElement("div")
	hiddenId.hidden = true
	hiddenId.textContent = `book id: ${bookId} owner id: ${ownerId}`
	cardBody.appendChild(cardTitle)
	cardBody.appendChild(cardAuthor)
	cardBody.appendChild(cardOwner)
	cardBody.appendChild(borrowBtn)
  cardBody.appendChild(hiddenId)
  
  const borrowDiv = d.createElement('div')
  borrowDiv.setAttribute('id', `borrow${bookId}`)
	borrowDiv.setAttribute('style', 'display: none')
		

	const borrowText = d.createElement('div')
	borrowText.textContent = 'By clicking "Borrow" you authorize Community Library to share your phone number with the book owner to facilitate this swap.'

		
	const cancel = d.createElement('button')
	cancel.textContent = 'Cancel'
	cancel.addEventListener('click', () =>{
    $(`#borrow${bookId}`).toggle()
    $(`#borrow-btn-${bookId}`).toggle()
	})
		
  const authorize = d.createElement('button')
	authorize.textContent = 'Borrow'
	authorize.addEventListener('click', () => {
    $.post('/books/borrow-book', {'book': bookId}, (response) => {
      alert(response)
    })
  })
    
  borrowDiv.appendChild(borrowText)
  borrowDiv.appendChild(cancel)
  borrowDiv.appendChild(authorize)
  bookCard.appendChild(borrowDiv)

	$('#book-view').append(bookCard)
	// return bookCard

}
// const cardBodyContent = `
// 	<h5 class="card-title">${title}<h5>
// 	<div class="card-text>
// 		<div>By: ${author}</div>
// 		<div>Owned by: ${owner}</div>

// 	<div>`