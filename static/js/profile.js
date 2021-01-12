"use strict"

// Render books owned by user
$.get('/profile/json', (data) => {
	if ( typeof data === "object") {
		data.forEach(book => {
			createBookDiv(book)
		})
  }
})


// Sends book information to server for upload to DB and Cloudinary
$('#upload-image-form').on('submit', (evt) => {
    evt.preventDefault();

		// prepare formData object
    const selectedGenres = $('#checkboxes input:checked').map(function(i, el){return el.name;}).get();
		const formData = new FormData();
    formData.append('file', $('#image-field').prop('files')[0]);
    formData.append('title', $('#title-field').val());
    formData.append('author', $('#author-field').val());
    formData.append('genres', selectedGenres);
    formData.append('description', $('#description-field').val());

    $.ajax({
        type: 'POST',
        url: '/upload-image',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: (response) => {
            document.getElementById("upload-image-form").reset();
						alert('Book added to your personal library')
						const bookDiv = createBookDiv(response)
						$('#user-library-view').append(bookDiv)
        }
    })
})


// redirect to search page
$('#book-search-btn').on('click', () => {
    document.location.href = '/search'
})

// Creates Div with all information for one book in library
function createBookDiv(book) {
	const bookDiv = document.createElement('div')
	bookDiv.setAttribute('class', 'col')

	const bookTitle = document.createElement('span')
	bookTitle.textContent = book.title

	const viewBook = document.createElement('button')
	viewBook.setAttribute('class', 'view-book-btn')
	viewBook.textContent = 'Book Details'
	// event listener toggles additional book info
	viewBook.addEventListener('click', () => {
		$(`#book${book.book_id}`).toggle()
	})

	const deleteBook = document.createElement('button')
	deleteBook.setAttribute('class', 'delete-book-btn')
	deleteBook.textContent = 'Delete Book'
	// event listener toggles book delete options
	deleteBook.addEventListener('click', () => {
		$(`#delete${book.book_id}`).toggle()
	})

	bookDiv.appendChild(bookTitle)
	bookDiv.appendChild(viewBook)
	bookDiv.appendChild(deleteBook)

	const additionalInfo = document.createElement('div')
	additionalInfo.setAttribute('id', `book${book.book_id}`)
	additionalInfo.setAttribute('style', 'display: none')

	const bookAuthor = document.createElement('div')
	bookAuthor.textContent = `By: ${book.author}`

	const bookGenres = document.createElement('div')
	bookGenres.textContent = `Genres: ${book.genre}`

	const bookDescription = document.createElement('div')
	bookDescription.textContent = `Description: ${book.description}`

	additionalInfo.appendChild(bookAuthor)
	additionalInfo.appendChild(bookGenres)
	additionalInfo.appendChild(bookDescription)

	const deleteInfo = document.createElement('div')
	deleteInfo.setAttribute('id', `delete${book.book_id}`)
	deleteInfo.setAttribute('style', 'display: none')

	const delMessage = document.createElement('div')
	delMessage.textContent = `Are you sure you want to delete ${book.title} from your library?`

	const cancelBtn = document.createElement('button')
	cancelBtn.setAttribute('class', 'cancel-btn')
	cancelBtn.textContent = 'Cancel'
	cancelBtn.addEventListener('click', () => {
		$(`#delete${book.book_id}`).toggle()
	})

	const deleteBtn = document.createElement('button')
	deleteBtn.setAttribute('class', 'delete-book-btn')
	deleteBtn.textContent = 'DELETE'
	deleteBtn.addEventListener('click', () => {
		$.post('/delete-book', {book: `${book.book_id}`}, (response) => {
			bookDiv.remove()
			alert(response)
		})
	})

	deleteInfo.appendChild(delMessage)
	deleteInfo.appendChild(cancelBtn)
	deleteInfo.appendChild(deleteBtn)

	bookDiv.appendChild(additionalInfo)
	bookDiv.appendChild(deleteInfo)

	$('#user-library-view').append(bookDiv)
}


