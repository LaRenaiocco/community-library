"use strict"

// Render books owned by user
$.get('/profile/json', (data) => {
    const books = data.books
    console.log(books)
})


// Sends book information to server for upload to DB and Cloudinary
$('#upload-image-form').on('submit', (evt) => {
    evt.preventDefault();
    console.log('default prevented')

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
        }
    })
})

// redirect to search page
$('#book-search-btn').on('click', () => {
    document.location.href = '/search'
})