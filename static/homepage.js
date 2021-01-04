"use strict"

$('#upload-image-form').on('submit', (evt) => {
    evt.preventDefault();
    console.log('default prevented')


    const formData = new FormData();
    formData.append('file', $('#image-field').prop('files')[0])

    $.ajax({
        type: 'POST',
        url: '/upload-image',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: (response) => {
            console.log(response)
            // $('#image-div').text(response)
        }
    })



})