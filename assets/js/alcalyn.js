$(document).on('keyup', Konami.code(function () {
    // Set comic sans
    $('head').append("<style>@font-face{font-family:'konami';font-style:normal;font-weight:400;src:local('konami'),local('konami-Regular'),url(/assets/fonts/konami/konami.woff) format('woff'),url(/assets/fonts/konami/konami.ttf) format('truetype');}</style>");
    $('head').append("<style>p, h1, h2, h3, h4, h5, h6, a, li { font-family: 'konami' !important; }</style>");

    // Add Clippy
    $('head').append('<link href="/assets/css/clippy.css" rel="stylesheet" type="text/css" />');
    clippy.load('Clippy', function(agent){
        agent.show();
    });
}));
