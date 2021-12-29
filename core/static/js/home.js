$(function() {
    const header         = $('header').height();
    const window_height  = $(window).height();
    const window_width   = $(window).width();
    console.log(window_height);
    console.log(header);

    if( window_width > window_height){
        $('#swiper-top').css("height", window_height - header - 80  +"px");
    } else {
        $('#swiper-top').css("height", (window_height - header)*0.4  +"px");
    }

    const swiper01 = new Swiper('#swiper-top', {
        spaceBetween: 15,
        pagination: {
            el: '.swiper-pagination',
            dynamicBullets : true,
            dynamicMainBullets : 4,
            type: 'bullets',
        },
        autoplay: {
            delay: 5000,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        loop: 'true',
        effect: 'fade',
    });
});

$(function() {
    const embeddedVideos = document.getElementsByClassName('video-embed');
    if (embeddedVideos) {
        for (const video of embeddedVideos) {
            const embedCode = video.getAttribute('data-embed-code');
            video.innerHTML = embedCode;
        }
    }
});

// Função abaixo de Gabriel feita anteriormente pra enviar requisição de doação de oferta/dízimo (depreciado)
// $(document).ready(function() {
//     let donateForm = $("#donateForm");
//     donateForm.submit(function(event) {
//         event.preventDefault();
//         const formData = $(this).serialize();
//         const selectedPaymentOption = $("#id_payment_option option:selected").val();
//         let endpoint;
//         if (selectedPaymentOption == "pagseguro") {
//             endpoint = "/donate/pagseguro";
//         } else if (selectedPaymentOption == "paypal") {
//             endpoint = "";
//         }

//         $.ajax({
//             method: "POST",
//             url: endpoint,
//             data: formData,
//             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//             crossDomain: true,
//             success: handleFormSuccess,
//             error: handleFormError
//         });

//         function handleFormSuccess(data, textStatus, jqXHR) {
//             console.log(data);
//             console.log(textStatus);
//             console.log(jqXHR);
//             donateForm[0].reset();
//         }

//         function handleFormError(jqXHR, textStatus, errorThrown) {
//             console.log(jqXHR);
//             console.log(textStatus);
//             console.log(errorThrown);
//         }
//     });
// });