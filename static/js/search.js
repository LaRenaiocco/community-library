"use strict"

// returns and compiles all book data
$('#browse-all').on('click', () => {
	$.get('/books/browse-all', (response) => {
		$('#book-view').empty()
		compileBookData(response)
	})
})


// submits search data to server side and returns results
$('#search-form').on('submit', (evt) => {
	evt.preventDefault()

	const search = $('#search-input').val()
	const param = $('input[name=param]:checked', '#search-form').val()
	const formData = {'search': search, 'param': param}

	$.post('/books/search-books', formData, (response) => {
		// clear out the book-view display
		$('#book-view').empty()
		// string will be an error alert. Object will be successful data query
		if( typeof response === "string" ) {
			alert(response)
			document.getElementById("search-form").reset();
		} else if ( typeof response === "object") {
			compileBookData(response)
		}
	})			
})


// compiles all book data from search response
function compileBookData(data) {
	data.forEach(book => {
		const bookId = book.book_id
		const title = book.title
		const author = book.author
		const description = book.description
		const genre = book.genre
		const url = book.image_url
		const ownerName = book.owner_name
		const ownerId = book.owner_id

		createBookCard(bookId, title, author, description, genre, url, ownerName, ownerId)
	})
}


// creates each book card from compiled data
function createBookCard(bookId, title, author, description, genre, url, ownerName, ownerId) {
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

	const cardTitle = d.createElement("h6")
	cardTitle.setAttribute("class", "card-title")
	cardTitle.textContent = title
	cardBody.appendChild(cardTitle)

	const cardAuthor = d.createElement("div")
	cardAuthor.setAttribute("class", "card-text")
	cardAuthor.textContent = `By: ${author}`
	cardBody.appendChild(cardAuthor)

	const cardOwner = d.createElement("div")
	cardOwner.setAttribute("class", "card-text")
	cardOwner.textContent = `Owned by: ${ownerName}`
	cardBody.appendChild(cardOwner)

	if (genre !== 'None' && genre !== null) {
		const cardGenre = d.createElement('div')
		cardGenre.setAttribute("class", "card-text")
		cardGenre.textContent = `Genres: ${genre}`
		cardBody.appendChild(cardGenre)
	}
	if (description !== 'None' && description !== null) {
		const cardDescription = d.createElement('div')
		cardDescription.setAttribute("class", "card-text")
		cardDescription.textContent = `Description: ${description}`
		cardBody.appendChild(cardDescription)
	}
	const borrowBtn = d.createElement("button")
  borrowBtn.textContent = "Borrow Me"
  borrowBtn.setAttribute('style', 'display: block')
	borrowBtn.setAttribute('id', `borrow-btn-${bookId}`)
	borrowBtn.setAttribute('class', 'btn search-page-btns search-submit')
  borrowBtn.addEventListener('click', () => {
    $(`#borrow${bookId}`).toggle()
    $(`#borrow-btn-${bookId}`).toggle()
	})
	cardBody.appendChild(borrowBtn)

  const borrowDiv = d.createElement('div')
  borrowDiv.setAttribute('id', `borrow${bookId}`)
	borrowDiv.setAttribute('style', 'display: none')
	
	const borrowText = d.createElement('div')
	borrowText.textContent = `By clicking "Borrow" you authorize Community Library to share your phone number with ${ownerName} to facilitate this swap.`

	const cancel = d.createElement('button')
	cancel.setAttribute('class', 'btn search-page-btns')
	cancel.textContent = 'Cancel'
	cancel.addEventListener('click', () =>{
    $(`#borrow${bookId}`).toggle()
    $(`#borrow-btn-${bookId}`).toggle()
	})
		
	const authorize = d.createElement('button')
	authorize.setAttribute('class', 'btn search-page-btns')
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
}
