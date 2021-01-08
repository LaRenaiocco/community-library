$('#browse-all').on('click', () => {
	$.get('/books/browse-all', (data) => {
		$('#book-view').empty()
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
			response.forEach(book => {
				const title = book.title
				const author = book.author
				const url = book.image_url
				const $newBook =  $(`<div><img src='${url}'></br><div>${title}</div><div>${author}</div></div>`)
				$('#book-view').append($newBook)
				console.log(book.title)
			})
		}
	})			
})