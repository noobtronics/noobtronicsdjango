const penthouse = require('penthouse')
const fs = require('fs')

penthouse({
  url: 'https://localhost/arduino-microcontrollers/arduino-uno',
  css: '/Users/Nikhil/Desktop/noobtronicsdjango/mysite/static/dist/css/app.24f62574.css',
  width: 1366,
  height: 768,
  renderWaitTime: 5000,
  keepLargerMediaQueries: true,
  blockJSRequests: false,
  screenshots: {
    basePath: 'productpage', // absolute or relative; excluding file extension
    type: 'jpeg', // jpeg or png, png default
    quality: 80 // only applies for jpeg type
  }
})
.then(criticalCss => {
  // use the critical css
  fs.writeFileSync('productpage.min.css', criticalCss);
})
