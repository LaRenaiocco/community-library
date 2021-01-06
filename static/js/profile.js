"use strict"

$('#upload-image-form').on('submit', (evt) => {
    evt.preventDefault();
    console.log('default prevented')
    // console.log($('#author-field').val())


    const formData = new FormData();
    formData.append('file', $('#image-field').prop('files')[0]);
    formData.append('title', $('#title-field').val());
    formData.append('author', $('#author-field').val());
    console.log(formData)

    $.ajax({
        type: 'POST',
        url: '/upload-image',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: (response) => {
            // console.log(response)
            // $('#image-div').text(response)
        }
    })
})

$('#book-search-btn').on('click', () => {
    document.location.href = '/search'
})