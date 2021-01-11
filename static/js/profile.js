"use strict"

// Render books owned by user
$.get('/profile/json', (data) => {
  // const books = data.books
  console.log(typeof data)
  if ( typeof data === "object") {
		createBookDiv(data)

			// deleteBook.addEventListener('click', () => {
			// 	alert('Trigger Modal')
			// })
  }
})


// Sends book information to server for upload to DB and Cloudinary
$('#upload-image-form').on('submit', (evt) => {
    evt.preventDefault();

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
            console.log('book uploaded')
            alert(response)
						// $('#image-div').text(response)
						// $('#user-library-view').append(bookDiv)
        }
    })
})


// redirect to search page
$('#book-search-btn').on('click', () => {
    document.location.href = '/search'
})

// Creates Div with all information for one book in library
function createBookDiv(data) {
	data.forEach(book => {
		const bookDiv = document.createElement('div')

		const bookTitle = document.createElement('span')
		bookTitle.textContent = book.title

		const viewBook = document.createElement('button')
		viewBook.setAttribute('class', 'view-book-btn')
		viewBook.textContent = 'Book Details'
		viewBook.addEventListener('click', () => {
			$(`#book${book.book_id}`).toggle()
			})

		const deleteBook = document.createElement('button')
		deleteBook.setAttribute('class', 'delete-book-btn')
		deleteBook.textContent = 'Delete Book'

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
		bookDescription.textContent = `Description ${book.description}`

		additionalInfo.appendChild(bookAuthor)
		additionalInfo.appendChild(bookGenres)
		additionalInfo.appendChild(bookDescription)

		bookDiv.appendChild(additionalInfo)

		$('#user-library-view').append(bookDiv)

		})
}