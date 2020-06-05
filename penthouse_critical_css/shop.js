const penthouse = require('penthouse')
const fs = require('fs')

penthouse({
  url: 'https://localhost/shop/microcontrollers',
  css: '/Users/Nikhil/Desktop/noobtronicsdjango/mysite/static/dist/css/app.0ecc9844.css',
  width: 1366,
  height: 768,
  renderWaitTime: 5000,
  keepLargerMediaQueries: true,
  blockJSRequests: false,
  screenshots: {
    basePath: 'shoppage', // absolute or relative; excluding file extension
    type: 'jpeg', // jpeg or png, png default
    quality: 80 // only applies for jpeg type
  }
})
.then(criticalCss => {
  // use the critical css
  fs.writeFileSync('shoppage.min.css', criticalCss);
})
